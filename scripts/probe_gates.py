#!/usr/bin/env python3
"""Is the concept gate actually discriminative, or is it saturated open?

The claim under test: the gate is supposed to encode "this concept is ASSERTED
in this note" versus "this concept is DENIED". Training supervises it with a
binary cross-entropy against assertion-derived targets, and routing deliberately
admits negated mentions so the gate has something to discriminate. If that
worked, negated mentions should carry visibly lower gates than affirmed ones.

An earlier read of the UI suggested every gate sat at 1.00, but that view only
showed concepts that made a per-code top-8 list, which selects for strong ones.
This looks at ALL routed slots, and splits them by the assertion class the
matcher assigned, which is the comparison that actually answers the question.

    python scripts/probe_gates.py --artifacts artifacts/fullcode --out gate_probe.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


class Settings:
    def __init__(self, artifacts: Path, device: str):
        self.MODEL_SOURCE = "local"
        self.LOCAL_FULLCODE_DIR = str(artifacts)
        self.DEVICE = device
        self.THRESHOLD = 0


def pct(a, q):
    return float(np.percentile(a, q)) if len(a) else float("nan")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifacts", default="artifacts/fullcode")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--limit", type=int, default=4)
    ap.add_argument("--out", default="gate_probe.json")
    args = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(root / "backend"))
    sys.path.insert(0, str(root / "scripts"))

    import torch

    from app.models.fullcode import build_config, fullcode_state, load_fullcode
    from app.models.router import light_text

    print("loading model...")
    load_fullcode(Settings(Path(args.artifacts), args.device))
    model, tok, router = (fullcode_state["model"], fullcode_state["tokenizer"],
                          fullcode_state["router"])
    vocab, titles = fullcode_state["label_vocab"], fullcode_state["code_titles"]
    cfg = build_config()
    print(f"compose={cfg.compose} experts={cfg.experts} width={cfg.concept_width}\n")

    # A medical note and three operative ones, so procedures are represented.
    notes = []
    seed = json.loads((root / "scripts" / "sample_notes_seed.json").read_text())
    notes.append(("MIMIC sample 0", seed[0]["text"]))
    from sample_notes_extra import EXTRA_NOTES
    for n in EXTRA_NOTES[:3]:
        notes.append((n["category"], n["text"]))
    notes = notes[: args.limit]

    report = {"config": {"compose": cfg.compose, "experts": cfg.experts,
                         "concept_width": cfg.concept_width,
                         "gate_act": cfg.gate_act, "w_sparse": cfg.w_sparse},
              "notes": []}

    for name, text in notes:
        light = light_text(text)
        routed = router.route(text, keep_spans=True)
        enc = tok(light, add_special_tokens=True, truncation=True,
                  max_length=cfg.max_len, padding=False, return_tensors="pt")
        cids = torch.from_numpy(routed.concept_ids).long().unsqueeze(0)
        with torch.no_grad():
            out = model(input_ids=enc["input_ids"], attention_mask=enc["attention_mask"],
                        concept_ids=cids, concept_mask=torch.ones_like(cids),
                        explain=True)

        gates = out["gate"][0].float().numpy()
        probs = torch.sigmoid(out["logits"][0].float()).numpy()

        # assertion class per concept: what the matcher tagged its mentions as
        by_concept = defaultdict(Counter)
        for m in routed.spans:
            by_concept[m["concept"]][m["assertion"]] += 1

        buckets = defaultdict(list)
        for slot, cidx in enumerate(routed.concept_ids):
            cid = router.concept_ids[int(cidx)]
            counts = by_concept.get(cid)
            if not counts:
                buckets["unmatched"].append(float(gates[slot])); continue
            # a concept whose mentions are ALL negated is the clean test case
            if set(counts) == {"negated"}:
                buckets["negated_only"].append(float(gates[slot]))
            elif set(counts) == {"affirmed"}:
                buckets["affirmed_only"].append(float(gates[slot]))
            else:
                buckets["mixed"].append(float(gates[slot]))

        g = np.asarray(gates)
        entry = {
            "note": name,
            "routed": int(g.size),
            "tokens": int(enc["input_ids"].shape[1]),
            "gate_all": {"min": float(g.min()), "p10": pct(g, 10), "p50": pct(g, 50),
                         "p90": pct(g, 90), "max": float(g.max()),
                         "frac_above_0.99": float((g > 0.99).mean()),
                         "frac_below_0.50": float((g < 0.50).mean())},
            "gate_by_assertion": {
                k: {"n": len(v), "mean": float(np.mean(v)), "p50": pct(np.asarray(v), 50),
                    "min": float(np.min(v)), "max": float(np.max(v))}
                for k, v in buckets.items() if v},
            "codes_above_0.3": int((probs > 0.3).sum()),
            "top_codes": [
                {"code": vocab[i], "title": titles.get(vocab[i], {}).get("title", ""),
                 "p": round(float(probs[i]), 4)}
                for i in np.argsort(-probs)[:8]],
        }
        report["notes"].append(entry)

        print(f"--- {name}: {entry['routed']} slots, {entry['tokens']} tokens")
        ga = entry["gate_all"]
        print(f"    gate  min {ga['min']:.3f}  p10 {ga['p10']:.3f}  p50 {ga['p50']:.3f}"
              f"  p90 {ga['p90']:.3f}  max {ga['max']:.3f}")
        print(f"    {ga['frac_above_0.99']*100:.1f}% above 0.99,"
              f" {ga['frac_below_0.50']*100:.1f}% below 0.50")
        for k, v in entry["gate_by_assertion"].items():
            print(f"    {k:15} n={v['n']:4}  mean {v['mean']:.3f}  median {v['p50']:.3f}"
                  f"  range {v['min']:.3f}-{v['max']:.3f}")
        print()

    Path(args.out).write_text(json.dumps(report, indent=2))
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
