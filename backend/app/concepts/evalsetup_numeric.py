"""`numeric_map_for`, lifted verbatim from ShifaMind-MoE
`shifamind/concepts/evalsetup.py:186`. Only this function is needed at serving
time; the rest of evalsetup is training and evaluation scaffolding.
"""

from __future__ import annotations


def numeric_map_for(bank: dict[str, dict]) -> dict[str, list[str]]:
    """Map each numeric concept name onto the bank ids that carry it."""
    from .bank import normalize_name
    from .numeric import concept_names
    want = {normalize_name(c): c for c in concept_names()}
    out: dict[str, list[str]] = {}
    for cid, v in bank.items():
        c = want.get(normalize_name(v["name"]))
        if c:
            out.setdefault(c, []).append(cid)
    return out
