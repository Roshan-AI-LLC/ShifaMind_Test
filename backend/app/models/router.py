"""Concept routing for inference. Must match training exactly.

The training pipeline routes from a precomputed silver matrix built by
`12_silver_labels.py`; at serving time there is no precomputed matrix, so the
same result is produced live. Every step below is pinned to a specific line of
the training code, because this is the component whose failures are silent: a
router that drifts still returns plausible ICD-10 codes, and only the gate
values shown to the clinician are wrong.

The contract, and where each part comes from:

1. TEXT      `LIGHT_PREPROCESSOR` in `shifamind/data/text.py`, selected by
             `12_silver_labels.py --text-col text_light` (its default).
             Lowercase, collapse whitespace, strip. Digits and punctuation
             survive, because several codes in this label space are defined by
             lab values.

2. BANK      `canonicalize(load_jsonl(merged_umls_records.jsonl))`. The file is
             already canonical, so canonicalize takes its fast path and the bank
             preserves FILE ORDER. Concept integer index == line number ==
             row of concept_queries.npy. Verified: the queries sidecar `ids`
             array is identical to the bank's concept ids, in order.

3. MATCHER   `ConceptMatcher(surface_map(bank), numeric_rules=RULES,
             numeric_map=numeric_map_for(bank))`, exactly as
             `shifamind/concepts/silver.py:_silver_chunk`. Numeric rules are ON:
             `12_silver_labels.py` defaults `--numeric` to True. scope and
             use_sections stay at their defaults (6, True).

4. ROUTE     count = affirmed + negated, per `ShifaMindDataset.__init__`
             (`route_assertions=("affirmed", "negated")`). NOT affirmed alone:
             routing on affirmed would make every routed concept present by
             construction and the concept head would learn to output 1.

5. TOP-K     `ShifaMindDataset.__getitem__`. If a note routes <= top_k concepts
             they are emitted in ASCENDING CONCEPT INDEX order, because that is
             what scipy hands back from a CSR row. Only when the note exceeds
             top_k does the lexsort run: count descending, ties broken by
             concept index ascending. Both orders are reproduced here. The model
             sums over slots so order does not change the logits, but the parity
             harness compares arrays element-wise and the displayed top-N
             depends on it.

A NOTE ON SECTION HEADERS. `use_sections=True` is passed, matching training, but
it cannot fire on `text_light`: the light preprocessor collapses newlines into
spaces and lowercases, while `_HEADER_RE` needs a line start and `_ANY_HEADER_RE`
needs a capital letter. So the FAMILY / HISTORICAL section logic is inert in this
pipeline and only the in-sentence triggers apply. That is training behaviour and
is reproduced deliberately; it is not a bug to fix here.
"""

from __future__ import annotations

import json
import logging
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ..concepts.bank import canonicalize, surface_map
from ..concepts.negex import Assertion, ConceptMatcher

log = logging.getLogger(__name__)

#: Routed assertion classes. ShifaMindDataset default.
ROUTE_ASSERTIONS: tuple[str, ...] = ("affirmed", "negated")

#: MCBConfig.top_k for w768_honest.
TOP_K = 384

_WS = re.compile(r"\s+")


def light_text(text: str) -> str:
    """`LIGHT_PREPROCESSOR` for a single string.

    pandas: `s.str.lower()` then `.replace(r"\\s+", " ", regex=True)` then
    `.strip()`. Nothing else runs: mullenbach stripping and digit removal are
    both off for this column.
    """
    return _WS.sub(" ", str(text).lower()).strip()


@dataclass
class RoutedNote:
    concept_ids: np.ndarray      # (n,) int64, model embedding indices
    concept_mask: np.ndarray     # (n,) int64, all ones before collation
    counts: np.ndarray           # (n,) float32, routed mention counts
    names: list[str]             # concept display names, aligned to concept_ids
    spans: list[dict]            # every match, for the evidence panel
    n_matched: int               # distinct concepts before top-k truncation
    truncated: bool              # True when n_matched > top_k


class ConceptRouter:
    def __init__(self, bank_path: Path, top_k: int = TOP_K, numeric: bool = True):
        records = [json.loads(line) for line in
                   Path(bank_path).read_text().splitlines() if line.strip()]
        self.bank, _ = canonicalize(records)
        self.concept_ids: list[str] = list(self.bank.keys())
        self.index: dict[str, int] = {c: i for i, c in enumerate(self.concept_ids)}
        self.names: list[str] = [self.bank[c].get("name", c) for c in self.concept_ids]
        self.top_k = top_k

        rules, nmap = None, None
        if numeric:
            from ..concepts.evalsetup_numeric import numeric_map_for
            from ..concepts.numeric import RULES
            rules, nmap = RULES, numeric_map_for(self.bank)
        self.matcher = ConceptMatcher(surface_map(self.bank),
                                      numeric_rules=rules, numeric_map=nmap)
        log.info("router ready: %d concepts, top_k=%d, numeric=%s",
                 len(self.concept_ids), top_k, numeric)

    # ------------------------------------------------------------------
    def route(self, raw_text: str, keep_spans: bool = True) -> RoutedNote:
        text = light_text(raw_text)
        summary, matches = self.matcher.match(text, keep_spans=keep_spans)

        counts: dict[str, float] = defaultdict(float)
        for a in ROUTE_ASSERTIONS:
            for cid, n in summary.bucket(Assertion(a)).items():
                if n:
                    counts[cid] += float(n)

        if not counts:
            return RoutedNote(np.zeros(0, np.int64), np.zeros(0, np.int64),
                              np.zeros(0, np.float32), [], [], 0, False)

        # scipy hands a CSR row back with indices ASCENDING. Reproduce that,
        # because when a note routes <= top_k concepts the dataset does no
        # sorting at all and this order is what the model saw in training.
        idx = np.array(sorted(self.index[c] for c in counts), dtype=np.int64)
        rev = {self.index[c]: c for c in counts}
        val = np.array([counts[rev[int(i)]] for i in idx], dtype=np.float32)

        n_matched = int(idx.size)
        truncated = n_matched > self.top_k
        if truncated:
            # ShifaMindDataset.__getitem__: keep the most-mentioned, ties broken
            # by concept id so a rerun selects the same slots.
            keep = np.lexsort((idx, -val))[:self.top_k]
            idx, val = idx[keep], val[keep]

        spans = [{"concept": m.concept_id,
                  "name": self.bank[m.concept_id].get("name", m.concept_id),
                  "surface": m.surface, "start": m.start, "end": m.end,
                  "assertion": m.assertion.value}
                 for m in matches] if keep_spans else []

        return RoutedNote(
            concept_ids=idx,
            concept_mask=np.ones_like(idx),
            counts=val,
            names=[self.names[int(i)] for i in idx],
            spans=spans,
            n_matched=n_matched,
            truncated=truncated,
        )
