# Go-Live Runbook — full migration to roshan-ai.com (with predictions)

Target end state:
- **Frontend:** `https://platform.roshan-ai.com/shifamind` (Netlify, basePath `/shifamind`)
- **API:** `https://api.roshan-ai.com` (Cloudflare → EC2 nginx → container :8000)
- **DB/Auth:** Supabase (unchanged)
- **Predictions:** model loaded on EC2

Do the phases **in order** — each has a verification gate. Don't move on until the
gate passes.

Your topology (confirmed from the repo, DEPLOY.md §9g):
`browser → Cloudflare (TLS) → EC2 nginx :80/:443 → uvicorn container :8000`

---

## Phase 1 — Get the API live at api.roshan-ai.com (fixes the SSL error)

### 1.1 SSH in and see what's actually running
```bash
ssh -i "/Users/mohammedsameersyed/Documents/Roshan AI/ShifaMind/ShifaMindv2/Repos/ShifaMind_Prod/shifamind-key.pem" ubuntu@52.20.157.176

docker ps                                  # expect: shifamind-api ... Up
curl -s localhost:8000/api/health ; echo   # expect: {"status":"ok","model_loaded":...}
sudo ss -tlnp | grep -E ':80 |:443 |:8000'  # what's listening on 80/443/8000?
```
- If `docker ps` is empty → the container isn't running. Redeploy: from your **local**
  machine, `export EC2_HOST=52.20.157.176 EC2_USER=ubuntu SSH_KEY="/Users/mohammedsameersyed/Documents/Roshan AI/ShifaMind/ShifaMindv2/Repos/ShifaMind_Prod/shifamind-key.pem"`
  then `./infra/deploy.sh ec2`.
- Note whether **nginx** is on :80 (it should be, per your setup).

### 1.2 Make nginx answer for the new hostname
Edit the server block so it accepts api.roshan-ai.com (keep the old name too during
transition):
```bash
sudo nano /etc/nginx/sites-available/shifamind-api
```
Set:
```nginx
server {
    listen 80;
    server_name api.roshan-ai.com api.shifamind.me;
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        # SSE streaming for chat — keep these
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 300s;
        chunked_transfer_encoding on;
    }
}
```
```bash
sudo nginx -t && sudo systemctl reload nginx
```
> You do **not** need certbot anymore — Cloudflare provides the public cert. nginx can
> stay on plain :80 behind Cloudflare.

### 1.3 Open the firewall to Cloudflare
AWS Console → EC2 → Security Groups → your instance's group → Inbound rules → add:
- **HTTP : 80 : 0.0.0.0/0** (and ::/0)
- (keep 22 for SSH; you can later restrict 80 to Cloudflare IP ranges)

### 1.4 Cloudflare DNS + SSL (zone: roshan-ai.com)
1. **DNS → Add record:** `A`, name `api`, IPv4 `52.20.157.176`, **Proxied** (orange cloud).
2. **SSL/TLS → Overview → Flexible**
   (browser↔Cloudflare = HTTPS; Cloudflare↔nginx = HTTP on :80. Simplest, works now.
   Harden to **Full** later by installing a Cloudflare Origin Cert on nginx + listen 443.)

### ✅ Gate 1
```bash
curl -i https://api.roshan-ai.com/api/health
```
Expect `200` and JSON `{"status":"ok","model_loaded":<bool>,...}`.
Also open `https://api.roshan-ai.com/api/docs` — Swagger should load.
If it hangs → firewall (1.3). If 522/523 → origin not reachable on :80 (nginx/1.2).

---

## Phase 2 — Make predictions work (model loaded)

Look at `model_loaded` from Gate 1.
- **`true`** → predictions already work. Skip to Phase 3. 🎉
- **`false`** → the model didn't load. Diagnose on EC2:
```bash
docker logs shifamind-api 2>&1 | grep -iE 'model|s3|cred|error' | tail -30
```
Most likely cause (per DIAGNOSIS.md): `MODEL_SOURCE=s3` but the container can't reach S3.
Check the prod env the container uses:
```bash
grep -E 'MODEL_SOURCE|S3_|AWS_' ~/shifamind/.env
```
Fix one of these, then `docker restart shifamind-api` and re-check `/api/health`:
1. **Add AWS creds** (if blank): put real `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`
   (an IAM user with `s3:GetObject` on `s3://shifamind-models/*`) into `~/shifamind/.env`.
   - Confirm the weights exist: `aws s3 ls s3://shifamind-models/phase1/`
   - If they're missing, upload from a machine that has them:
     `python scripts/upload_model_s3.py` (see DEPLOY.md §8).
2. **Or attach an IAM role** to the EC2 instance with that S3 read policy (no keys in
   `.env` needed) — cleaner long-term.
3. **Or go local:** set `MODEL_SOURCE=local`, put `phase1_best.pt` + the json metadata
   in the image/`model/` dir, redeploy. Heavier image, but no S3 dependency.

### ✅ Gate 2
`curl -s https://api.roshan-ai.com/api/health` shows `"model_loaded": true`.

---

## Phase 3 — Frontend live at platform.roshan-ai.com/shifamind (Netlify)

### 3.1 Point Netlify at the right branch
Netlify → your ShifaMind site → **Site configuration → Build & deploy → Branches**:
deploy branch = **`claude/init-empty-repo-9OMXj`** (where you merged everything).

### 3.2 Environment variables
Netlify → **Site configuration → Environment variables** — set:
| Key | Value |
|-----|-------|
| `NEXT_PUBLIC_BASE_PATH` | `/shifamind` |
| `NEXT_PUBLIC_API_URL` | `https://api.roshan-ai.com` |
| `NEXT_PUBLIC_SUPABASE_URL` | your Supabase URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | your publishable / anon key |

### 3.3 Custom domain
1. Netlify → **Domain management → Add domain** → `platform.roshan-ai.com`.
2. Cloudflare → DNS → **CNAME** `platform` → `<your-site>.netlify.app`,
   **DNS only (grey cloud)** so Netlify serves its own TLS cert (avoids double-proxy/cert
   loops). Netlify auto-provisions Let's Encrypt for the domain.

### 3.4 Deploy
Trigger a deploy (push, or Netlify → Deploys → Trigger deploy → **Clear cache and deploy**
so the new env vars + basePath bake in). The `netlify.toml` `/` → `/shifamind` redirect
(already in the repo) makes the bare domain land on the app.

### ✅ Gate 3
- `https://platform.roshan-ai.com/shifamind` loads the redesigned login.
- `https://platform.roshan-ai.com/` redirects to `/shifamind`.

---

## Phase 4 — Wire the cross-service settings

### 4.1 Backend CORS (already in code; confirm on the box)
The container's env must allow the new origin. `~/shifamind/.env` →
`CORS_ORIGINS=https://platform.roshan-ai.com,https://platform.shifamind.me,http://localhost:3000`
then `docker restart shifamind-api`.

### 4.2 Supabase redirect URLs
Supabase → **Authentication → URL Configuration → Redirect URLs** → add:
`https://platform.roshan-ai.com/shifamind/**` (keep the old one during transition).
Set **Site URL** to `https://platform.roshan-ai.com/shifamind`.

### ✅ Gate 4 (end-to-end)
Open `https://platform.roshan-ai.com/shifamind`, sign in, open Workspace:
- Sample templates load (API + Supabase reachable, CORS ok).
- Paste a note → Predict → ranked ICD-10 codes appear (model loaded).
- Chat streams a reply (SSE through nginx + Cloudflare).

---

## After it's all green
- Update the **website** `PLATFORM_URL` (already staged in the Website repo) and deploy it
  so "Try ShifaMind" points to the new URL.
- Do the **Namecheap** auto-renew + redirect (NAMECHEAP_SHIFAMIND_ME.md).
- Retire `api.shifamind.me` / `platform.shifamind.me` once stable.
- Harden Cloudflare API SSL from Flexible → Full (origin cert on nginx).

## If chat streaming is choppy
Cloudflare can buffer SSE. If replies arrive in bursts, add a Cloudflare **Configuration
Rule** for `api.roshan-ai.com/api/chat*` or test with the proxy temporarily set to DNS-only
to confirm nginx's `proxy_buffering off` is doing its job.
