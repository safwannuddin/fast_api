# Day 6 — Database Integration with SQLAlchemy

> **Goal:** Connect FastAPI to a real database, define database models with SQLAlchemy, and understand how to manage database sessions.

---

## 🗄️ Why Do We Need a Database?

Our in-memory lists from previous days lose all data when the server restarts. A database **persists data** between restarts and supports:
- Multiple concurrent users
- Complex queries (filtering, sorting, joining tables)
- Transactions (all-or-nothing operations)

---

## 📚 Key Concepts

| Term | Meaning |
|------|---------|
| **ORM** | Object-Relational Mapper — lets you interact with a DB using Python objects instead of raw SQL |
| **SQLAlchemy** | The most popular Python ORM |
| **Model** | A Python class that maps to a database table |
| **Session** | A "unit of work" — you interact with the DB through a session |
| **Migration** | A script that updates the database schema as your code changes |

---

## 🚀 Setup

```bash
pip install sqlalchemy
```

For this course we'll use **SQLite** (no server setup needed — it's just a file). On Day 10, you'll learn to switch to PostgreSQL for production.

---

## 📁 Project Structure for Day 6+

```
my_fastapi_project/
├── main.py
├── database.py      ← DB connection & session
├── models.py        ← SQLAlchemy table models
├── schemas.py       ← Pydantic request/response schemas
└── requirements.txt
```

---

## 🔌 database.py — Connecting to the Database

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# SQLite: stores data in a file called "app.db" in the current directory
DATABASE_URL = "sqlite:///./app.db"

# PostgreSQL (for production — we'll use SQLite for now):
# DATABASE_URL = "postgresql://user:password@localhost/dbname"

# create_engine: manages the connection to the database
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # needed for SQLite only
)

# sessionmaker: creates new Session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all our models
class Base(DeclarativeBase):
    pass

# Dependency: provides a DB session to each request, then closes it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 🏗️ models.py — Defining Database Tables

```python
# models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship: one user has many posts
    posts = relationship("Post", back_populates="author")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Foreign key: links each post to a user
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship: each post belongs to one user
    author = relationship("User", back_populates="posts")
```

### Column Types Reference

| SQLAlchemy Type | Python Type | SQL Type |
|----------------|-------------|---------|
| `Integer` | `int` | INTEGER |
| `String` | `str` | VARCHAR |
| `Float` | `float` | FLOAT |
| `Boolean` | `bool` | BOOLEAN |
| `DateTime` | `datetime` | DATETIME |
| `Text` | `str` | TEXT (unlimited) |
| `JSON` | `dict`/`list` | JSON |

### Column Options

```python
Column(
    Integer,
    primary_key=True,   # This is the primary key
    index=True,          # Create a DB index for faster lookups
    unique=True,         # Values must be unique
    nullable=False,      # Cannot be NULL
    default=0,           # Python-level default
    server_default="0"   # Database-level default
)
```

---

## 🔄 Creating the Tables

Add this to `main.py`:

```python
# main.py
from fastapi import FastAPI
from database import engine, Base
import models  # Import models so SQLAlchemy knows about them

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()
```

When you run the app, SQLAlchemy automatically creates the tables if they don't exist.

---

## 💉 Dependency Injection — Using the Database

FastAPI's `Depends()` handles injecting the database session into your route functions:

```python
# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
```

**How `Depends(get_db)` works:**
1. FastAPI calls `get_db()` before your function runs
2. `get_db` opens a DB session and `yield`s it
3. Your function receives the session as `db`
4. After your function returns, `get_db` closes the session (even if there's an error)

---

## 🔍 Basic Database Queries

```python
from sqlalchemy.orm import Session
import models

def examples(db: Session):
    # Get all records
    users = db.query(models.User).all()

    # Filter
    active_users = db.query(models.User).filter(models.User.is_active == True).all()

    # Get one by primary key
    user = db.query(models.User).filter(models.User.id == 1).first()

    # Get by any column
    user = db.query(models.User).filter(models.User.email == "alice@example.com").first()

    # Ordering
    users = db.query(models.User).order_by(models.User.name).all()

    # Limit and offset (pagination)
    users = db.query(models.User).offset(10).limit(5).all()

    # Count
    count = db.query(models.User).count()

    # Multiple filters (AND)
    users = db.query(models.User).filter(
        models.User.is_active == True,
        models.User.name.contains("Alice")
    ).all()
```

---

## ✏️ Create, Update, Delete

```python
# CREATE
def create_user(db: Session, name: str, email: str, hashed_password: str):
    new_user = models.User(
        name=name,
        email=email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()          # Save to database
    db.refresh(new_user) # Refresh to get DB-generated fields (id, created_at)
    return new_user


# UPDATE
def update_user(db: Session, user_id: int, new_name: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.name = new_name
        db.commit()
        db.refresh(user)
    return user


# DELETE
def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user
```

---

## 🔗 Querying Relationships

```python
# Get a user with their posts (SQLAlchemy loads relationships automatically)
user = db.query(models.User).filter(models.User.id == 1).first()
print(user.posts)  # List of Post objects

# Get posts with their author
post = db.query(models.Post).filter(models.Post.id == 1).first()
print(post.author.name)  # Author's name

# Filter posts by author
posts = db.query(models.Post)\
          .filter(models.Post.author_id == user_id)\
          .order_by(models.Post.created_at.desc())\
          .all()
```

---

## 🗂️ schemas.py — Pydantic Schemas for the API

```python
# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Lets Pydantic read from SQLAlchemy models

class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = False

class PostRead(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    author_id: int

    class Config:
        from_attributes = True
```

> ⚠️ **SQLAlchemy models** (in `models.py`) define *database tables*.
> **Pydantic schemas** (in `schemas.py`) define *API request/response shapes*.
> They are different things!

---

## 🔧 Putting It All Together

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models, schemas
from passlib.context import CryptContext  # for Day 8

Base.metadata.create_all(bind=engine)
app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/users", response_model=schemas.UserRead, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = pwd_context.hash(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users", response_model=list[schemas.UserRead])
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.User).offset(skip).limit(limit).all()

@app.get("/users/{user_id}", response_model=schemas.UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

---

## 📝 Day 6 Exercises

1. Set up `database.py`, `models.py`, `schemas.py`, and `main.py` as shown above.
2. Run `uvicorn main:app --reload` and verify the `app.db` file is created.
3. Use `/docs` to create a few users and verify they're persisted after a restart.
4. Add a `Category` model with `id` and `name`. Add a `category_id` foreign key to your items/posts.
5. Write a query that returns only posts where `published=True`, ordered by newest first.

---

## ✅ Day 6 Checklist

- [ ] I understand the difference between SQLAlchemy models and Pydantic schemas
- [ ] I can set up a SQLite database with SQLAlchemy
- [ ] I can define database models with columns and relationships
- [ ] I understand how `get_db` and `Depends()` work together
- [ ] I can perform basic CRUD operations using SQLAlchemy sessions

---

⬅️ **Previous:** [Day 5](day05.md) | ➡️ **Next:** [Day 7 — Full CRUD Application](day07.md)
