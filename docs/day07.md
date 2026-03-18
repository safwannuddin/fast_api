# Day 7 — Building a Full CRUD Application

> **Goal:** Combine everything from Days 3–6 to build a complete, database-backed REST API with full Create, Read, Update, Delete functionality.

---

## 🏛️ What We're Building

A **Blog API** with:
- Users (register, list, get by ID, update, delete)
- Posts (create, list, get by ID, update, delete)
- Proper error handling with `HTTPException`
- Pagination support
- Router-based organization

---

## 📁 Project Structure

```
blog_api/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── routers/
│   ├── __init__.py
│   ├── users.py
│   └── posts.py
└── requirements.txt
```

---

## 🔌 database.py

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///./blog.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 🗃️ models.py

```python
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    author = relationship("User", back_populates="posts")
```

---

## 📋 schemas.py

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# ── User Schemas ──────────────────────────────────────────────

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)

class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None

class UserRead(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# ── Post Schemas ──────────────────────────────────────────────

class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)
    published: bool = False

class PostUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    content: Optional[str] = Field(default=None, min_length=1)
    published: Optional[bool] = None

class PostRead(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    updated_at: Optional[datetime]
    author_id: int
    author: UserRead

    class Config:
        from_attributes = True
```

---

## 🔀 routers/users.py

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import get_db
import models, schemas
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )
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


@router.get("/", response_model=List[schemas.UserRead])
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """List all users with pagination."""
    return db.query(models.User).offset(skip).limit(limit).all()


@router.get("/{user_id}", response_model=schemas.UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=schemas.UserRead)
def update_user(user_id: int, updates: schemas.UserUpdate, db: Session = Depends(get_db)):
    """Update a user's profile."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    update_data = updates.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
```

---

## 📝 routers/posts.py

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import models, schemas

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=schemas.PostRead, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, author_id: int, db: Session = Depends(get_db)):
    """Create a new post."""
    # Verify the author exists
    author = db.query(models.User).filter(models.User.id == author_id).first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    
    new_post = models.Post(**post.model_dump(), author_id=author_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/", response_model=List[schemas.PostRead])
def list_posts(
    skip: int = 0,
    limit: int = Query(default=10, le=100),
    published_only: bool = False,
    author_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """List posts with optional filtering and pagination."""
    query = db.query(models.Post)
    
    if published_only:
        query = query.filter(models.Post.published == True)
    
    if author_id:
        query = query.filter(models.Post.author_id == author_id)
    
    return query.order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{post_id}", response_model=schemas.PostRead)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Get a specific post by ID."""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.patch("/{post_id}", response_model=schemas.PostRead)
def update_post(post_id: int, updates: schemas.PostUpdate, db: Session = Depends(get_db)):
    """Update a post."""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    update_data = updates.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(post, field, value)
    
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """Delete a post."""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    db.delete(post)
    db.commit()
```

---

## 🚀 main.py

```python
from fastapi import FastAPI
from database import engine, Base
import models
from routers import users, posts

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blog API",
    description="A complete blogging backend built with FastAPI",
    version="1.0.0"
)

# Register routers
app.include_router(users.router)
app.include_router(posts.router)

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Blog API is running"}
```

Create `routers/__init__.py` (empty file):

```bash
touch routers/__init__.py
```

---

## ⚠️ Error Handling

FastAPI's `HTTPException` sends proper error responses:

```python
from fastapi import HTTPException, status

# 404 Not Found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found"
)

# 400 Bad Request
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Email already taken"
)

# 403 Forbidden
raise HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You don't have permission to perform this action"
)
```

Response format (automatically handled):
```json
{
  "detail": "User not found"
}
```

### Custom Exception Handlers

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "The resource you're looking for doesn't exist"}
    )
```

---

## 🧪 Manual Testing Checklist

Run the app and use `/docs` to test:

```
✅ POST /users          → Create a user
✅ GET  /users          → List all users
✅ GET  /users/1        → Get user 1
✅ PATCH /users/1       → Update user 1's name
✅ DELETE /users/1      → Delete user 1 (cascades to their posts)

✅ POST /posts?author_id=1    → Create a post for user 1
✅ GET  /posts               → List all posts
✅ GET  /posts?published_only=true → Only published posts
✅ GET  /posts?author_id=1   → Posts by user 1
✅ PATCH /posts/1            → Update post 1
✅ DELETE /posts/1           → Delete post 1
```

---

## 📝 Day 7 Exercises

1. Add a `GET /users/{user_id}/posts` endpoint that returns all posts by a specific user.
2. Add a `published_at` datetime field to `Post` that's set automatically when `published` changes to `True`.
3. Add a simple search: `GET /posts?search=fastapi` should search both `title` and `content`.
4. Add pagination metadata to list responses: return `{"data": [...], "total": 50, "page": 1, "pages": 5}`.
5. Add a `PATCH /posts/{post_id}/publish` shortcut endpoint that just sets `published=True`.

---

## ✅ Day 7 Checklist

- [ ] I've built a complete CRUD API with proper router organization
- [ ] I understand how `APIRouter` helps organize routes
- [ ] I can raise `HTTPException` with appropriate status codes
- [ ] I can implement filtering, sorting, and pagination in list endpoints
- [ ] I understand cascade delete (deleting a user removes their posts)

---

⬅️ **Previous:** [Day 6](day06.md) | ➡️ **Next:** [Day 8 — Authentication & Security](day08.md)
