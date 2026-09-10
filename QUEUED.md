# Queued

Backlog, oldest first. Section 1 was raised in the design-overhaul session of
2026-06-11 and closed during the full-code deploy on 2026-09-09/10; sections
2-5 are still open.

## 1. Backend / DB fixes — DONE (2026-09-09/10)

All four closed during the full-code deploy. Root-cause notes live in
FULLCODE_DEPLOY.md now; DIAGNOSIS.md was deleted as it described only these.

- [x] **Model loading** — the box now pulls artifacts from S3 with an EC2
      instance role (`shifamind-ec2-s3`), no keys on disk. Cached on a mounted
      volume so replacing the container does not re-download 758MB
- [x] **Silent persistence** — `_persist()` logs `persist <id>: HTTP <code>` on
      every call, not only on failure, so silence in the log means the code did
      not run. The actual cause of the empty history turned out to be different
      and worse: the frontend was pointed at the OLD API host the whole time.
      See FULLCODE_DEPLOY.md Phase 3.4
- [x] **`get_current_doctor` / RLS uid** — verified by `scripts/diag_history.py`,
      which signs in as the doctor and makes the byte-identical insert. RLS and
      the column types were never the problem
- [x] **LLM** — the box carries a working paid OpenRouter key. Note the LOCAL
      `.env` still has a 9-character stub that 401s, so chat works in production
      and not on a laptop. Worth copying the box's value down

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
