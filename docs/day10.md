# Day 10 — Deployment & Production Best Practices

> **Goal:** Prepare your FastAPI application for the real world — environment variables, Docker, database migrations, and deploying to a cloud platform.

---

## 🌍 What Changes in Production?

| Development | Production |
|------------|-----------|
| SQLite (file) | PostgreSQL (dedicated server) |
| Secret key in code | Secret key in environment variable |
| `--reload` flag | Process manager (gunicorn) |
| Local machine | Cloud server |
| Any port | Port 80/443 |
| No HTTPS | HTTPS required |

---

## 1️⃣ Environment Variables — Never Hardcode Secrets

Never put secrets (passwords, API keys, secret keys) directly in your code. Use environment variables instead.

### Installing python-dotenv

```bash
pip install python-dotenv
```

### .env file (never commit this!)

```bash
# .env
DATABASE_URL=postgresql://user:password@localhost/blog_db
SECRET_KEY=super-long-random-secret-key-at-least-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=false
ALLOWED_ORIGINS=https://yourfrontend.com,https://api.yoursite.com
```

### .gitignore — Protect Your Secrets

```gitignore
# .gitignore
.env
*.db
__pycache__/
*.pyc
.pytest_cache/
venv/
htmlcov/
```

> 🚨 **NEVER** commit `.env` to git. Your secrets could be exposed publicly.

### config.py — Load Environment Variables

```python
# config.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    debug: bool = False
    allowed_origins: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

Install:

```bash
pip install pydantic-settings
```

### Using Settings in Your App

```python
# database.py
from config import settings

engine = create_engine(settings.database_url)

# auth.py
from config import settings

def create_access_token(data: dict):
    ...
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
```

---

## 2️⃣ CORS — Allow Your Frontend to Call Your API

CORS (Cross-Origin Resource Sharing) lets browsers make requests from one domain to another:

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)
```

For development only (allow everything):

```python
allow_origins=["*"]  # Never use this in production!
```

---

## 3️⃣ Database Migrations with Alembic

As your app evolves, you'll need to update the database schema. Alembic manages these changes safely.

```bash
pip install alembic
alembic init alembic
```

### Configure alembic.ini

Change the `sqlalchemy.url` line:

```ini
# alembic.ini
sqlalchemy.url = %(DATABASE_URL)s
```

### alembic/env.py — Connect to Your Models

```python
# alembic/env.py (key parts to update)
from config import settings
from database import Base
import models  # Import all models so Alembic knows about them

# Replace the sqlalchemy.url line
config.set_main_option("sqlalchemy.url", settings.database_url)

# Use your Base's metadata for auto-generation
target_metadata = Base.metadata
```

### Creating and Running Migrations

```bash
# Auto-generate a migration from model changes
alembic revision --autogenerate -m "add role column to users"

# Apply migrations
alembic upgrade head

# Roll back one migration
alembic downgrade -1

# Show migration history
alembic history
```

> Each migration generates a file in `alembic/versions/` — commit these to git!

---

## 4️⃣ Docker — Containerize Your App

Docker packages your app with all its dependencies so it runs identically everywhere.

### Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies (done first so Docker can cache this layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port uvicorn will listen on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### .dockerignore

```
.env
.git
__pycache__
*.pyc
*.db
venv/
.pytest_cache/
htmlcov/
```

### docker-compose.yml — App + Database

```yaml
# docker-compose.yml
version: "3.9"

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: bloguser
      POSTGRES_PASSWORD: blogpassword
      POSTGRES_DB: blog_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://bloguser:blogpassword@db/blog_db
      SECRET_KEY: your-production-secret-key-here
    depends_on:
      - db
    command: >
      sh -c "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"

volumes:
  postgres_data:
```

### Running with Docker Compose

```bash
# Build and start
docker-compose up --build

# Run in background
docker-compose up -d

# Stop
docker-compose down

# Stop and remove volumes (wipes the database!)
docker-compose down -v
```

---

## 5️⃣ Switching from SQLite to PostgreSQL

```bash
pip install psycopg2-binary
```

Update your `.env`:

```bash
DATABASE_URL=postgresql://bloguser:blogpassword@localhost/blog_db
```

Remove the `connect_args` from `database.py` (SQLite-only):

```python
# database.py
engine = create_engine(settings.database_url)  # No connect_args needed for PostgreSQL
```

---

## 6️⃣ Production Server — Gunicorn + Uvicorn Workers

For production, use Gunicorn (a process manager) with Uvicorn workers:

```bash
pip install gunicorn
```

```bash
# Start with 4 worker processes
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

Update your Dockerfile for production:

```dockerfile
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

---

## 7️⃣ Deploying to the Cloud

### Option A: Railway (Easiest for Beginners)

1. Push your code to GitHub
2. Go to [railway.app](https://railway.app) and sign in with GitHub
3. Click **New Project** → **Deploy from GitHub repo**
4. Add a **PostgreSQL** service (Railway provides it free)
5. Copy the `DATABASE_URL` from the PostgreSQL service into your service's environment variables
6. Add your other environment variables (`SECRET_KEY`, etc.)
7. Railway automatically detects Python and deploys! 🎉

### Option B: Render

1. Push to GitHub
2. Go to [render.com](https://render.com)
3. Create a **Web Service** → connect your GitHub repo
4. Set **Build Command:** `pip install -r requirements.txt`
5. Set **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add a **PostgreSQL** database from Render's dashboard
7. Set environment variables in the Render dashboard

### Option C: VPS (DigitalOcean / Linode / AWS EC2)

```bash
# On your server:
# 1. Install Docker
curl -fsSL https://get.docker.com | sh

# 2. Clone your repo
git clone https://github.com/yourusername/blog_api.git
cd blog_api

# 3. Create .env with production values
nano .env

# 4. Start with Docker Compose
docker-compose up -d

# 5. Set up Nginx as a reverse proxy (port 80/443 → port 8000)
# 6. Get a free SSL certificate with Let's Encrypt
```

---

## 8️⃣ Security Hardening Checklist

```python
# main.py — production-ready configuration

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI(
    docs_url="/docs" if settings.debug else None,  # Hide docs in production
    redoc_url="/redoc" if settings.debug else None
)

# Only allow specific hosts (prevents host header injection)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["yourapi.com", "www.yourapi.com"]
)

# CORS: only allow your frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)
```

**Security Checklist:**

- [ ] All secrets are in environment variables (never in code)
- [ ] `.env` is in `.gitignore`
- [ ] Passwords are hashed with bcrypt
- [ ] JWT secret key is long and random (use `openssl rand -hex 32`)
- [ ] Tokens have a reasonable expiration (30 minutes for access tokens)
- [ ] HTTPS is enabled (SSL certificate)
- [ ] CORS is restricted to known origins
- [ ] `/docs` is disabled in production (or password-protected)
- [ ] Database is not publicly accessible (only accessible by the app)
- [ ] Input validation is enforced (Pydantic handles this)

---

## 9️⃣ Monitoring & Logging

```python
# main.py
import logging
import time
from fastapi import Request

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} "
        f"→ {response.status_code} ({duration:.3f}s)"
    )
    return response
```

---

## 🎯 Your 10-Day Project Challenge

Now that you've learned everything, build a complete project from scratch! Here are some ideas:

### 🛒 E-Commerce API
- Products (CRUD + categories + stock management)
- Users + authentication
- Shopping cart
- Orders
- Product search and filtering

### 📝 Task Manager API
- Users + authentication
- Projects (CRUD)
- Tasks (CRUD, assign to users, due dates, priority)
- Comments on tasks

### 📰 News Aggregator API
- Articles (CRUD)
- Categories/tags
- Comments
- User subscriptions
- Search functionality

---

## 📝 Day 10 Exercises

1. Move all your secrets to `.env` and load them with `pydantic-settings`.
2. Add CORS middleware allowing `http://localhost:3000` (as if you had a React frontend).
3. Create a `Dockerfile` and build the image: `docker build -t blog-api .`
4. Run the container: `docker run -p 8000:8000 --env-file .env blog-api`
5. Set up Alembic and create your first migration.
6. Deploy your app to Railway or Render (free tier available).

---

## ✅ Day 10 Checklist

- [ ] I store secrets in environment variables, never in code
- [ ] I've containerized my app with Docker
- [ ] I understand how database migrations work with Alembic
- [ ] I've switched from SQLite to PostgreSQL
- [ ] I've deployed my app to a cloud platform
- [ ] I understand the key security practices for production APIs

---

## 🏁 Congratulations — You've Completed the Course!

Here's a summary of what you've learned in 10 days:

| Day | Achievement |
|-----|-------------|
| 1 | ✅ Backend concepts & Python recap |
| 2 | ✅ HTTP, REST, and API design |
| 3 | ✅ FastAPI setup, routing, and auto-docs |
| 4 | ✅ Path params, query params, request body |
| 5 | ✅ Pydantic validation & schemas |
| 6 | ✅ Database with SQLAlchemy |
| 7 | ✅ Full CRUD application |
| 8 | ✅ JWT Authentication & Authorization |
| 9 | ✅ Testing with pytest |
| 10 | ✅ Docker, migrations & deployment |

### 🚀 Where to Go Next

- **Official FastAPI docs:** [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **SQLAlchemy 2.0 docs:** [docs.sqlalchemy.org](https://docs.sqlalchemy.org)
- **Learn async Python:** Look into `asyncio`, `async def`, `await`
- **Learn GraphQL:** [Strawberry](https://strawberry.rocks/) — GraphQL for FastAPI
- **Learn WebSockets:** FastAPI supports them natively
- **Explore microservices:** Message queues (Redis, RabbitMQ), service discovery
- **Practice:** Build real projects, contribute to open source

---

⬅️ **Previous:** [Day 9](day09.md) | 🏠 **Back to Start:** [README](../README.md)
