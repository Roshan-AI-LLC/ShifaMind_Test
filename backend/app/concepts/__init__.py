"""Vendored, byte-for-byte, from ShifaMind-MoE `shifamind/concepts/`.

These files are COPIES, not a reimplementation. The routing they produce has to
match training exactly: a router that differs by two surface forms in a hundred
notes still lands inside 0.001 micro-F1 while showing a clinician gate values
that are wrong. Do not "clean up" anything in here. If the training repo
changes, re-copy and re-run the parity harness.

Source commit fingerprint: bank d4493a6f55b4 (merged_umls, 16,227 concepts).
"""

from .bank import canonicalize, normalize_name, surface_map
from .negex import Assertion, ConceptMatcher, Match, MatchSummary

__all__ = ["Assertion", "ConceptMatcher", "Match", "MatchSummary",
           "canonicalize", "normalize_name", "surface_map"]
