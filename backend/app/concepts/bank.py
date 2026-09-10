"""Canonicalisation: per-code concept lists → one shared bank.

Generation runs per code, which is what guarantees tail coverage — every code
gets concepts by construction. But if the output stays per-code you have ~40k
concepts each referenced by exactly one code, which is just a wider copy of the
label space: no sharing between related codes, nothing for routing to exploit,
and a bottleneck that bottlenecks nothing.

The value is in the collapse. "low serum potassium" should be one concept that
E87.6, E87.1 and N17.9 all point at. This module performs that merge and emits
the concept→code incidence matrix that everything downstream is scored on.

Merging is deliberately conservative and lexical — surface-form overlap and
normalised-name identity. Embedding-based merging would collapse more, but it
also collapses clinically distinct things ("hyperkalemia"/"hypokalemia" sit very
close in embedding space), and a wrong merge is far more damaging than a missed
one: it silently ties together codes that should stay separable.
"""

from __future__ import annotations

import logging
import re
from collections import defaultdict

log = logging.getLogger(__name__)

_STOP = {"of", "the", "a", "an", "in", "on", "with", "and", "or", "to", "for"}
_PLURAL = re.compile(r"(?<=[a-z])s$")


def normalize_name(name: str) -> str:
    """Lowercase, strip punctuation, drop stopwords, naive singularise, sort.

    Sorting the tokens makes "potassium low serum" and "low serum potassium"
    identical, which is the most common way two models phrase the same concept.
    """
    toks = re.findall(r"[a-z0-9]+", str(name).lower())
    toks = [_PLURAL.sub("", t) for t in toks if t not in _STOP]
    return " ".join(sorted(toks))


def canonicalize(
    records: list[dict],
    min_codes: int = 1,
    surface_overlap: float = 0.5,
) -> tuple[dict[str, dict], dict[str, set[str]]]:
    """Merge per-code concepts into a shared bank.

    Args:
        records: ``[{"code": ..., "concepts": [...]}, ...]`` from generation.
        min_codes: drop concepts referenced by fewer than this many codes.
        surface_overlap: Jaccard threshold on surface-form sets above which two
            differently-named concepts are treated as the same concept.

    Returns:
        ``(bank, concept_to_codes)`` where ``bank`` maps concept_id to
        ``{name, category, type, surface_forms, codes, n_codes}``.
    """
    # An already-canonical bank passes straight through. 22_bank_umls.py emits
    # per-concept records (concept/name/surface_forms/codes); generation emits
    # per-code records ({"code", "concepts": [...]}). Re-canonicalising the
    # former would re-run the merge and silently discard the CUI assignments and
    # the UMLS links, so detect the shape instead of assuming it.
    if records and "concept" in records[0] and "concepts" not in records[0]:
        bank = {r["concept"]: {
            "name": r.get("name", r["concept"]),
            "category": r.get("category", "other"),
            "type": r.get("type", "finding"),
            "surface_forms": list(r.get("surface_forms", [])),
            "codes": list(r.get("codes", [])),
            "n_codes": len(r.get("codes", [])),
            **({"cuis": r["cuis"]} if "cuis" in r else {}),
        } for r in records}
        log.info("bank already canonical: %d concepts, %.2f codes/concept mean, "
                 "%.1f surface forms/concept mean", len(bank),
                 sum(v["n_codes"] for v in bank.values()) / max(len(bank), 1),
                 sum(len(v["surface_forms"]) for v in bank.values())
                 / max(len(bank), 1))
        return bank, {cid: set(v["codes"]) for cid, v in bank.items()}

    # Pass 1 — group by normalised name.
    groups: dict[str, dict] = {}
    for rec in records:
        code = rec["code"]
        for c in rec["concepts"]:
            key = normalize_name(c["name"])
            if not key:
                continue
            g = groups.setdefault(key, {
                "names": [], "categories": [], "types": [],
                "surface_forms": set(), "codes": set(),
            })
            g["names"].append(c["name"])
            g["categories"].append(c.get("category", "other"))
            g["types"].append(c.get("type", "finding"))
            g["surface_forms"].update(c.get("surface_forms", []))
            g["codes"].add(code)

    # Pass 2 — merge groups whose surface forms overlap heavily. Bucketed by a
    # shared surface form so this stays near-linear instead of O(n^2).
    by_form: dict[str, list[str]] = defaultdict(list)
    for key, g in groups.items():
        for f in g["surface_forms"]:
            by_form[f].append(key)

    parent = {k: k for k in groups}

    def find(k: str) -> str:
        while parent[k] != k:
            parent[k] = parent[parent[k]]
            k = parent[k]
        return k

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    # A generic surface form ("infection", "pain") can land in hundreds of
    # concepts, and the pairwise comparison below is quadratic in bucket size.
    # Such forms are also uninformative for merging, so skip the huge buckets.
    MAX_BUCKET = 60
    skipped_buckets = 0
    for form, keys in by_form.items():
        if len(keys) < 2:
            continue
        if len(keys) > MAX_BUCKET:
            skipped_buckets += 1
            continue
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                a, b = groups[keys[i]]["surface_forms"], groups[keys[j]]["surface_forms"]
                inter = len(a & b)
                if inter and inter / len(a | b) >= surface_overlap:
                    union(keys[i], keys[j])

    if skipped_buckets:
        log.info("skipped %d oversized surface-form buckets during merge "
                 "(>%d concepts share one form)", skipped_buckets, MAX_BUCKET)

    merged: dict[str, dict] = {}
    for key, g in groups.items():
        root = find(key)
        m = merged.setdefault(root, {
            "names": [], "categories": [], "types": [],
            "surface_forms": set(), "codes": set(),
        })
        for f in ("names", "categories", "types"):
            m[f].extend(g[f])
        m["surface_forms"].update(g["surface_forms"])
        m["codes"].update(g["codes"])

    def majority(xs: list[str]) -> str:
        return max(set(xs), key=xs.count) if xs else "other"

    bank: dict[str, dict] = {}
    for i, (root, m) in enumerate(sorted(merged.items())):
        if len(m["codes"]) < min_codes:
            continue
        cid = f"c{i:05d}"
        bank[cid] = {
            "name": majority(m["names"]),
            "category": majority(m["categories"]),
            "type": majority(m["types"]),
            "surface_forms": sorted(m["surface_forms"]),
            "codes": sorted(m["codes"]),
            "n_codes": len(m["codes"]),
        }

    concept_to_codes = {cid: set(v["codes"]) for cid, v in bank.items()}
    raw = sum(len(r["concepts"]) for r in records)
    log.info(
        "canonicalised %d raw concepts → %d unique (%.1f%% collapse), "
        "%.2f codes/concept mean",
        raw, len(bank),
        100 * (1 - len(bank) / max(raw, 1)),
        sum(v["n_codes"] for v in bank.values()) / max(len(bank), 1),
    )
    return bank, concept_to_codes


def surface_map(bank: dict[str, dict]) -> dict[str, list[str]]:
    """``{concept_id: [surface_form, ...]}`` for :class:`ConceptMatcher`."""
    return {cid: v["surface_forms"] for cid, v in bank.items()}
