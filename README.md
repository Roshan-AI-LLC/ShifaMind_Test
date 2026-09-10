# ShifaMind Platform

Authenticated clinical coding platform. A doctor pastes a discharge note and
gets ICD-10 codes back — each one accompanied by the clinical concepts that
produced it, every concept carrying a signed contribution and the character
spans in the note that fired it.

**Live:** `platform.roshan-ai.com/shifamind` (Netlify) · API `api.roshan-ai.com`
(Cloudflare → EC2 nginx → container :8000) · Auth/DB Supabase

## The model

Full-code ShifaMind, tag `w768_honest`, seed 10.

| | |
|---|---|
| Codes | 7,940 ICD-10 (5,802 CM + 2,138 PCS) |
| Concepts | 16,227, of which 384 are routed per note |
| Encoder | BioClinical-ModernBERT-base, 6,144 tokens |
| Composition | `strict` — no residual bypass |
| Threshold | 0.3, selected on validation, never tuned on test |

`compose="strict"` is the load-bearing choice. There is no residual path, so
`logit = bias + Σ concept contributions` exactly, and the model asserts that
reconciliation on every call rather than trusting it. A prediction whose
explanation does not add up is refused, because a clinician cannot detect that
from the output and an unverifiable explanation is worse than none.

The serving code in `backend/app/models/` is vendored byte-for-byte from the
training repo, with provenance in each file's header. Reimplementing it would
let serving and training drift, and the failure mode is plausible codes with
meaningless attribution.

## Layout

```
backend/app/
  models/      mcb.py, explain.py (vendored), fullcode*.py, router.py
  concepts/    Aho-Corasick matcher, ConText assertions, numeric rules
  routers/     predict, health, notes, chat, reviews, admin
frontend/      Next.js 16, Supabase auth
infra/         Dockerfile.backend, deploy_remote_build.sh, sync_env_keys.sh
scripts/       parity, smoke, seeding, diagnostics
supabase/      migrations
```

## Running locally

```bash
python -m venv .venv-serve && .venv-serve/bin/pip install -r backend/requirements.txt
.venv-serve/bin/uvicorn backend.app.main:app --reload    # from the repo root

cd frontend && npm run dev:local
```

`dev:local`, not `dev`. `.env` holds the PRODUCTION `NEXT_PUBLIC_API_URL`, so
plain `next dev` points the browser at the deployed box and every local backend
change is silently ignored. This cost hours once; see FULLCODE_DEPLOY.md
Phase 3.4.

## Deploying

```bash
export EC2_HOST=52.20.157.176 EC2_USER=ubuntu SSH_KEY="…/shifamind-key.pem"
./infra/deploy_remote_build.sh
```

Builds on the box. The dev Mac is arm64 and EC2 is x86_64, and cross-building
torch under QEMU is far slower than a native build on the instance's own cores.
The script tags the running image `previous` before replacing it.

Artifacts come from `s3://shifamind-models/models/fullcode/s10/` via the
instance role, cached under `/var/lib/shifamind/fullcode` on a mounted volume.
No AWS keys live on the box.

Full runbook: **FULLCODE_DEPLOY.md**. Domain and cutover: **GO_LIVE.md**.

## Checks

```bash
python scripts/parity_router.py                  # router matches training, byte for byte
python scripts/smoke_fullcode.py                 # checkpoint loads, attribution reconciles
python scripts/smoke_api.py --url … --email …    # the deployed service, end to end
python scripts/diag_history.py <email> <pass>    # why a prediction did not persist
```

`smoke_api.py` checks more than HTTP 200: no empty code lists, no code outside
the vocabulary, every code carrying at least one concept with a real span, and
`concept_share == 1.0`. The span check is the important one — a code we cannot
point at a quoted span for defeats the purpose of the system.
