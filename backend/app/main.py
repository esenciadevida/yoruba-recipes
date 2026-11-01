from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import router as v1_router
from app.db.session import create_db_and_tables
from app.seed import seed_data_if_empty
from app.seed_categories import seed_categories
from app.core.config import settings
from app.core.rate_limit import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    seed_data_if_empty()
    seed_categories()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    lifespan=lifespan,
)

# ── Rate limiter setup (immediately after app creation) ──
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count"],
)

# Routers
app.include_router(v1_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}