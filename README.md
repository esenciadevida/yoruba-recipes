# Yorùbá Recipes

A full-stack platform for exploring Yorùbá cuisine — dishes, meal combinations, and the cultural context behind them. Ships with a public site, an admin dashboard for content management, and a versioned REST API.

## Repository layout

| Directory | Role | Stack |
| :--- | :--- | :--- |
| `backend/` | REST API, models, migrations, seeding | FastAPI · SQLModel · Alembic |
| `frontend/` | Public site | React 19 · Vite · Tailwind CSS 4 · Framer Motion |
| `admin/` | Content dashboard | React · Vite · Tailwind CSS 4 |

## Backend

The API is versioned under `/api/v1`. Interactive documentation is generated at `/docs`.

```
GET    /api/v1/recipes                 list and filter dishes
GET    /api/v1/recipes/{id}            single dish
GET    /api/v1/categories              categories
GET    /api/v1/combinations            curated meal pairings
POST   /api/v1/auth/register           create an account
POST   /api/v1/auth/login              issue a JWT
GET    /api/v1/auth/me                 current user
GET    /api/v1/stats                   dashboard aggregates
POST   /api/v1/newsletter/subscribe    mailing list signup
GET    /api/v1/admin/submissions       community submissions awaiting review
GET    /api/v1/developer/recipes       read-only developer API
```

Write operations are JWT-protected, and the API is rate limited with `slowapi`.

### Running locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Create a `.env` file in `backend/` first:

```
DATABASE_URL=sqlite:///./yoruba_recipes.db
SECRET_KEY=generate-a-random-value
```

`DATABASE_URL` defaults to a local SQLite file if unset; PostgreSQL works by pointing it at a `postgresql+psycopg2://` URL. Tables and reference data are created and seeded automatically on first start.

### Migrations

Alembic is configured for schema changes:

```bash
cd backend
alembic upgrade head
alembic revision --autogenerate -m "describe the change"
```

### Creating an admin user

Credentials are never hardcoded. Pass them as arguments or environment variables:

```bash
cd backend
python create_admin.py <username> <password>
# or
ADMIN_USERNAME=admin ADMIN_PASSWORD=... python create_admin.py
```

### Configuration

| Variable | Default | Purpose |
| :--- | :--- | :--- |
| `DATABASE_URL` | `sqlite:///./yoruba_recipes.db` | Database connection string |
| `SECRET_KEY` | `change-me` | JWT signing key — set this in production |
| `ALLOWED_ORIGINS` | `["*"]` | Permitted CORS origins |
| `MAILERLITE_API_KEY` | empty | Newsletter integration |
| `MAILERLITE_GROUP_ID` | empty | Newsletter group to subscribe into |

## Frontend and admin

Both apps are Vite/React and follow the same commands:

```bash
cd frontend        # or: cd admin
npm install
npm run dev
```

Point them at the API with a `.env` file containing `VITE_API_URL=http://127.0.0.1:8000`.

## Contributing

Community submissions are part of the product: recipes submitted through the public site land in a review queue and are approved or rejected from the admin dashboard, with an audit trail in `submissionlog`.

## License

Released under the [MIT License](LICENSE).
