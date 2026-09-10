"""Numeric-value concepts: the evidence string matching throws away.

A discharge summary does not usually say "hyperkalemia". It says "K 6.2". It does
not say "reduced ejection fraction", it says "EF 25%". Our Aho-Corasick matcher
is literal, so every one of those mentions is invisible to the bank — and they
are not incidental, they are frequently *the* documented evidence for the code.

The obvious fix — add "EF" and "creatinine" as surface forms — makes things
worse, not better. Those fire on almost every note regardless of the value, so
they are constant features that carry no signal. What matters is the number
relative to a clinical threshold, which is why this needs a rule with a
comparison in it rather than another string in the bank.

Each rule extracts the value and emits a concept only when the value is outside
the reference range, so ``creatinine high`` fires on "Cr 3.1" and stays silent on
"Cr 0.9". Thresholds below are conventional adult reference limits; they are a
knob, not a claim, and ``--numeric-off`` disables the whole pass.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# A number, optionally decimal, not glued to a word character.
_V = r"(\d{1,3}(?:\.\d{1,2})?)"
# Connective between the analyte and its value. Clinicians rarely write the bare
# pair: "troponin peaked at 0.9", "Cr bumped to 3.1", "K trending down to 3.0".
# A closed list of connective verbs, capped at three, keeps that flexibility
# without letting the value hop across a conjunction — "creatinine and potassium
# 6.2" must not be read as a creatinine of 6.2, so `and`/`,` are deliberately
# absent from the list.
_LINK = (r"of|is|was|were|are|to|at|up|down|now|has|had|been|"
         r"peaked?|peaking|rose|rising|risen|bumped|trending|trended|"
         r"increased|decreased|elevated|dropped|fell|fallen|remains?|"
         r"stable|max|min|today|from|noted|measured|level|value")
_C = rf"(?:\s*(?:{_LINK})\b){{0,3}}\s*(?:[:=-]\s*)?\s*"


@dataclass(frozen=True)
class NumericRule:
    """One analyte, its pattern, and the range outside which it means something.

    ``low``/``high`` are exclusive bounds. A rule with only ``high`` set emits
    just the ``high`` concept; values inside the range emit nothing at all, which
    is the point — a normal potassium is not evidence for anything.
    """
    name: str            # concept stem, e.g. "potassium"
    category: str        # lab | vital | imaging | index
    pattern: str         # must contain exactly one capture group: the value
    low: float | None = None
    high: float | None = None
    low_name: str | None = None    # override, e.g. "hypokalemia"
    high_name: str | None = None

    def concept_low(self) -> str:
        return self.low_name or f"{self.name} low"

    def concept_high(self) -> str:
        return self.high_name or f"{self.name} high"


# Reference limits are the conventional adult ranges. Where a code boundary is
# what actually matters (EF < 40 for HFrEF, A1c >= 6.5 for diabetes) the
# clinically meaningful cut is used rather than the lab's flag range.
RULES: tuple[NumericRule, ...] = (
    # --- chemistry ---
    NumericRule("potassium", "lab",
                rf"\b(?:potassium|k\+?){_C}{_V}\b", 3.5, 5.2,
                "hypokalemia", "hyperkalemia"),
    NumericRule("sodium", "lab",
                rf"\b(?:sodium|na\+?){_C}{_V}\b", 135, 145,
                "hyponatremia", "hypernatremia"),
    NumericRule("creatinine", "lab",
                rf"\b(?:creatinine|creat|cr){_C}{_V}\b", None, 1.3,
                None, "creatinine elevated"),
    NumericRule("bun", "lab", rf"\b(?:bun){_C}{_V}\b", None, 25),
    NumericRule("egfr", "lab", rf"\b(?:e?gfrs?){_C}{_V}\b", 60, None,
                "gfr reduced", None),
    NumericRule("bicarbonate", "lab",
                rf"\b(?:bicarb(?:onate)?|hco3){_C}{_V}\b", 22, 29),
    NumericRule("glucose", "lab", rf"\b(?:glucose|bg|fsbs){_C}{_V}\b", 70, 200,
                "hypoglycemia", "hyperglycemia"),
    NumericRule("hba1c", "lab", rf"\b(?:hba1c|a1c|hgba1c){_C}{_V}\b", None, 6.5,
                None, "hemoglobin a1c elevated"),
    NumericRule("calcium", "lab", rf"\b(?:calcium|ca){_C}{_V}\b", 8.5, 10.5,
                "hypocalcemia", "hypercalcemia"),
    NumericRule("magnesium", "lab", rf"\b(?:magnesium|mag|mg){_C}{_V}\b", 1.7, 2.4,
                "hypomagnesemia", "hypermagnesemia"),
    NumericRule("phosphate", "lab", rf"\b(?:phos(?:phate|phorus)?){_C}{_V}\b", 2.5, 4.5),
    NumericRule("albumin", "lab", rf"\b(?:albumin|alb){_C}{_V}\b", 3.5, None,
                "hypoalbuminemia", None),
    NumericRule("bilirubin", "lab", rf"\b(?:bili(?:rubin)?|tbili){_C}{_V}\b", None, 1.2,
                None, "hyperbilirubinemia"),
    NumericRule("alt", "lab", rf"\b(?:alt|sgpt){_C}{_V}\b", None, 55),
    NumericRule("ast", "lab", rf"\b(?:ast|sgot){_C}{_V}\b", None, 48),
    NumericRule("lipase", "lab", rf"\b(?:lipase){_C}{_V}\b", None, 160),

    # --- haematology / coagulation ---
    NumericRule("hemoglobin", "lab",
                rf"\b(?:h(?:emoglobin|gb|b)){_C}{_V}\b", 12.0, 17.5,
                "anemia by hemoglobin", None),
    NumericRule("hematocrit", "lab", rf"\b(?:h(?:ematocrit|ct)){_C}{_V}\b", 36, 50),
    NumericRule("platelets", "lab", rf"\b(?:platelets?|plt){_C}{_V}\b", 150, 450,
                "thrombocytopenia", "thrombocytosis"),
    NumericRule("wbc", "lab", rf"\b(?:wbc|white count|leukocytes?){_C}{_V}\b", 4.0, 11.0,
                "leukopenia", "leukocytosis"),
    NumericRule("inr", "lab", rf"\b(?:inr){_C}{_V}\b", None, 1.2,
                None, "inr elevated"),

    # --- cardiac / sepsis markers ---
    NumericRule("troponin", "lab", rf"\b(?:troponins?|trops?|ctni?){_C}{_V}\b", None, 0.04,
                None, "troponin elevated"),
    NumericRule("bnp", "lab", rf"\b(?:nt-?pro-?bnp|pro-?bnp|bnp){_C}{_V}\b", None, 100,
                None, "bnp elevated"),
    NumericRule("lactate", "lab", rf"\b(?:lactates?|lactic acid){_C}{_V}\b", None, 2.0,
                None, "lactate elevated"),

    # --- imaging / index ---
    NumericRule("ejection fraction", "imaging",
                rf"\b(?:lv\s*ef|lvef|ef|ejection fraction){_C}{_V}\s*(?:%|percent)",
                50, None, "reduced ejection fraction", None),
    NumericRule("bmi", "index", rf"\b(?:bmi){_C}{_V}\b", 18.5, 30.0,
                "underweight by bmi", "obesity by bmi"),

    # --- vitals / gas ---
    NumericRule("ph", "lab", rf"\b(?:ph){_C}(7\.\d{{1,2}})\b", 7.35, 7.45,
                "acidemia", "alkalemia"),
    NumericRule("pco2", "lab", rf"\b(?:p?a?co2){_C}{_V}\b", 35, 45),
    NumericRule("oxygen saturation", "vital",
                rf"\b(?:spo2|o2\s*sats?|sats?|oxygen saturation){_C}{_V}\s*%?", 90, None,
                "hypoxemia by saturation", None),
    NumericRule("systolic blood pressure", "vital",
                rf"\b(?:sbp|systolic){_C}{_V}\b", 90, 160,
                "hypotension by sbp", "hypertension by sbp"),
    NumericRule("heart rate", "vital", rf"\b(?:hr|heart rate|pulse){_C}{_V}\b", 60, 100,
                "bradycardia by rate", "tachycardia by rate"),
    NumericRule("temperature", "vital",
                rf"\b(?:t(?:emp)?(?:max|m)?){_C}(1\d{{2}}\.\d|\d{{2}}\.\d)\b",
                None, 100.4, None, "fever by temperature"),
    NumericRule("respiratory rate", "vital", rf"\b(?:rr|resp rate){_C}{_V}\b", 12, 20,
                None, "tachypnea by rate"),
)


def concept_names() -> dict[str, NumericRule]:
    """Every concept these rules can emit, mapped back to its rule."""
    out: dict[str, NumericRule] = {}
    for r in RULES:
        if r.low is not None:
            out[r.concept_low()] = r
        if r.high is not None:
            out[r.concept_high()] = r
    return out


def compile_rules(rules: tuple[NumericRule, ...] = RULES):
    """``[(compiled, rule)]``, validated to expose exactly one value group."""
    out = []
    for r in rules:
        rx = re.compile(r.pattern, re.IGNORECASE)
        if rx.groups != 1:
            raise ValueError(
                f"numeric rule {r.name!r} must have exactly one capture group "
                f"(the value); it has {rx.groups}")
        out.append((rx, r))
    return out


def evaluate(rule: NumericRule, raw: str) -> str | None:
    """Concept name for this observed value, or None when it is unremarkable."""
    try:
        v = float(raw)
    except (TypeError, ValueError):
        return None
    if rule.low is not None and v < rule.low:
        return rule.concept_low()
    if rule.high is not None and v > rule.high:
        return rule.concept_high()
    return None
