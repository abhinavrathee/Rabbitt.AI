# Sales Insight Automator 🐰

> **Rabbitt AI** · Sprint Prototype · March 2026
>
> Upload a `.csv` or `.xlsx` file. Groq (Llama 3.3 70B) generates an executive brief → delivers it to your inbox.

---

## Live URLs

| Service | URL |
|---|---|
| Frontend | `https://sales-insight.vercel.app` *(update after deploy)* |
| Backend API | `https://sales-insight-api.onrender.com` *(update after deploy)* |
| Swagger Docs | `https://sales-insight-api.onrender.com/docs` |

---

## Local Development (No Docker Required)

### Prerequisites

| Tool | Version |
|---|---|
| Python | 3.11+ |
| Node.js | 20+ |
| npm | 10+ |

### 1 — Clone the repo

```bash
git clone https://github.com/your-org/sales-insight-automator.git
cd sales-insight-automator
```

### 2 — Configure environment variables

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` and fill in your keys:

```
GEMINI_API_KEY=<your Gemini key>   # https://aistudio.google.com/app/apikey
SMTP_USER=<your Gmail address>
SMTP_PASSWORD=<Gmail App Password> # https://myaccount.google.com/apppasswords
```

### 3 — Start the backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
# → Backend running at http://localhost:8000
# → Swagger docs at http://localhost:8000/docs
```

### 4 — Start the frontend

```bash
cd frontend
npm install
npm run dev
# → Frontend running at http://localhost:5173
```

Open `http://localhost:5173`, upload `sales_q1_2026.csv`, enter an email, and click **Generate & Send Summary**.

---

## Docker (Documented Deliverable — Optional)

> The application runs perfectly without Docker. These instructions are provided for containerised deployments.

```bash
# Copy env file
cp backend/.env.example backend/.env
# (fill in your keys in backend/.env)

# Build and run both services
docker-compose up --build

# Frontend → http://localhost:5173
# Backend  → http://localhost:8000
# Swagger  → http://localhost:8000/docs
```

---

## Running Tests

```bash
cd backend
pip install pytest
pytest tests/ -v
```

---

## Environment Variables Reference

All variables live in `backend/.env` (copy from `backend/.env.example`).

| Variable | Description | Required |
|---|---|---|
| `GROQ_API_KEY` | Groq API key (get free at console.groq.com) | ✅ |
| `GROQ_MODEL` | Model name (default: `llama-3.3-70b-versatile`) | optional |
| `SMTP_USER` | Gmail address to send from | ✅ |
| `SMTP_PASSWORD` | Gmail App Password | ✅ |
| `SMTP_HOST` | SMTP host (default: `smtp.gmail.com`) | optional |
| `SMTP_PORT` | SMTP port (default: `587`) | optional |
| `FROM_NAME` | Display name in the "From" header | optional |
| `FRONTEND_ORIGIN` | Allowed CORS origin | ✅ |
| `MAX_FILE_SIZE_MB` | Upload size ceiling (default: `5`) | optional |
| `RATE_LIMIT` | SlowAPI rate limit (default: `5/minute`) | optional |

---

## Security Overview

| Layer | Mechanism |
|---|---|
| **Rate Limiting** | `SlowAPI` — 5 requests/minute per IP on `/api/upload` |
| **File Validation** | Extension whitelist (`.csv`, `.xlsx`), max 5 MB enforced server-side |
| **CORS** | Restricted to `FRONTEND_ORIGIN` env var only |
| **Input Validation** | `pydantic.EmailStr` for emails; form fields validated by FastAPI |
| **Secrets** | All credentials in `.env`, never committed (`.gitignore` excludes `.env`) |
| **No Shell Exec** | Files parsed entirely by `pandas` — no `subprocess` or shell calls |
| **Non-root Docker** | Docker containers run as a non-root user (`appuser`) |

---

## Architecture

```
Browser (React + Vite SPA)
    │  POST /api/upload  (multipart)
    ▼
FastAPI Backend
    ├── Rate Limiter (SlowAPI)
    ├── File validator (ext + size)
    ├── services/parser.py   → pandas → markdown summary
    ├── services/ai.py       → Groq Llama 3.3 70B
    └── services/email.py    → Gmail SMTP → inbox
```

---

## CI / CD

GitHub Actions triggers on every **Pull Request to `main`**:

1. `🐍 Lint Backend` — `flake8` + `black --check`
2. `🧪 Test Backend` — `pytest tests/ -v`
3. `⚛️ Lint & Build Frontend` — `eslint` + `vite build`

See [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

---

## Reference Data

`sales_q1_2026.csv` is included in the repo root for testing.

---

## License

MIT © Rabbitt AI
