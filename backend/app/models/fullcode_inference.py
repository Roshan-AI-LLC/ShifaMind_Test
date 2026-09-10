"""Full-code inference: note in, ranked codes with their evidence out.

The response is the product. A code without its concepts is what every other
ICD coder already returns; the per-concept decomposition is the thing ShifaMind
exists to provide, so it is assembled here rather than left to the caller.

Tokenizer settings are pinned to `14_tokenise_cache.py`: the same `text_light`
string the router consumes, `add_special_tokens=True`, `truncation=True`,
`max_length=6144`, no padding. The router and the encoder must see the same
text or the gates describe a different note than the logits do.

Attribution is exact, not approximate. `ShifaMindMoE.contributions` asserts that
the per-concept terms plus the bias reconcile to the predicted logit and raises
if they do not. That assertion is deliberately left enabled in production: an
explanation that does not add up is worse than no explanation, and a clinician
has no way to notice it.
"""

from __future__ import annotations

import logging
import os
import threading
import time
from collections import defaultdict

import numpy as np

from .fullcode import fullcode_state
from .router import light_text

logger = logging.getLogger(__name__)

#: Concepts listed per predicted code. Ranked by |contribution|, so the strongest
#: support and the strongest objection both surface.
TOP_CONCEPTS_PER_CODE = 8

#: A concept whose gate closes below this was found in the note and then
#: SUPPRESSED by the model. Measured on real notes, the gate is sharply bimodal:
#: affirmed mentions sit at ~0.99 and negated ones at ~0.00, with 13-24% of every
#: note's routed slots landing in the closed group. 0.5 sits in the empty middle.
GATE_CLOSED = 0.5

#: Codes returned when nothing clears the threshold, so the UI can still show a
#: ranked list and say "nothing met the bar".
FALLBACK_TOP_N = 10

#: ONE forward at a time. A single request peaks around 4.2 GB of RSS on an
#: ~2,900-token note, so two concurrent requests on an 8 GiB box is 8.4 GB and
#: the kernel kills the container. Queueing the second request costs a second
#: of latency; not queueing it costs the process. Raise MAX_CONCURRENCY only
#: after measuring peak RSS on the box it will run on.
MAX_CONCURRENCY = int(os.environ.get("MAX_CONCURRENCY", "1"))
#: How long a queued request waits before giving up with a clean 503 rather
#: than piling up until something else breaks.
QUEUE_TIMEOUT_S = float(os.environ.get("QUEUE_TIMEOUT_S", "120"))

_slots = threading.BoundedSemaphore(MAX_CONCURRENCY)


class ModelBusy(RuntimeError):
    """All inference slots are occupied. Map this to HTTP 503 + Retry-After."""


def predict(text: str, threshold: float | None = None,
            top_concepts: int = TOP_CONCEPTS_PER_CODE) -> dict:
    import torch

    s = fullcode_state
    if not s["loaded"]:
        raise RuntimeError("full-code model is not loaded")

    if not _slots.acquire(timeout=QUEUE_TIMEOUT_S):
        raise ModelBusy(
            f"all {MAX_CONCURRENCY} inference slot(s) busy for "
            f"{QUEUE_TIMEOUT_S:.0f}s")
    try:
        return _predict_locked(text, threshold, top_concepts)
    finally:
        _slots.release()


def _predict_locked(text: str, threshold: float | None,
                    top_concepts: int) -> dict:
    import torch

    s = fullcode_state
    model, tok, router = s["model"], s["tokenizer"], s["router"]
    device = s["device"]
    thr = float(threshold if threshold is not None else s["threshold"])
    t0 = time.perf_counter()

    light = light_text(text)
    routed = router.route(text, keep_spans=True)

    enc = tok(light, add_special_tokens=True, truncation=True,
              max_length=model.cfg.max_len, padding=False,
              return_tensors="pt")

    # A note that routes nothing still has to produce a prediction: one dead
    # slot with a zero mask. The label attention masks it out and nan_to_num
    # turns the all -inf softmax into zeros, so the model falls back to its
    # per-code prior bias. That is the correct behaviour, not an error.
    if routed.concept_ids.size:
        cids = torch.from_numpy(routed.concept_ids).long().unsqueeze(0)
        cmask = torch.ones_like(cids)
    else:
        cids = torch.zeros((1, 1), dtype=torch.long)
        cmask = torch.zeros((1, 1), dtype=torch.long)

    batch = {
        "input_ids": enc["input_ids"].to(device),
        "attention_mask": enc["attention_mask"].to(device),
        "concept_ids": cids.to(device),
        "concept_mask": cmask.to(device),
    }

    with torch.no_grad():
        out = model(**batch, explain=True)

    logits = out["logits"][0].float()
    probs = torch.sigmoid(logits)
    gates = out["gate"][0].float().cpu().numpy()

    picked = (probs > thr).nonzero(as_tuple=True)[0]
    fell_back = picked.numel() == 0
    if fell_back:
        picked = torch.topk(probs, min(FALLBACK_TOP_N, probs.numel())).indices

    order = picked[torch.argsort(probs[picked], descending=True)]

    # spans grouped by concept, so a concept mentioned three times shows all three
    spans_by_concept: dict[str, list[dict]] = defaultdict(list)
    for m in routed.spans:
        spans_by_concept[m["concept"]].append(
            {"start": m["start"], "end": m["end"],
             "surface": m["surface"], "assertion": m["assertion"]})

    codes = []
    for idx in order.tolist():
        code = s["label_vocab"][idx]
        meta = (s["code_titles"] or {}).get(code, {})
        entry = {
            "code": code,
            "title": meta.get("title", ""),
            "kind": meta.get("kind", ""),
            "probability": float(probs[idx]),
            "above_threshold": bool(float(probs[idx]) > thr),
            "concepts": [],
        }

        if routed.concept_ids.size:
            # Exact decomposition. Raises if the terms do not reconcile.
            d = model.contributions(out, idx, top_n=min(top_concepts, routed.concept_ids.size))
            contrib = d["contrib"][0].float().cpu().numpy()
            top_slots = d["top_idx"][0].cpu().numpy()
            for slot in top_slots:
                slot = int(slot)
                cidx = int(routed.concept_ids[slot])
                cid = router.concept_ids[cidx]
                entry["concepts"].append({
                    "concept": cid,
                    "name": router.names[cidx],
                    "contribution": float(contrib[slot]),   # signed
                    "gate": float(gates[slot]),
                    "spans": spans_by_concept.get(cid, []),
                })
            # .detach(): contributions() is @torch.no_grad but label_out.bias
            # is still a leaf with requires_grad, and float() warns on it.
            entry["bias"] = float(d["bias"].detach())
            entry["recon_error"] = d["recon_error"]
        codes.append(entry)

    # Concepts the note MENTIONS and the model then SHUTS OFF. These never
    # appear in the per-code lists, because a closed gate contributes ~0 and so
    # can never rank in a top-N by contribution. That makes them invisible
    # exactly when they are most interesting: "denies chest pain" being
    # correctly suppressed is something a black-box coder cannot show at all.
    suppressed = []
    if routed.concept_ids.size:
        for slot, cidx in enumerate(routed.concept_ids):
            g = float(gates[slot])
            if g >= GATE_CLOSED:
                continue
            cid = router.concept_ids[int(cidx)]
            spans = spans_by_concept.get(cid, [])
            suppressed.append({
                "concept": cid,
                "name": router.names[int(cidx)],
                "gate": g,
                "spans": spans,
                # Why the matcher thought it was not asserted.
                "assertion": spans[0]["assertion"] if spans else None,
            })
        suppressed.sort(key=lambda c: c["gate"])

    grounding = model.grounding_split(out, threshold=thr)

    return {
        "codes": codes,
        "threshold": thr,
        "no_code_met_threshold": fell_back,
        "routing": {
            "concepts_matched": routed.n_matched,
            "concepts_routed": int(routed.concept_ids.size),
            "concepts_suppressed": len(suppressed),
            "truncated": routed.truncated,
            "top_k": model.cfg.top_k,
        },
        "suppressed": suppressed,
        "tokens": int(enc["input_ids"].shape[1]),
        "truncated_note": bool(enc["input_ids"].shape[1] >= model.cfg.max_len),
        # 1.0 under strict composition, by construction. Reported anyway so a
        # regression to a bypassing config is visible in the response itself.
        "concept_share": grounding.get("concept_share"),
        "model": {"tag": s["tag"], "seed": s["seed"], "compose": "strict"},
        "latency_ms": round((time.perf_counter() - t0) * 1000, 1),
    }


def summarise(result: dict) -> str:
    """One-line log summary. Kept out of the response body."""
    r = result["routing"]
    n = sum(1 for c in result["codes"] if c["above_threshold"])
    return (f"{n} codes >= {result['threshold']:.2f}, "
            f"{r['concepts_routed']}/{r['concepts_matched']} concepts routed"
            f", {r['concepts_suppressed']} suppressed"
            f"{' (truncated)' if r['truncated'] else ''}, "
            f"{result['tokens']} tokens, {result['latency_ms']}ms")
