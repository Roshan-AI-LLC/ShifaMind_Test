# Queued — not done in the design-overhaul session (2026-06-11)

We deliberately scoped today's session to the **design overhaul** (highest-visible-
impact, lowest-risk) and prep work. The items below are pinned for follow-up
sessions so nothing gets rushed. Roughly in priority order.

## 1. Backend / DB fixes (see DIAGNOSIS.md for root causes)
- [ ] **Model loading** — `MODEL_SOURCE=s3` but AWS creds are blank, so `/predict`
      returns 503 off-EC2. Attach an EC2 IAM role, OR bake weights into the image
      with `MODEL_SOURCE=local`, OR populate backend AWS creds. _This is the most
      likely cause of "bad results."_
- [ ] **Silent persistence** — `predict.py` swallows Supabase insert failures with a
      `logger.warning`. Surface the error and add an integration test asserting a row
      lands in `predictions`. _This is the most likely cause of "DB not linking."_
- [ ] **Verify** `get_current_doctor` returns the auth UID that RLS `predictions_own`
      (`auth.uid() = doctor_id`) checks against.
- [ ] **LLM** — move off OpenRouter `:free` (rate-limited) to a paid model, and/or
      wire Bedrock creds so the fallback actually works. Fix the bogus
      `OPENROUTER_MODEL` default in `config.py`.

## 2. Performance pass (frontend)
- [ ] Run `next build` on a machine with network and check bundle sizes / route
      weights (the sandbox couldn't fetch the Linux SWC binary).
- [ ] Audit the self-hosted fonts — consider subsetting Inter/Tomorrow (currently
      shipping full variable + 4 Tomorrow weights ≈ 2 MB) to trim transfer.
- [ ] Lighthouse pass on login + dashboard; lazy-load heavy workspace tabs.

## 3. Domain migration (steps written up in DOMAIN_MIGRATION.md)
- [ ] DNS for `platform.roshan-ai.com`.
- [ ] Set `NEXT_PUBLIC_BASE_PATH=/shifamind` on the ShifaMind Netlify site.
- [ ] Add the `/shifamind/*` rewrite on the router site.
- [ ] Add new origin to backend `CORS_ORIGINS` + Supabase redirect URLs.
- [ ] Deploy the website `config.ts` change (only after the above is live).
- [ ] 301 the old `platform.shifamind.me` for a transition window.

## 4. Multi-product scaffolding
- [ ] Stand up `platform.roshan-ai.com/nabzgraph` using the same basePath pattern
      and the NabzGraph theme (the website already defines `.theme-nabzgraph`
      ocean-cyan tokens — port them into the platform the same way ShifaMind's were).
- [ ] Optional launcher at `platform.roshan-ai.com` root listing the products.

## 5. Design polish follow-ups (nice-to-have)
- [ ] Visually QA every dashboard sub-page in light mode on a real browser; the
      token migration is mechanical, so eyeball contrast on charts/admin tables.
- [ ] Consider porting the website's scroll-reveal motion into longer dashboard
      pages for parity (currently using the lighter `enter-fade-up` entrances).
