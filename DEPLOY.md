# ShifaMind Platform — Full Deployment Guide

> From zero to fully running app. Frontend first, then backend.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Clone the Repository](#2-clone-the-repository)
3. [Supabase Setup](#3-supabase-setup)
4. [Frontend — Local Dev](#4-frontend--local-dev)
5. [Seed the Database](#5-seed-the-database)
6. [Deploy Frontend to Netlify](#6-deploy-frontend-to-netlify)
7. [Backend — Local Dev](#7-backend--local-dev)
8. [Upload Model to S3](#8-upload-model-to-s3)
9. [Deploy Backend to AWS](#9-deploy-backend-to-aws)
10. [Connect Frontend to Live API](#10-connect-frontend-to-live-api)
11. [OpenRouter LLM Setup](#11-openrouter-llm-setup)
12. [Verify Everything Works](#12-verify-everything-works)
13. [Optional: Switch to AWS Bedrock](#13-optional-switch-to-aws-bedrock)

---

## 1. Prerequisites

Install these before starting:

| Tool | Version | Install |
|------|---------|---------|
| Git | any | https://git-scm.com |
| Node.js | 20+ | https://nodejs.org |
| Python | 3.11+ | https://python.org |
| Docker | any | https://docker.com |
| AWS CLI | v2 | https://aws.amazon.com/cli |

Create accounts (all free tiers work):

- [Supabase](https://supabase.com) — auth + database
- [Netlify](https://netlify.com) — frontend hosting
- [OpenRouter](https://openrouter.ai) — LLM (free tier, 200 req/day)
- AWS account — EC2 + S3 (or use a free-tier t2.micro for testing)

---

## 2. Clone the Repository

```bash
git clone https://github.com/roshan-ai-llc/shifamind_test.git
cd shifamind_test

# Confirm you're on the right branch
git checkout claude/init-empty-repo-9OMXj
git log --oneline -5
```

Copy the root env file:

```bash
cp .env.example .env
```

Leave `.env` open — you'll fill in values as you go through this guide.

---

## 3. Supabase Setup

### 3a. Create a new project

1. Go to [supabase.com](https://supabase.com) → **New project**
2. Choose a name (e.g. `shifamind-platform`), set a database password, pick a region close to you
3. Wait ~2 minutes for it to provision

### 3b. Grab your keys

Supabase rolled out a new API key format in mid-2025. Depending on when you created your project you'll see one of two layouts — both work fine.

**Go to: Project Settings → API**

---

**New projects (created after July 2025) — new key format**

| What you need | Where to find it | Looks like |
|---------------|-----------------|------------|
| Project URL | "Project URL" box | `https://xxxxxxxxxxxx.supabase.co` |
| Publishable key | "API Keys" → **Publishable** | `sb_publishable_...` |
| Secret key | "API Keys" → **Secret** (click "Reveal") | `sb_secret_...` |

> The **Secret** key is hidden by default — click the eye icon to reveal it. Every reveal is logged in your org's audit log.

---

**Older projects — legacy key format (still fully supported)**

| What you need | Where to find it | Looks like |
|---------------|-----------------|------------|
| Project URL | "Project URL" box | `https://xxxxxxxxxxxx.supabase.co` |
| anon key | "Project API keys" → **anon / public** | `eyJhbGciOiJIUz...` (long JWT) |
| service_role key | "Project API keys" → **service_role** | `eyJhbGciOiJIUz...` (long JWT) |

---

Copy the values into your `.env` file. Use whichever format your project shows:

```env
# URL is always the same
NEXT_PUBLIC_SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co

# Publishable / anon key  (safe for frontend)
NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_...   # new format
# NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGci...        # old format — either works
SUPABASE_ANON_KEY=sb_publishable_...

# Secret / service_role key  (backend only — never put in frontend)
SUPABASE_SERVICE_ROLE_KEY=sb_secret_...   # new format
# SUPABASE_SERVICE_ROLE_KEY=eyJhbGci...  # old format — either works
```

> **Why two keys?** The publishable/anon key is safe to expose — it only has low-privilege read access via RLS. The secret/service_role key bypasses RLS entirely and must never be in your frontend code or committed to git.

### 3c. Run the database migration

1. In Supabase: **SQL Editor → New query**
2. Open `supabase/migrations/001_initial_schema.sql` from the repo
3. Paste the entire contents and click **Run**
4. You should see: `Success. No rows returned`

This creates all 6 tables + RLS policies + indexes.

### 3d. (Optional) Disable email confirmation for dev

In Supabase: **Authentication → Providers → Email**
Turn off **"Confirm email"** — makes seeding doctor accounts easier locally.
Re-enable it before going to production.

---

## 4. Frontend — Local Dev

### 4a. Install dependencies

```bash
cd frontend
npm install
```

### 4b. Create your local env file

```bash
cp .env.example .env.local
```

Edit `frontend/.env.local` and set:

```env
NEXT_PUBLIC_SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Leave this pointing to localhost for now — you'll update after backend is live
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 4c. Start the dev server

```bash
npm run dev
```

Visit **http://localhost:3000**

You should see the login page. It will look correct but login won't work yet — you need to seed doctor accounts first (next step).

---

## 5. Seed the Database

Open a new terminal from the **repo root** (not inside `frontend/`).

### 5a. Create a virtual environment and install seed dependencies

```bash
# Make sure you're in the repo root, not frontend/
cd shifamind_test   # skip if already there

python3 -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate

pip install supabase python-dotenv
```

> Always use a venv — never `pip install` globally on a Mac/Linux machine. Your `.venv/` folder is already in `.gitignore`.

### 5b. Seed doctor accounts

```bash
SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co \
SUPABASE_SERVICE_ROLE_KEY=eyJ... \
python scripts/seed_doctors.py
```

This creates **15 doctor accounts** (12 doctors + 3 admins).
Default password: `ShifaMind2025!`

You'll see output like:
```
  Creating s.chen@shifamind.dev (doctor)... OK (id=abc12345...)
  Creating j.okafor@shifamind.dev (doctor)... OK
  ...
  Done: 15 created, 0 skipped, 0 failed
```

### 5c. Test login

Go back to **http://localhost:3000/login**

Sign in with:
- **Email:** `o.shaikh@shifamind.dev` (admin)
- **Password:** `ShifaMind2025!`

You should be redirected to `/dashboard`. The app shell (sidebar, header, dashboard home) should render fully.

### 5d. Seed sample notes

```bash
SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co \
SUPABASE_SERVICE_ROLE_KEY=eyJ... \
python scripts/seed_notes.py
```

This loads 10 clinical notes across 8 specialties into the `sample_notes` table. They'll appear in the Workspace note selector dropdown once the frontend connects to the backend API.

---

## 6. Deploy Frontend to Netlify

### 6a. Push to GitHub (if not already)

Your branch `claude/init-empty-repo-9OMXj` is already pushed to `roshan-ai-llc/shifamind_test`.

### 6b. Connect to Netlify

1. Go to [netlify.com](https://netlify.com) → **Add new site → Import an existing project**
2. Connect to GitHub → select `roshan-ai-llc/shifamind_test`
3. Set:
   - **Branch:** `claude/init-empty-repo-9OMXj`
   - **Base directory:** `frontend`
   - **Build command:** `npm run build`
   - **Publish directory:** `frontend/.next`
4. Click **Add the Netlify Next.js plugin** when prompted (or it auto-detects from `netlify.toml`)

### 6c. Set environment variables in Netlify

In Netlify: **Site configuration → Environment variables → Add a variable**

Add each of these:

| Key | Value |
|-----|-------|
| `NEXT_PUBLIC_SUPABASE_URL` | your Supabase project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | your publishable key (`sb_publishable_...`) or anon key (`eyJ...`) |
| `NEXT_PUBLIC_API_URL` | `https://api.shifamind.me` (or your EC2 URL for now) |

### 6d. Set custom domain

In Netlify: **Domain management → Add a domain**
Add `platform.shifamind.me` → follow the DNS instructions for your domain registrar.

### 6e. Trigger a deploy

Click **Deploy site**. First build takes ~2-3 minutes.

Once done, visit `https://platform.shifamind.me` — the login page should load.

> At this point the frontend is fully live. Login and navigation work. The Workspace and Chat will show errors until the backend is connected — that's expected.

---

## 7. Backend — Local Dev

### 7a. Create a virtual environment and install Python dependencies

```bash
# From the repo root
python3 -m venv .venv          # skip if you already made it in step 5
source .venv/bin/activate      # on Windows: .venv\Scripts\activate

pip install -r backend/requirements.txt
```

> This installs FastAPI, PyTorch, Transformers, boto3, Supabase client, and httpx.
> PyTorch is ~800MB — takes a few minutes.

### 7b. Create backend env file

```bash
cp ../.env.example .env
```

Edit `backend/.env` and set at minimum:

```env
# Supabase
SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...

# LLM (fill in after step 11)
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-...
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct:free

# Model (use local for now, switch to s3 after step 8)
MODEL_SOURCE=local
LOCAL_MODEL_PATH=../model/phase1_best.pt
LOCAL_THRESHOLDS_PATH=../model/optimal_thresholds.json
DEVICE=cpu

# CORS — allow local frontend
CORS_ORIGINS=http://localhost:3000,https://platform.shifamind.me
```

### 7c. Place model weights locally (if you have them)

If you have the trained model files:

```bash
cp /path/to/phase1_best.pt model/phase1_best.pt
cp /path/to/optimal_thresholds.json model/optimal_thresholds.json
```

If you **don't** have the weights yet, the API still starts — `model_loaded: false` in the health check. The `/api/predict` endpoint will return a 503 until weights are loaded.

### 7d. Start the API

```bash
# From the repo root, with venv active
cd backend
uvicorn app.main:app --reload --port 8000
```

Expected output:
```
INFO  ShifaMind API starting up...
INFO  Model loader: loading from local path...   ← if weights present
INFO  Phase 1 model loaded successfully.          ← if weights present
INFO  Startup complete.
INFO  Uvicorn running on http://0.0.0.0:8000
```

### 7e. Test the health endpoint

```bash
curl http://localhost:8000/api/health
```

Expected:
```json
{
  "status": "ok",
  "model_loaded": true,
  "llm_provider": "openrouter",
  "version": "1.0.0"
}
```

Visit **http://localhost:8000/api/docs** for the full interactive Swagger UI.

---

## 8. Upload Model to S3

Skip this step if you want to run with `MODEL_SOURCE=local` on EC2 directly. Using S3 is recommended for production (weights aren't baked into the Docker image).

### 8a. Create S3 bucket

```bash
aws s3 mb s3://shifamind-models --region us-east-1
```

Block public access (it's private by default — leave it that way):

```bash
aws s3api put-public-access-block \
  --bucket shifamind-models \
  --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

### 8b. Upload weights

```bash
AWS_ACCESS_KEY_ID=xxx \
AWS_SECRET_ACCESS_KEY=xxx \
S3_BUCKET=shifamind-models \
python scripts/upload_model_s3.py \
  --weights model/phase1_best.pt \
  --thresholds model/optimal_thresholds.json
```

You'll see a progress bar. ~400MB upload takes 1-3 minutes depending on connection.

Output:
```
Uploading to s3://shifamind-models/phase1/

  Uploading phase1_best.pt (398.2 MB) → s3://shifamind-models/phase1/phase1_best.pt
  [████████████████████] 100.0%

  Uploading optimal_thresholds.json (0.0 MB) → s3://shifamind-models/phase1/optimal_thresholds.json
  [████████████████████] 100.0%

Upload complete.
  S3_MODEL_KEY=phase1/phase1_best.pt
  S3_THRESHOLDS_KEY=phase1/optimal_thresholds.json
```

### 8c. Update backend env to use S3

In your production `.env`:

```env
MODEL_SOURCE=s3
S3_BUCKET=shifamind-models
S3_MODEL_KEY=phase1/phase1_best.pt
S3_THRESHOLDS_KEY=phase1/optimal_thresholds.json
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_DEFAULT_REGION=us-east-1
```

---

## 9. Deploy Backend to AWS

### 9a. Launch an EC2 instance

1. Go to AWS Console → **EC2 → Launch Instance**
2. Choose:
   - **AMI:** Ubuntu 22.04 LTS
   - **Instance type:** `t3.medium` (2 vCPU, 4GB RAM — minimum for PyTorch CPU inference)
   - **Storage:** 20GB gp3
   - **Security group:** Allow inbound TCP 8000 (API) and 22 (SSH) from your IP
3. Download your `.pem` key file
4. Launch

### 9b. Point your domain to EC2

In your DNS provider, add an **A record**:
```
api.shifamind.me  →  <your EC2 public IP>
```

Wait a few minutes for DNS to propagate.

### 9c. SSH in and install Docker

```bash
ssh -i ~/.ssh/shifamind.pem ubuntu@<EC2-IP>
```

On the server:

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker ubuntu
newgrp docker

# Confirm
docker --version
```

### 9d. Create the env file on EC2

```bash
mkdir ~/shifamind
nano ~/shifamind/.env
```

Paste your full production env (all vars from `.env.example`):

```env
SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...

LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-...
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct:free

MODEL_SOURCE=s3
S3_BUCKET=shifamind-models
S3_MODEL_KEY=phase1/phase1_best.pt
S3_THRESHOLDS_KEY=phase1/optimal_thresholds.json
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_DEFAULT_REGION=us-east-1

DEVICE=cpu
CORS_ORIGINS=https://platform.shifamind.me,http://localhost:3000
SECRET_KEY=<generate a random 64-char string>
```

Save with `Ctrl+X → Y → Enter`.

### 9e. Deploy using the deploy script

Back on your **local machine** (not EC2):

```bash
# Set your EC2 details
export EC2_HOST=<your-ec2-ip>
export EC2_USER=ubuntu
export SSH_KEY=~/.ssh/shifamind.pem

# Build and deploy
./infra/deploy.sh ec2
```

The script will:
1. Build the Docker image locally
2. Save it as a tarball
3. Copy it to EC2 via SCP
4. Load and start the container on EC2

This takes ~3-5 minutes for the first deploy.

### 9f. Verify the container is running

SSH back to EC2:

```bash
docker ps
# Should show: shifamind-api   Up X minutes
```

Check the health endpoint:

```bash
curl http://localhost:8000/api/health
# Or from your machine:
curl http://api.shifamind.me:8000/api/health
```

### 9g. (Optional) Nginx reverse proxy + HTTPS

Install Nginx and Certbot for HTTPS on `api.shifamind.me`:

```bash
sudo apt install -y nginx certbot python3-certbot-nginx
```

Create `/etc/nginx/sites-available/shifamind-api`:

```nginx
server {
    listen 80;
    server_name api.shifamind.me;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # SSE — disable buffering for streaming chat
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 300s;
        chunked_transfer_encoding on;
    }
}
```

Enable and get SSL cert:

```bash
sudo ln -s /etc/nginx/sites-available/shifamind-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
sudo certbot --nginx -d api.shifamind.me
```

After this, your API is at `https://api.shifamind.me/api/health`.

---

## 10. Connect Frontend to Live API

### 10a. Update Netlify env var

In Netlify: **Site configuration → Environment variables**

Update:
```
NEXT_PUBLIC_API_URL = https://api.shifamind.me
```

### 10b. Redeploy frontend

In Netlify: **Deploys → Trigger deploy → Deploy site**

Or push any commit to the branch — Netlify auto-deploys.

### 10c. Test the full flow

1. Go to `https://platform.shifamind.me`
2. Login with `o.shaikh@shifamind.dev` / `ShifaMind2025!`
3. Navigate to **Workspace**
4. Click "Choose a sample clinical note" — you should see the 10 seeded notes
5. Select one and click **Analyze with ShifaMind**
6. Predictions should load in ~300-500ms
7. Click **Discuss this case →** to open Chat
8. Type a message — you should see streaming LLM tokens

---

## 11. OpenRouter LLM Setup

### 11a. Get your API key

1. Go to [openrouter.ai](https://openrouter.ai) → Sign up
2. Go to **Keys → Create key**
3. Copy the key (starts with `sk-or-`)

### 11b. Set the key

In `backend/.env` (local) and the EC2 `~/shifamind/.env`:

```env
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxxxxxx
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct:free
```

The free tier gives **200 requests/day** with `meta-llama/llama-3.3-70b-instruct:free`. No credit card required.

### 11c. Redeploy backend after key change

```bash
export EC2_HOST=<your-ec2-ip>
export EC2_USER=ubuntu
export SSH_KEY=~/.ssh/shifamind.pem
./infra/deploy.sh ec2
```

---

## 12. Verify Everything Works

Run through this checklist:

### Auth
- [ ] Login at `/login` with `s.chen@shifamind.dev` / `ShifaMind2025!` — redirects to `/dashboard`
- [ ] Unauthenticated visit to `/dashboard` — redirects to `/login`
- [ ] Admin login with `o.shaikh@shifamind.dev` — sees Admin link in sidebar

### Workspace
- [ ] `/dashboard/workspace` — note selector dropdown shows 10 sample notes
- [ ] Select "Heart Failure" note, click Analyze — predictions appear in ~500ms
- [ ] Diagnoses tab shows ranked ICD-10 codes with confidence bars
- [ ] Concepts tab shows active concepts as pills and bars
- [ ] Attribution tab shows the diagnosis ↔ concept map
- [ ] "Rate prediction" opens star rating modal, submit sends review

### Chat
- [ ] Click "Discuss this case →" from Workspace — opens chat with prediction context
- [ ] Type a message, hit Enter — LLM responds with streaming tokens
- [ ] Right sidebar shows active diagnoses + concepts from the prediction
- [ ] "New chat" button resets the session

### History
- [ ] `/dashboard/history` — shows previous predictions
- [ ] Click a prediction card to expand — shows top codes + concepts
- [ ] Chat link in history card opens pre-loaded chat

### Profile
- [ ] `/dashboard/profile` — shows doctor name, specialty, activity stats
- [ ] "Send magic link" button triggers email (if SMTP configured in Supabase)

### Admin (sign in as admin first)
- [ ] `/admin` — shows stats tiles (predictions, chats, reviews, active doctors)
- [ ] Top ICD-10 codes chart populates after predictions are made
- [ ] Reviews table shows submitted feedback

### API health
```bash
curl https://api.shifamind.me/api/health
# Expected: {"status":"ok","model_loaded":true,"llm_provider":"openrouter","version":"1.0.0"}
```

---

## 13. Optional: Switch to AWS Bedrock

Once you have AWS credits or want to move off the OpenRouter free tier:

### 13a. Request model access

In AWS Console: **Bedrock → Model access**
Request access to:
- `meta.llama3-3-70b-instruct-v1:0` (primary)
- `anthropic.claude-sonnet-4-20250514-v1:0` (fallback)

Approval is usually instant for Llama, ~1 hour for Claude.

### 13b. Update one env var

On EC2, edit `~/shifamind/.env`:

```env
LLM_PROVIDER=bedrock
BEDROCK_PRIMARY_MODEL=meta.llama3-3-70b-instruct-v1:0
BEDROCK_FALLBACK_MODEL=anthropic.claude-sonnet-4-20250514-v1:0
```

Your existing `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` + `AWS_DEFAULT_REGION` are already set.
Make sure your IAM user has the `AmazonBedrockFullAccess` policy attached.

### 13c. Redeploy

```bash
./infra/deploy.sh ec2
```

That's it. One env var change. The backend factory auto-selects Bedrock. If the primary model fails, it falls back to Claude Sonnet automatically.

---

## Troubleshooting

**Login redirects loop**
→ Check `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` are set correctly in Netlify env vars and the site was redeployed after setting them.

**"Model not loaded" 503 on /api/predict**
→ Check `docker logs shifamind-api` on EC2. If S3 download failed, verify `AWS_ACCESS_KEY_ID`, `S3_BUCKET`, and that the bucket is in the same region as `AWS_DEFAULT_REGION`.

**Chat gives no response / SSE connection drops**
→ If using Nginx, confirm `proxy_buffering off` is set in the config. SSE requires unbuffered responses.

**"Doctor account not found" 403**
→ The logged-in user exists in `auth.users` but not in the `doctors` table. Re-run `python scripts/seed_doctors.py` or manually insert a row via Supabase SQL editor.

**CORS errors in browser**
→ Make sure `CORS_ORIGINS` on the backend includes both `https://platform.shifamind.me` and `http://localhost:3000` exactly (no trailing slash).

**Netlify build fails**
→ Confirm the **Base directory** is set to `frontend` in Netlify build settings, not the repo root.
