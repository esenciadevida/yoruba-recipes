from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.database import create_db_and_tables
from app.routers import foods, combinations, auth, categories, stats
from app.seed import seed_data_if_empty
from app.seed_categories import seed_categories

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    seed_data_if_empty()
    seed_categories()
    yield

app = FastAPI(
    title="Yoruba Recipes API",
    description="A curated showcase of authentic Yoruba foods and meal combinations.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count"],
)

# Include routers
app.include_router(foods.router)
app.include_router(combinations.router)
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(stats.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Yoruba Recipes API. Visit /docs for Swagger UI."}