# Full-code deploy runbook — ShifaMind w768_honest (seed 10)

Replaces the live 50-code / 111-concept model with the full-code model:
7,940 ICD-10 codes, 16,227 concepts, 384 routed slots per note.

## Folders

| folder | role |
|---|---|
| `ShifaMind_Prod/shifamind_test` | **this repo.** The deploy target |
| `Personal/Code Repos/shifamind_released` | read-only. Weights, vocab, concept bank |
| `Claude/Projects/ShifaMind-MoE/MoE` | read-only. Model class, router |

---

## Phase 0 — Locked decisions

- [x] Model: `w768_honest_best.pt`, seed 10, 6 epochs, `compose="strict"`
- [x] Rejected: `lic8` (licensed compose = residual bypass, breaks the 100%
      attribution claim, despite the best macro-F1 in the table),
      `e8_s10` and `w16h8` (8 epochs is worse on every metric)
- [x] Threshold: **0.3** default, validation-selected, set by `THRESHOLD` env
      var so it changes without a rebuild. 0.5 for precision-first. Not 0.1
- [x] No side-by-side containers. Two model copies will not fit in RAM.
      Rollback is the tagged previous image, see Phase 5
- [x] S3 layout, new keys, old keys untouched:
      ```
      s3://<bucket>/models/fullcode/s10/model.pt
      s3://<bucket>/models/fullcode/s10/thresholds.json
      s3://<bucket>/models/fullcode/s10/label_vocab.json
      s3://<bucket>/models/fullcode/s10/concept_bank.jsonl
      s3://<bucket>/models/fullcode/s10/concept_queries.npy
      ```

**MCBConfig — pin every field, inherit no defaults.** The class defaults
`n_concepts` to 16,245; the artifacts are 16,227. From
`RELEASED/w768_honest_log.jsonl` line 0:

```
n_concepts 16227   n_labels 7940    hidden 768      top_k 384
concept_width 768  concept_layers 1 label_heads 1   label_attn softmax
gate concept       gate_tied True   gate_act sigmoid
compose strict     experts none     hier False      max_len 6144
backbone thomas-sounack/BioClinical-ModernBERT-base
```

---

## Phase 1 — Port the serving code (DONE)

- [x] `ShifaMindMoE` + `MCBConfig` vendored to `backend/app/models/mcb.py`
- [x] Attribution vendored to `backend/app/models/explain.py`
- [x] Concept router ported: `backend/app/models/router.py` +
      `backend/app/concepts/` (negex, numeric, bank, evalsetup_numeric)
- [x] `backend/app/models/fullcode.py` — every MCBConfig field pinned,
      `use_residual` DERIVED from compose the way `16_train.py:714` does
- [x] `backend/app/models/fullcode_inference.py` — signed contributions, spans,
      assertion status, one-forward-at-a-time semaphore
- [x] `POST /api/predict` rewritten; `GET /api/health/model` added
- [x] 50-code model deleted entirely: loader, inference, phase1_model,
      model/ dir, MODEL_VARIANT, and every top50 setting
- [x] Frontend: real per-code evidence instead of the same global top-3
      concepts pinned to every prediction. `next build` clean
- [x] Artifacts cache to `FULLCODE_CACHE_DIR` between boots, size-verified,
      `.part` + atomic rename
- [x] Dockerfile bakes the backbone in, `TRANSFORMERS_OFFLINE=1`
- [x] Requirements resolve and import together (httpx 0.25.2 with
      huggingface_hub 1.30.0 verified, not assumed)

---

## Phase 2 — Parity

### 2a — Router parity (PASSED)

`scripts/parity_router.py`, reference side re-runs the training path.

- [x] top_k 384: 10 notes, 2,299 slots, arrays identical (CSR ascending path)
- [x] top_k 50: 10 notes, 500 slots, arrays identical (lexsort tie-break path)
- [x] `light_text` byte-identical to `LIGHT_PREPROCESSOR`

Both branches matter. Every sample note routes under 384, so the first run
never exercised the lexsort at all; `--top-k 50` forces it.

### 2b — Model behaviour (PASSED on 10 notes)

`scripts/smoke_fullcode.py`:

- [x] `load_state_dict(strict=True)` — caught `use_residual` being wrong
- [x] attribution reconciles on every note
- [x] `concept_share` 1.0000 on every note, strict composition confirmed
- [x] peak RSS 4,175 MB, latency p50 939 / p95 1,242 / max 1,340 ms
- [ ] **Metric parity still open**: micro-F1 0.5970 / macro-F1 0.2579 on the
      full test split. Needs the MIMIC test notes plus gold labels, which the
      10 bundled samples cannot provide

---

## Phase 2c — Local end to end (DONE)

- [x] Supabase migrated to a new project, 3 migrations applied, 6 tables
- [x] 27 sample notes seeded (21 original + 6 new operative templates),
      15 demo doctors, 1 real admin account
- [x] Backend serving on localhost:8000, model loads, auth works
- [x] Real prediction through the UI: 14 codes, evidence panel renders signed
      contributions, matched spans and assertion status
- [x] Procedure codes confirmed reaching the UI (PCS), which the 50-code model
      could not emit at all
- [x] `inference_time_ms` INT-vs-float bug fixed; persist failures now log at
      ERROR so they cannot hide again
- [ ] **Confirm history actually persists** after the fix (one prediction,
      then check /dashboard/history)

### Gate discrimination — MEASURED, not assumed

`scripts/probe_gates.py`, all 384 routed slots per note, split by the assertion
class the matcher assigned. Four notes, 141 negated slots:

| note | affirmed gate | negated gate |
|---|---|---|
| MIMIC sample 0 | 0.996 | 0.008 |
| Colorectal Surgery | 1.000 | 0.000 |
| Surgical Oncology | 0.990 | 0.045 |
| Orthopedic Surgery | 0.994 | 0.000 |

The gate is sharply bimodal and separates asserted from denied almost cleanly.
13-24% of every note's slots close below 0.50. This is the measurement behind
"the number displayed is the number applied", and it is worth having in the
paper. Full distributions in `gate_probe.json`.

Consequence for the product: suppressed concepts are now returned by the API
and shown in the Concepts tab. They can never appear in a per-code top-N,
because a closed gate contributes ~0, so the most auditable thing the model
does was previously invisible.

---

## Phase 3.4 — Local testing points at the OLD server (RESOLVED)

Symptom: predictions returned fine in the UI, the `predictions` table in the
new Supabase project stayed empty, and Prediction History showed 0. Several
rounds went into auditing RLS, column types and the persist call. All of it was
fine. `scripts/diag_history.py` proved it: signing in as the doctor and making
the byte-identical insert returned HTTP 201, and reading it back returned the
row.

Cause: `NEXT_PUBLIC_API_URL=https://api.roshan-ai.com` in `.env`. The browser
was talking to the old EC2 box — old 50-code build, old Supabase project —
while the history page read the NEW project. Nothing was ever wrong with the
new backend; it was never being called.

The tell was in the uvicorn log and nowhere else: no `POST /api/predict` line,
only `Application startup complete` and two DevTools 404s (`GET /` and
`GET /json/version`). **Check the backend log for the request before auditing
what the request does.**

Fix: `npm run dev:local` in `frontend/` (added to package.json). It exports
`NEXT_PUBLIC_API_URL=http://localhost:8000`, which `next.config.mjs` prefers
over `.env` (`process.env[k] || parentEnv[k]`). `.env` keeps the production
host so Netlify is unaffected. `NEXT_PUBLIC_*` is inlined at startup, so the
dev server must be restarted, not reloaded.

At Phase 7 cutover, `.env`'s `NEXT_PUBLIC_API_URL` becomes correct again once
the new image is serving `api.roshan-ai.com`. Until then, every local test must
use `dev:local` or it silently exercises the old model.

Also fixed while here:
- `SUPABASE_ANON_KEY` in `.env` was the literal placeholder `sb_publishable_...`.
  Harmless, because `config.py` reads `NEXT_PUBLIC_SUPABASE_ANON_KEY`, but it
  sent the first diagnostic run down a false path. Both names now hold the key.
- `_persist()` serialises with a numpy-aware encoder and logs
  `persist <id>: HTTP <code>` on every call, not only on failure. Silence in
  the log now means the code did not run.

---

## Phase 3.5 — BLOCKER: AWS credentials

`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are empty in `.env`. Nothing in
Phase 4 or 5 can run without them.

- [ ] Either `aws configure` locally for the S3 upload, or
- [ ] Attach an IAM role to the EC2 instance (better for the box: no long-lived
      keys on disk). The role needs `s3:GetObject` on the artifact prefix
- [ ] `aws sts get-caller-identity` to confirm which account you are in

---

## Phase 3 — Instance (RESOLVED)

Measured on the Mac, 10 real notes, CPU, `attn_implementation=eager`:

| | |
|---|---|
| resident after load | 2,115 MB |
| **peak during inference** | **4,175 MB** |
| latency p50 / p95 / max | 939 / 1,242 / 1,340 ms |
| load time (warm HF cache) | 4.8 s |

- [x] **c6i.xlarge** — 4 vCPU, 8 GiB, not burstable. t3.medium cannot hold one
      request; t3.large can but is burstable and throttles under sustained load
- [x] **Concurrency pinned to 1** (`MAX_CONCURRENCY`). Two concurrent requests
      is 8.4 GB against 8 GiB and the kernel kills the container. The second
      request now queues for up to `QUEUE_TIMEOUT_S` and then returns 503
- [ ] Re-measure peak RSS **on the box**, not the Mac. Apple silicon and Xeon
      allocate differently and the margin here is 3.8 GB, not 30 GB
- [ ] A/B the attention kernel there: `ATTN_IMPL=sdpa` against the default
      `eager`. Eager materialises the full (heads, seq, seq) matrix, which is
      where most of the 2 GB transient goes. Mathematically equivalent, so if
      sdpa is cheaper it is free headroom
- [ ] Latency on a Xeon core will be slower than 939 ms. Measure before
      quoting a number to anyone

### Cold start matters more than it looks

The server is only up for testing and demos, so **every start is a cold start**
and it happens with someone waiting. Two dependencies have to go:

- [ ] **Bake the backbone into the image.** `AutoModel.from_pretrained` pulls
      BioClinical-ModernBERT from HuggingFace on first load. Download it at
      image build time and set `HF_HOME`/`TRANSFORMERS_OFFLINE=1` so a demo
      never depends on HuggingFace being reachable
- [ ] **Cache the checkpoint on the instance volume.** Re-pulling 758 MB from
      S3 on every boot is minutes of dead air. Pull once to an EBS path and
      have the loader use it when present

## Phase 4 — Artifacts to S3 (AWS)

Credentials are already in `.env` (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`,
`AWS_DEFAULT_REGION`). Load them into your shell, do not paste them anywhere:

```bash
set -a; source .env; set +a
aws sts get-caller-identity          # confirms which account you are in
aws s3 ls "s3://$S3_BUCKET/"         # confirms the bucket and your access
```

- [ ] **Record the old keys first**, so rollback has something to point at:
      ```bash
      echo "OLD_MODEL_KEY=$S3_MODEL_KEY"
      echo "OLD_THRESHOLDS_KEY=$S3_THRESHOLDS_KEY"
      aws s3 ls "s3://$S3_BUCKET/$S3_MODEL_KEY"
      ```
- [ ] Dry run every upload before running it for real:
      ```bash
      REL="<path>/shifamind_released"
      aws s3 cp "$REL/w768_honest_best.pt" \
        "s3://$S3_BUCKET/models/fullcode/s10/model.pt" --dryrun
      ```
- [ ] Remove `--dryrun` and upload all five artifacts
- [ ] Verify size and checksum:
      ```bash
      aws s3 ls "s3://$S3_BUCKET/models/fullcode/s10/"
      shasum -a 256 "$REL/w768_honest_best.pt"
      aws s3api head-object --bucket "$S3_BUCKET" \
        --key models/fullcode/s10/model.pt --query 'ETag'
      ```
- [ ] Confirm the 50-code keys are still there and readable

`aws s3 cp` never deletes. `aws s3 sync --delete` does. Do not use sync here.

---

## Phase 5 — Deploy (AWS + EC2)

Box as of the resize: `i-0d9324e54da57b696`, **c6a.xlarge** (4 vCPU / 8 GiB —
AMD rather than the c6i in the original plan; same memory, which is the binding
constraint, marginally slower forward pass). Elastic IP **52.20.157.176**,
replacing the plain public IP `34.199.65.62`, which would have changed on every
stop/start — and this box is stopped between demos by design, so that was a
DNS break waiting to happen. The Cloudflare `A` record for `api` points here.


**Tag the running image before you replace it. This is your rollback.**

```bash
ssh -i "<path>/shifamind-key.pem" ubuntu@52.20.157.176
docker ps                                    # note the running image
docker tag shifamind-api:latest shifamind-api:50code-rollback
docker images | grep shifamind               # confirm the tag exists
```

- [ ] Rollback tag exists on the box **before** anything else happens
- [ ] Build and ship the new image: `./infra/deploy.sh ec2` with
      `EC2_HOST=52.20.157.176 EC2_USER=ubuntu SSH_KEY=<path>/shifamind-key.pem`
- [ ] `.env` on the box: **no S3 key edits needed.** `config.py` already
      defaults every `S3_FULLCODE_*_KEY` to `models/fullcode/s10/…`, which is
      where Phase 4 uploaded. The old `S3_MODEL_KEY`/`S3_THRESHOLDS_KEY` are
      read by nothing now; leave them for the rollback image, which does use them
- [ ] `.env` on the box: `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` **blank**.
      The instance role supplies them. A long-lived key on an internet-facing
      box is the thing this avoids
- [ ] Instance is c6i.xlarge. Peak RSS measured at 4,175MB; t3.medium/large
      cannot hold it and the OOM killer takes the container mid-demo
- [ ] Container starts and stays up: `docker ps`, then `docker logs -f shifamind-api`
- [ ] Model loads. First boot downloads 758MB from S3, so give it time
- [ ] `curl -s localhost:8000/api/health` reports `codes: 7940`

**Rollback, any time:**
```bash
docker stop shifamind-api && docker rm shifamind-api
docker run -d --name shifamind-api --restart unless-stopped -p 8000:8000 \
  --env-file /home/ubuntu/shifamind/.env.50code shifamind-api:50code-rollback
```
Keep `.env.50code` on the box with the old S3 keys in it, written in Phase 4.

`deploy.sh` now tags the running image as `shifamind-api:previous` (plus a
timestamped copy) before it loads the new one, so the rollback tag exists even
if the manual step above is skipped. It also mounts
`/var/lib/shifamind/fullcode` from the host, so `docker rm` no longer costs a
758MB re-download on the next boot.

---

## Phase 6 — Automated smoke checks

No human review here, by decision. These all run without one.

- [ ] 20 notes through the API, all return 200
- [ ] No note returns an empty code list
- [ ] Every returned code carries at least one concept with a non-empty span
- [ ] No code outside the 7,940 vocabulary appears
- [ ] p95 latency acceptable at your expected concurrency
- [ ] Memory stable over 100 sequential requests. `docker stats` at start and end
- [ ] Frontend renders the new evidence fields without console errors
- [ ] PHI defaults unchanged: no training on customer data, audit logging on

---

## Phase 7 — Site and cutover

- [ ] Frontend promoted on Netlify
- [ ] Watch 30 minutes: error rate, latency, memory
- [ ] ShifaMind page numbers updated
- [ ] Flip `FULL_CODE_PUBLIC` in `Website/src/components/shifamind/FullCodeBenchmark.tsx`
      once the preprint posts, and set `PAPER_URL`

---

## Phase 8 — Decommission (not before one week stable)

Nothing here runs until Phase 7 is signed off: the new stack live on
`api.roshan-ai.com`, Phase 6 smoke checks passed, and at least one real demo
run on it. Until then `phase1/` IS the rollback, and the old box still cold-boots
from it.

- [ ] **Delete the stale 50-code artifacts from S3.** Dry run, read the list,
      then drop the flag:
      `aws s3 rm s3://shifamind-models/phase1/ --recursive --dryrun`
      (Mohammed asked to be reminded of this one.)
- [ ] Drop the `50code-rollback` image tag, and the `shifamind-api:previous-*`
      tags `deploy.sh` accumulates
- [ ] Remove the 50-code path from the serving code
- [ ] Archive `optimal_thresholds.json` and the 111-concept list
- [ ] `rm .env.bak.*` from the repo root if any remain — gitignored, but they
      hold live credentials

---

## Open items

- [ ] Confirm the paper's 27.2 macro-F1 came from these three seeds under the
      Wu et al. convention (artifacts give 25.7 under mean-of-per-code)
- [ ] Manual coder review, deferred to after deployment by decision
