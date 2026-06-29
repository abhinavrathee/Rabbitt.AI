import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv

from routers.upload import router as upload_router

load_dotenv()

# ---------------------------------------------------------------------------
# Rate limiter (shared instance — imported by routers)
# ---------------------------------------------------------------------------
limiter = Limiter(key_func=get_remote_address)

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Sales Insight Automator API",
    description=(
        "Upload a CSV or XLSX sales file and receive an AI-generated "
        "narrative summary delivered straight to your inbox."
    ),
    version="1.0.0",
    contact={"name": "Rabbitt AI Engineering", "email": "engineering@rabbittai.com"},
    license_info={"name": "MIT"},
)

# Attach rate-limiter state and exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS — restrict to configured frontend origin (or localhost for dev)
frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(upload_router, prefix="/api")


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/health", tags=["Health"], summary="Health check")
async def health():
    """Returns 200 OK when the service is healthy."""
    return {"status": "ok"}
