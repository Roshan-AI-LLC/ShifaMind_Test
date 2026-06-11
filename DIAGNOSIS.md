# ShifaMind Platform — Diagnosis (DB linking + "bad results")

_Diagnosed 2026-06-11. Findings only; fixes are queued (see QUEUED.md), not applied in the design-overhaul PR._

## Summary

The "DB isn't linking" and "results are bad" complaints are **two separate problems**, and
neither is a foundation issue. Ranked by likelihood of being what you're seeing:

### 1. Model can't load → `/predict` returns 503 (the "bad results")
- `.env` has `MODEL_SOURCE=s3` and `S3_BUCKET=shifamind-models`, but **`AWS_ACCESS_KEY_ID`
  and `AWS_SECRET_ACCESS_KEY` are blank.**
- With no creds, the backend cannot pull `phase1/phase1_best.pt` from S3, so
  `model_state["loaded"]` stays false and every `/predict` returns
  `503 "Model not loaded"`. The UI then shows nothing/garbage.
- On the EC2 host this *may* work via an instance IAM role; anywhere else it fails.
- **Confirm:** is the prod EC2 using an instance role? If not, this is the bug.
- **Fix options (queued):** attach an IAM role to EC2, OR set `MODEL_SOURCE=local` and bake
  weights into the image, OR populate AWS creds in the backend `.env`.

### 2. Prediction persistence fails silently (the "DB not linking")
- In `backend/app/routers/predict.py`, the Supabase insert into `predictions` is wrapped in
  `try/except` that only does `logger.warning(...)` and continues. **Any write failure is
  invisible to the user** — they get a result, but nothing is saved, so history/admin views
  look empty → "DB isn't working."
- The insert uses the user's JWT + anon key against RLS policy `predictions_own`
  (`auth.uid() = doctor_id`). This works only if `doctor["id"]` exactly equals the token's
  `auth.uid()`. Worth verifying the dependency `get_current_doctor` returns the auth UID, not
  a separate doctors-table PK.
- **Fix (queued):** surface persistence errors (at least to logs/metrics, ideally a non-fatal
  toast), and add an integration test that asserts a row lands in `predictions`.

### 3. LLM chat quality / rate limits
- `OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct:free`. The `:free` tier is ~200 req/day
  and frequently 429s → intermittent empty/poor chat answers.
- Bedrock fallback (`anthropic.claude-sonnet-4-...`) needs AWS creds, which are blank — so
  there is effectively **no working fallback** when OpenRouter rate-limits.
- Note: `config.py` default `OPENROUTER_MODEL` is `google/gemma-4-26b-a4b-it:free`, which is
  not a real model id — harmless since `.env` overrides it, but should be corrected.
- **Fix (queued):** move off `:free` to a paid OpenRouter model or wire up Bedrock creds so the
  fallback actually works.

## What is NOT broken
- Stack is modern (Next 16 / React 19 / Tailwind 4 / FastAPI / Supabase).
- Schema + RLS migrations (001–003, incl. the admin-recursion fix) look sound.
- Auth (Supabase SSR) is wired correctly.

## Recommended fix order (separate session)
1. Confirm/repair model loading (S3 creds or local weights) — restores predictions.
2. Make persistence failures loud + add a write integration test — restores "DB linking".
3. Move LLM off free tier and/or enable Bedrock fallback — restores chat quality.
