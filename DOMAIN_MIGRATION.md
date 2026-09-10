# Domain Migration — platform.shifamind.me → platform.roshan-ai.com/shifamind

Path-based, multi-product layout so every Roshan AI product lives under one host:

| Product    | URL                                         |
|------------|---------------------------------------------|
| ShifaMind  | `https://platform.roshan-ai.com/shifamind`  |
| NabzGraph  | `https://platform.roshan-ai.com/nabzgraph`  (future) |

Each product stays its own Netlify site/app; `platform.roshan-ai.com` is a thin
router that rewrites each path prefix to the right site. This keeps independent
deploys and scaling per product while presenting one clean domain.

The backend API moves to `api.roshan-ai.com`, fronted by Cloudflare (see §0).

## 0. API host → api.roshan-ai.com (via Cloudflare) — fixes the SSL error

**Why:** `api.shifamind.me` resolves to the Elastic IP (52.20.157.176) and the
server answers on 443, but the TLS cert doesn't cover that hostname
(`curl` → "no alternative certificate subject name matches"), so browsers reject
it ("Failed to fetch"). Putting the API behind Cloudflare lets Cloudflare's edge
present a valid cert automatically — no certbot/renewals on EC2.

**Steps (in Cloudflare, zone `roshan-ai.com`):**
1. DNS → add `A` record: name `api`, IPv4 `52.20.157.176`, **Proxied** (orange cloud).
2. SSL/TLS → Overview → set encryption mode:
   - **Flexible** if the EC2 origin serves plain HTTP (e.g. uvicorn/nginx on :80) —
     fastest to get unblocked. Cloudflare↔browser is HTTPS; Cloudflare↔origin is HTTP.
   - **Full** if the origin already serves HTTPS (even a self-signed/origin cert).
     More secure; prefer this once stable (install a Cloudflare Origin Certificate
     on the box).
3. Make sure the EC2 **security group** allows inbound from Cloudflare on the origin
   port (80 or 443). The app container itself listens on 8000 (`infra/deploy.sh`),
   so you need nginx/Caddy on 80→8000, **or** an Origin Rule in Cloudflare overriding
   the origin port to 8000.
4. Verify: `curl -i https://api.roshan-ai.com/api/health` → `200` JSON, and
   `https://api.roshan-ai.com/api/docs` loads.

**Code already updated for this (committed / local):**
- `.env` + `.env.example` — `NEXT_PUBLIC_API_URL=https://api.roshan-ai.com`.
- `CORS_ORIGINS` (root `.env` + `backend/app/config.py` default) now includes
  `https://platform.roshan-ai.com` (old origin kept for transition).
- After step 1 is live, redeploy the backend so the new CORS list takes effect,
  and rebuild/redeploy the frontend so the new API URL is baked in.

**Retire `api.shifamind.me`** once `api.roshan-ai.com` is verified.

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
