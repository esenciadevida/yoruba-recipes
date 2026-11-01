# Yorùbá Recipes

A full-stack platform for exploring authentic Yorùbá cuisine — foods, meal combinations, categories, and the stories behind them. Includes a public-facing site and a separate admin dashboard for managing content.

## Architecture

This repository contains three applications:

| Directory | Role | Stack |
| :--- | :--- | :--- |
| `backend/` | REST API, data model, auth, seeding | FastAPI · SQLModel · SQLite/PostgreSQL |
| `frontend/` | Public site: browse foods, combinations, categories | React 19 · Vite · Tailwind CSS 4 |
| `admin/` | Dashboard for creating and managing content | React · Vite |

## Features

- **Food catalogue** — browse dishes with descriptions, ingredients, and categories
- **Meal combinations** — curated pairings of foods that belong together
- **Category browsing** — soups, swallows, rice dishes, snacks, and more
- **Statistics endpoints** — counts and aggregates for the dashboard
- **JWT authentication** — protected routes for admin access
- **Auto-seeding** — the API seeds reference data on first boot, so a fresh clone runs without manual SQL

## Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API starts on `http://127.0.0.1:8000`. Interactive docs (Swagger UI) are at `/docs`, generated automatically from the FastAPI schemas.

Routes are organised by domain:

```
/api/foods          – list, filter, and read dishes
/api/combinations   – meal pairings
/api/categories     – category tree
/api/auth           – login and token issue
/api/stats          – aggregate counts
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Set the API base URL in a `.env` file before running:

```
VITE_API_URL=http://127.0.0.1:8000
```

The admin dashboard follows the same commands from the `admin/` directory.

## Configuration

| Variable | Used by | Description |
| :--- | :--- | :--- |
| `VITE_API_URL` | frontend, admin | Base URL of the backend API |
| `ALLOWED_ORIGINS` | backend | Comma-separated list of permitted CORS origins |
| `DATABASE_URL` | backend | Optional. Falls back to the bundled SQLite file |

## Tech notes

The API is built on SQLModel so the same class definitions drive both the database tables and the Pydantic response schemas, which keeps the models and the OpenAPI contract from drifting apart. CORS origins are read from the environment so the same build runs locally and in production.

## License

No license has been applied yet. Treat the code as all rights reserved until one is added.
