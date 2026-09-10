"""Assertion detection for clinical concept mentions.

A rewrite of the earlier NegEx pass. That version had four correctness bugs and one
feasibility problem; all are addressed here.

What was wrong before
----------------------
1.  **Triggers were matched as substrings.** ``any(t in pre_text for t in
    PRE_NEGATION_TRIGGERS)`` with ``"no"`` in the trigger list fires on
    *normal*, *noted*, *nodular*, *nocturnal*, *known*, *diagnosis*; ``"not"``
    fires on *notable* and *nothing*. Those are among the most common words in a
    discharge summary, so a large fraction of true concept mentions were being
    marked negated. Triggers here are matched with word boundaries.
2.  **Token offsets drifted.** ``sent.split()`` collapses runs of whitespace but
    the offset accumulator advanced by ``len(tok) + 1``, so every tab, newline or
    double space shifted the computed concept position — and clinical notes are
    full of irregular whitespace. Offsets here come from the tokenizer itself.
3.  **Multi-word concepts were treated as one token.** The forward scope started
    at ``concept_tok_idx + 1``, i.e. the *second word of the concept*, so part of
    the concept sat inside its own scope window. Spans are explicit here.
4.  **Scope truncation used the first terminator, not the last.** For text
    preceding a concept you want everything after the *last* boundary; using the
    first left stale triggers from earlier clauses inside the window.

And the feasibility problem: the earlier pass ran one regex scan per (note, concept) pair.
At 122k notes x ~3k concepts that is ~370M scans. Here every surface form goes
into a single Aho-Corasick automaton, so each note is scanned once regardless of
bank size, and assertion logic runs only at actual match sites.

What it does beyond negation
----------------------------
Negation alone mislabels clinical text. Following ConText (Harkema et al., 2009)
this tags four independent axes, because each produces a *different* kind of
false positive for patient-level coding:

* ``NEGATED``     — "no evidence of pneumonia"
* ``HYPOTHETICAL``— "rule out MI", "concerning for sepsis" (being tested for)
* ``FAMILY``      — under Family History, or "mother with diabetes" (wrong person)
* ``HISTORICAL``  — under Past Medical History, "h/o CHF" (wrong encounter)
* ``AFFIRMED``    — none of the above

Only ``AFFIRMED`` should count as concept-present for supervising this
admission's codes. The others are returned separately rather than discarded, so
downstream code can decide — historical mentions in particular are genuinely
predictive for some chronic codes and you may want them back.
"""

from __future__ import annotations

import logging
import re
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum

log = logging.getLogger(__name__)

try:
    import ahocorasick
    _HAVE_AHOCORASICK = True
except ImportError:  # pragma: no cover - fallback path
    _HAVE_AHOCORASICK = False


class Assertion(str, Enum):
    AFFIRMED = "affirmed"
    NEGATED = "negated"
    HYPOTHETICAL = "hypothetical"
    FAMILY = "family"
    HISTORICAL = "historical"


# ---------------------------------------------------------------------------
# Lexicons
#
# Ordered longest-first where phrases overlap, so "no evidence of" is tested
# before bare "no". Every entry is matched with word boundaries.
# ---------------------------------------------------------------------------

PRE_NEGATION = [
    "no evidence of", "no evidence for", "no signs of", "no sign of",
    "no symptoms of", "no indication of", "no complaints of", "no findings of",
    "not evidence of", "without evidence of", "without any evidence of",
    "negative for", "neg for", "nonreactive for",
    "ruled out for", "ruled out",
    "denies any", "denies", "denied", "denying",
    "free of", "resolved", "cleared of",
    "no longer", "no acute", "no known",
    "did not", "does not", "do not", "was not", "were not",
    "is not", "are not", "has not", "have not", "had not", "cannot", "can not",
    "without", "absent", "never", "none", "no", "not",
]

POST_NEGATION = [
    "was ruled out", "were ruled out", "have been ruled out", "has been ruled out",
    "were negative", "was negative", "is negative", "are negative",
    "not present", "not seen", "not found", "not detected",
    "not demonstrated", "not identified", "not appreciated", "not noted",
    "is absent", "are absent", "was absent",
    # Hedged post-negation. Standard NegEx carries these and ours did not, so
    # "heart failure is unlikely" was scoring as an affirmed heart failure.
    "is unlikely", "was unlikely", "seems unlikely", "appears unlikely",
    "unlikely", "is doubtful", "doubtful",
]

# Pseudo-negations: contain a negation token but do not negate anything.
PSEUDO_NEGATION = [
    "no increase", "no decrease", "no change", "no interval change",
    "no significant change", "no further", "no new",
    "not only", "not necessarily", "not certain", "not clear", "not cause",
    "no reason", "without difficulty", "without hesitation", "without incident",
    "without complication", "without complications",
    "cannot be excluded", "cannot be ruled out", "not be excluded",
    "not rule out", "no doubt",
    # "not ruled out" means the diagnosis is still live. Without this the
    # PRE_NEGATION entry "ruled out for" fires and the concept is recorded as
    # explicitly absent — the exact inversion of what the note says.
    "not ruled out", "not been ruled out", "not entirely ruled out",
    "not completely ruled out", "not fully ruled out", "not excluded",
]

# Being investigated / possible — an ICD code should not be assigned from these.
HYPOTHETICAL = [
    "rule out", "r/o", "to evaluate for", "evaluate for", "assess for",
    "concerning for", "concern for", "worrisome for", "suspicious for",
    "suggestive of", "cannot exclude", "cannot be excluded",
    "possible", "possibly", "probable", "presumed", "presumptive",
    "questionable", "question of", "versus", "vs",
    "differential includes", "differential diagnosis",
    "if he develops", "if she develops", "if the patient develops",
    "should he", "should she", "in case of", "watch for", "monitor for",
    "return if", "risk of", "at risk for", "prophylaxis for", "prophylaxis against",
]

# Someone other than the patient.
FAMILY = [
    "mother", "father", "sister", "brother", "son", "daughter",
    "aunt", "uncle", "cousin", "grandmother", "grandfather", "grandparent",
    "parents", "sibling", "siblings", "maternal", "paternal",
    "family history of", "fh of", "familial",
]

# Prior encounters rather than this admission.
HISTORICAL = [
    "history of", "hx of", "h/o", "past medical history",
    "previously", "in the past", "prior to admission", "prior history",
    "status post", "s/p", "years ago", "months ago", "remote history",
    "chronic", "long standing", "longstanding",
]

# Section headers that set assertion for everything beneath them until the next
# header. Matched at line starts on the raw (pre-lowercased) text.
SECTION_HEADERS: dict[str, Assertion] = {
    "family history": Assertion.FAMILY,
    "social history": Assertion.FAMILY,
    "past medical history": Assertion.HISTORICAL,
    "past surgical history": Assertion.HISTORICAL,
    "pmh": Assertion.HISTORICAL,
    "psh": Assertion.HISTORICAL,
    "prior hospitalizations": Assertion.HISTORICAL,
    "allergies": Assertion.HISTORICAL,
}

#: Clause boundaries that terminate a trigger's scope.
SCOPE_TERMINATORS = re.compile(
    r"[.;:!?]|\b(?:but|however|although|though|yet|except|aside from|apart from)\b",
    re.IGNORECASE,
)

#: Default scope in tokens either side of a concept mention.
DEFAULT_SCOPE = 6

_TOKEN_RE = re.compile(r"[A-Za-z0-9_/\-']+")

# Abbreviations whose trailing period must not end a sentence.
_ABBREV = {
    "dr", "mr", "mrs", "ms", "prof", "vs", "approx", "no", "pt", "hr",
    "mg", "ml", "mcg", "kg", "cm", "mm", "dl", "meq", "iu", "po", "iv",
    "q", "qd", "bid", "tid", "qid", "prn", "am", "pm", "hs", "sq", "sc",
    "a", "b", "c", "d", "e", "i", "m",
}


def _compile_lexicon(phrases: list[str]) -> re.Pattern:
    """One word-boundary alternation per lexicon, longest phrase first.

    Sorting by length matters: without it ``no`` would match inside the span of
    ``no evidence of`` and the more specific phrase would never be credited.
    """
    ordered = sorted(set(phrases), key=len, reverse=True)
    joined = "|".join(re.escape(p) for p in ordered)
    # The alternation MUST be wrapped in a non-capturing group. `|` binds looser
    # than concatenation, so `(?<!\w)a|b|c(?!\w)` applies the lookbehind only to
    # `a` and the lookahead only to `c`, leaving everything between unguarded —
    # which is how `not` ends up matching inside `notable`. Exactly the failure
    # this module exists to fix, so it is worth being explicit about.
    return re.compile(rf"(?<![A-Za-z0-9])(?:{joined})(?![A-Za-z0-9])", re.IGNORECASE)


_RE_PRE_NEG = _compile_lexicon(PRE_NEGATION)
_RE_POST_NEG = _compile_lexicon(POST_NEGATION)
_RE_PSEUDO = _compile_lexicon(PSEUDO_NEGATION)
_RE_HYPO = _compile_lexicon(HYPOTHETICAL)
_RE_FAMILY = _compile_lexicon(FAMILY)
_RE_HIST = _compile_lexicon(HISTORICAL)


# ---------------------------------------------------------------------------
# Sentence and token segmentation
# ---------------------------------------------------------------------------

def split_sentences(text: str) -> list[tuple[int, int]]:
    """Return (start, end) char spans of sentences.

    Splits on newlines and on terminal punctuation, but not on periods that
    belong to a known abbreviation or sit inside a decimal number — both of
    which are everywhere in clinical text ("q.d.", "2.5 mg", "Dr. Smith").
    """
    spans: list[tuple[int, int]] = []
    start = 0
    for m in re.finditer(r"[.!?;]+(?=\s|$)|\n+", text):
        end = m.start()
        if text[m.start()] == ".":
            before = text[max(0, end - 12):end]
            word = re.search(r"([A-Za-z0-9]+)$", before)
            if word and word.group(1).lower() in _ABBREV:
                continue
            if end + 1 < len(text) and text[end + 1].isdigit():
                continue  # decimal
        if end > start:
            spans.append((start, end))
        start = m.end()
    if start < len(text):
        spans.append((start, len(text)))
    return [(s, e) for s, e in spans if e > s]


def tokenize(text: str) -> list[tuple[int, int]]:
    """Token char spans. Offsets come from the regex, so whitespace never drifts."""
    return [(m.start(), m.end()) for m in _TOKEN_RE.finditer(text)]


# ---------------------------------------------------------------------------
# Section map
# ---------------------------------------------------------------------------

_HEADER_RE = re.compile(
    r"^[ \t]*(" + "|".join(re.escape(h) for h in sorted(SECTION_HEADERS, key=len, reverse=True)) + r")[ \t]*:",
    re.IGNORECASE | re.MULTILINE,
)
_ANY_HEADER_RE = re.compile(r"^[ \t]*[A-Z][A-Za-z /\-]{2,40}:", re.MULTILINE)


def section_spans(text: str) -> list[tuple[int, int, Assertion]]:
    """Char ranges governed by an assertion-setting section header.

    A header's influence runs until the next header of any kind, so a concept
    under "Family History:" is tagged FAMILY but one under the "Assessment:"
    that follows is not.
    """
    out: list[tuple[int, int, Assertion]] = []
    all_headers = [m.start() for m in _ANY_HEADER_RE.finditer(text)]
    for m in _HEADER_RE.finditer(text):
        label = SECTION_HEADERS[m.group(1).lower()]
        start = m.end()
        nxt = [h for h in all_headers if h > m.start()]
        end = nxt[0] if nxt else len(text)
        out.append((start, end, label))
    return out


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------

@dataclass
class Match:
    concept_id: str
    surface: str
    start: int
    end: int
    assertion: Assertion
    sentence: str = ""


@dataclass
class MatchSummary:
    """Per-note tallies, one entry per concept that matched at least once."""

    affirmed: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    negated: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    hypothetical: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    family: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    historical: dict[str, int] = field(default_factory=lambda: defaultdict(int))

    def bucket(self, a: Assertion) -> dict[str, int]:
        return {
            Assertion.AFFIRMED: self.affirmed,
            Assertion.NEGATED: self.negated,
            Assertion.HYPOTHETICAL: self.hypothetical,
            Assertion.FAMILY: self.family,
            Assertion.HISTORICAL: self.historical,
        }[a]

    def present(self) -> set[str]:
        """Concepts with at least one affirmed mention."""
        return {c for c, n in self.affirmed.items() if n > 0}

    def any_mention(self) -> set[str]:
        s: set[str] = set()
        for d in (self.affirmed, self.negated, self.hypothetical,
                  self.family, self.historical):
            s |= set(d)
        return s


class ConceptMatcher:
    """Single-pass multi-concept matcher with ConText assertion tagging.

    Args:
        concepts: ``{concept_id: [surface_form, ...]}``. Surface forms are
            lowercased and matched on word boundaries.
        scope: token window either side of a mention searched for triggers.
        use_sections: honour assertion-setting section headers.
    """

    def __init__(
        self,
        concepts: dict[str, list[str]],
        scope: int = DEFAULT_SCOPE,
        use_sections: bool = True,
        numeric_rules=None,
        numeric_map: dict[str, list[str]] | None = None,
    ) -> None:
        """``numeric_rules`` is an optional tuple of
        :class:`shifamind.concepts.numeric.NumericRule`. Their matches join the
        literal ones *before* overlap resolution and assertion, so a value
        mention is negated, historical or family-attributed by exactly the same
        ConText pass as a string mention — "no longer hyperkalemic, K 4.1" must
        not fire, and neither must "father had an EF of 20%".
        """
        self.scope = scope
        self.use_sections = use_sections
        self.surface_to_ids: dict[str, set[str]] = defaultdict(set)
        for cid, forms in concepts.items():
            for f in forms:
                f = " ".join(str(f).lower().split())
                if f:
                    self.surface_to_ids[f].add(cid)

        # Numeric rules resolve to a concept only after their value is read, so
        # each (rule, bucket) pair gets a sentinel surface key registered up
        # front; the match loop then treats them exactly like literal hits.
        self._numeric = []
        if numeric_rules:
            from .numeric import compile_rules, concept_names
            # With a map supplied, a rule whose concept is absent from the bank
            # must be dropped entirely, not fall back to its own name: the name
            # is not a bank id, and emitting it produces a KeyError downstream
            # when the column index is looked up. Without a map (tests,
            # notebooks, no bank at all) the name IS the id.
            kept = []
            for rule in numeric_rules:
                live = False
                for cname in (rule.concept_low(), rule.concept_high()):
                    if cname not in concept_names():
                        continue
                    cids = [cname] if numeric_map is None else numeric_map.get(cname, [])
                    for cid in cids:
                        self.surface_to_ids[f"\x00num:{cname}"].add(cid)
                        live = True
                if live:
                    kept.append(rule)
            self._numeric = compile_rules(tuple(kept)) if kept else []

        self._automaton = None
        if _HAVE_AHOCORASICK and self.surface_to_ids:
            A = ahocorasick.Automaton()
            for surface in self.surface_to_ids:
                if surface.startswith("\x00"):
                    continue          # sentinel for a numeric rule, not a literal
                A.add_word(surface, surface)
            A.make_automaton()
            self._automaton = A
        elif self.surface_to_ids:
            log.warning(
                "pyahocorasick not installed — falling back to regex alternation. "
                "This is far slower on a full-size bank; `pip install pyahocorasick`."
            )
            self._fallback_re = _compile_lexicon(list(self.surface_to_ids))

    # -- surface-form scan ---------------------------------------------------

    def _raw_matches(self, lowered: str) -> list[tuple[int, int, str]]:
        """(start, end, surface) for every surface form, word-boundary enforced.

        Aho-Corasick is substring-based, so boundaries are checked afterwards —
        this is the check whose absence caused the earlier pass to fire ``no`` inside
        ``normal``.
        """
        out: list[tuple[int, int, str]] = []
        if self._automaton is not None:
            for end_idx, surface in self._automaton.iter(lowered):
                start = end_idx - len(surface) + 1
                end = end_idx + 1
                if start > 0 and (lowered[start - 1].isalnum() or lowered[start - 1] == "_"):
                    continue
                if end < len(lowered) and (lowered[end].isalnum() or lowered[end] == "_"):
                    continue
                out.append((start, end, surface))
        else:
            for m in self._fallback_re.finditer(lowered):
                out.append((m.start(), m.end(), m.group(0)))

        for rx, rule in self._numeric:
            from .numeric import evaluate
            for m in rx.finditer(lowered):
                cname = evaluate(rule, m.group(1))
                if cname:
                    out.append((m.start(), m.end(), f"\x00num:{cname}"))

        # Longest match wins where surface forms overlap. Without this, a bank
        # containing both "heart failure" and "congestive heart failure" counts
        # one written mention twice, inflating the frequencies that the lift and
        # redundancy measures are computed from.
        out.sort(key=lambda r: (r[0], -(r[1] - r[0])))
        kept: list[tuple[int, int, str]] = []
        last_end = -1
        for start, end, surface in out:
            if start >= last_end:
                kept.append((start, end, surface))
                last_end = end
        return kept

    # -- assertion -----------------------------------------------------------

    def _assert_at(
        self,
        sent: str,
        rel_start: int,
        rel_end: int,
    ) -> Assertion:
        """Classify one mention, given its span within its sentence."""
        toks = tokenize(sent)
        if not toks:
            return Assertion.AFFIRMED

        # Token indices covering the concept span. Doing this by span rather than
        # by a single index is what keeps multi-word concepts out of their own
        # scope window.
        first = next((i for i, (s, e) in enumerate(toks) if e > rel_start), 0)
        last = next((i for i in range(len(toks) - 1, -1, -1) if toks[i][0] < rel_end), first)

        lo = max(0, first - self.scope)
        hi = min(len(toks), last + 1 + self.scope)
        pre = sent[toks[lo][0]: toks[first][0]] if first > lo else ""
        post = sent[toks[last][1]: toks[hi - 1][1]] if hi - 1 > last else ""

        # Truncate at clause boundaries: for the preceding window keep text after
        # the LAST terminator; for the following window keep text before the
        # FIRST. The earlier pass used the first in both directions, leaking stale triggers.
        pre_bounds = list(SCOPE_TERMINATORS.finditer(pre))
        if pre_bounds:
            pre = pre[pre_bounds[-1].end():]
        post_bound = SCOPE_TERMINATORS.search(post)
        if post_bound:
            post = post[:post_bound.start()]

        window = f"{pre} {post}"

        # Pseudo-negations veto negation only, not the other axes.
        pseudo = _RE_PSEUDO.search(window) is not None

        if _RE_FAMILY.search(pre):
            return Assertion.FAMILY
        if _RE_HYPO.search(pre) or _RE_HYPO.search(post):
            return Assertion.HYPOTHETICAL
        if not pseudo and (_RE_PRE_NEG.search(pre) or _RE_POST_NEG.search(post)):
            return Assertion.NEGATED
        if _RE_HIST.search(pre):
            return Assertion.HISTORICAL
        return Assertion.AFFIRMED

    # -- public --------------------------------------------------------------

    def match(self, text: str, keep_spans: bool = False) -> tuple[MatchSummary, list[Match]]:
        """Find and classify every concept mention in one note."""
        summary = MatchSummary()
        spans: list[Match] = []
        if not text:
            return summary, spans

        lowered = text.lower()
        raw = self._raw_matches(lowered)
        if not raw:
            return summary, spans

        sents = split_sentences(lowered)
        sections = section_spans(text) if self.use_sections else []

        # Walk sentences and matches together; both are sorted, so this is linear
        # rather than a per-match search.
        raw.sort(key=lambda r: r[0])
        si = 0
        for start, end, surface in raw:
            while si < len(sents) and sents[si][1] <= start:
                si += 1
            if si >= len(sents):
                s_start, s_end = 0, len(lowered)
            else:
                s_start, s_end = sents[si]
                if start < s_start:
                    s_start, s_end = 0, len(lowered)

            sent = lowered[s_start:s_end]
            assertion = self._assert_at(sent, start - s_start, end - s_start)

            # A section header overrides only an otherwise-affirmed mention;
            # an explicit in-sentence negation is more specific than the header.
            if assertion is Assertion.AFFIRMED:
                for sec_s, sec_e, sec_label in sections:
                    if sec_s <= start < sec_e:
                        assertion = sec_label
                        break

            for cid in self.surface_to_ids[surface]:
                summary.bucket(assertion)[cid] += 1
                if keep_spans:
                    spans.append(Match(cid, surface, start, end, assertion, sent))

        return summary, spans

    def present_concepts(self, text: str) -> set[str]:
        """Concepts with >=1 affirmed mention — the supervision signal."""
        return self.match(text)[0].present()
