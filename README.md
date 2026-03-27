# ShifaMind Platform

Authenticated clinical decision support platform for doctors — ICD-10 predictions, concept explanations, and LLM-powered chat grounded in Phase 1 BioClinicalBERT output.

**Live:** `platform.shifamind.me` (Netlify) | API: `api.shifamind.me` (AWS EC2/ECS)

---

## Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14 (App Router) + Tailwind CSS + shadcn/ui |
| Hosting | Netlify + `@netlify/plugin-nextjs` |
| Auth & DB | Supabase (Auth + Postgres) |
| Backend | FastAPI (Python 3.11) |
| ML Inference | PyTorch + BioClinicalBERT Phase 1 (~300ms CPU) |
| LLM | OpenRouter (default) → AWS Bedrock (swap via env var) |
| Model Storage | AWS S3 |

---

## Build Plan

| Part | Focus | Status |
|------|-------|--------|
| **1** | Foundation: scaffold, auth, DB schema, backend skeleton | ✅ This PR |
| **2** | ML serving: Phase 1 model + `/api/predict` + Workspace UI | Pending |
| **3** | LLM & chat: OpenRouter/Bedrock + SSE streaming | Pending |
| **4** | Data layer + admin dashboard + UX polish | Pending |

---

## Quick Start

### Prerequisites
- Node.js 20+
- Python 3.11+
- A Supabase project (free tier)

### 1. Clone & configure

```bash
git clone https://github.com/roshan-ai-llc/shifamind_test
cd shifamind_test
cp .env.example .env
# Fill in your Supabase URL, keys, etc.
```

### 2. Apply database schema

In your Supabase SQL editor, run:
```
supabase/migrations/001_initial_schema.sql
```

### 3. Seed doctor accounts

```bash
pip install supabase python-dotenv
python scripts/seed_doctors.py
```

Default password: `ShifaMind2025!` (override with `SEED_PASSWORD` env var)

### 4. Run the frontend

```bash
cd frontend
cp ../.env.example .env.local   # fill NEXT_PUBLIC_* vars
npm install
npm run dev
# → http://localhost:3000
```

### 5. Run the backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# → http://localhost:8000/api/health
# → http://localhost:8000/api/docs
```

---

## Project Structure

```
shifamind-platform/
├── frontend/          # Next.js 14 App Router
│   ├── app/           # Pages (login, dashboard, admin)
│   ├── components/    # UI components (glass design system)
│   ├── lib/           # Supabase clients, utils
│   └── hooks/         # useAuth, usePrediction, useChat
├── backend/           # FastAPI
│   └── app/           # main, config, routers, schemas
├── model/             # Phase 1 inference code (added Part 2)
├── supabase/
│   └── migrations/    # SQL schema
├── scripts/           # seed_doctors.py, seed_notes.py
└── infra/             # Dockerfile, deploy scripts
```

---

## Environment Variables

See `.env.example` for all required variables.

Key ones for Part 1:
- `NEXT_PUBLIC_SUPABASE_URL` + `NEXT_PUBLIC_SUPABASE_ANON_KEY` — frontend auth
- `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` — backend + seed scripts
- `NEXT_PUBLIC_API_URL` — points frontend to backend

---

## Design System

Glassmorphism — matches `shifamind.me` aesthetic.

```
--bg-deep: #060a13       Dark navy background
--accent:  #4ecdc4       Teal accent (predictions, CTAs)
--glass:   rgba(255,255,255,0.04) + backdrop-blur-xl
```

All content uses `GlassCard` on a dark background. No ambient orbs in the app shell (unlike the marketing page).
