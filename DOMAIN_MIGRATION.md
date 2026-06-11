# Domain Migration — platform.shifamind.me → platform.roshan-ai.com/shifamind

Path-based, multi-product layout so every Roshan AI product lives under one host:

| Product    | URL                                         |
|------------|---------------------------------------------|
| ShifaMind  | `https://platform.roshan-ai.com/shifamind`  |
| NabzGraph  | `https://platform.roshan-ai.com/nabzgraph`  (future) |

Each product stays its own Netlify site/app; `platform.roshan-ai.com` is a thin
router that rewrites each path prefix to the right site. This keeps independent
deploys and scaling per product while presenting one clean domain.

## What's already done in code (this PR)
- `frontend/next.config.mjs` — `basePath`/`assetPrefix` driven by
  `NEXT_PUBLIC_BASE_PATH`. **Opt-in:** empty by default, so the current
  `platform.shifamind.me` deploy is unaffected until you set the env var.
- `frontend/app/login/page.tsx` — magic-link `emailRedirectTo` now respects the
  base path.
- Website `src/lib/config.ts` — `PLATFORM_URL` updated to the new URL (with
  `PLATFORM_URL_LEGACY` kept). **Do not deploy the website change until step 4.**

## Cutover steps (you run these — DNS/host changes, not done in this PR)

1. **DNS** — add a record for `platform.roshan-ai.com` (CNAME → the router
   Netlify site, or an A/ALIAS per your DNS host).

2. **Set the base path on the ShifaMind Netlify site**
   - Site → Environment variables → `NEXT_PUBLIC_BASE_PATH = /shifamind`
   - Redeploy. The app now serves under `/shifamind`.

3. **Add the router rewrite** on the `platform.roshan-ai.com` site so the path
   prefix proxies to the ShifaMind site. In that site's `netlify.toml`:
   ```toml
   [[redirects]]
     from = "/shifamind/*"
     to = "https://<shifamind-site>.netlify.app/shifamind/:splat"
     status = 200          # 200 = proxy/rewrite (URL stays platform.roshan-ai.com)
     force = true
   # later:
   # [[redirects]]
   #   from = "/nabzgraph/*"
   #   to = "https://<nabzgraph-site>.netlify.app/nabzgraph/:splat"
   #   status = 200
   #   force = true
   ```
   (Alternatively run all products as one Next app with route groups — simpler
   routing, but couples deploys. The per-site rewrite above is the recommended
   path given ShifaMind is already its own app.)

4. **Update + deploy the website** so "Try ShifaMind" points to the new URL
   (the `config.ts` change in this PR). Only after steps 1–3 are verified.

5. **Backend CORS** — add the new origin in the backend `.env`:
   ```
   CORS_ORIGINS="https://platform.roshan-ai.com,https://platform.shifamind.me,http://localhost:3000"
   ```
   Redeploy the API.

6. **Supabase Auth** — add `https://platform.roshan-ai.com/shifamind/**` to
   Auth → URL Configuration → Redirect URLs (keep the old one during transition).

7. **Old domain** — keep `platform.shifamind.me` 301-redirecting to the new URL
   for a transition window, then retire.

## Rollback
Unset `NEXT_PUBLIC_BASE_PATH` and revert the website `config.ts` to
`PLATFORM_URL_LEGACY`. No code changes required.
