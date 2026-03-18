# Day 8 — Authentication & Security with JWT

> **Goal:** Implement secure user authentication — password hashing, JWT token generation, and protected routes.

---

## 🔐 Why Authentication?

Without authentication, anyone can access any endpoint. Authentication answers:
- **Who are you?** (Authentication — verifying identity)
- **What are you allowed to do?** (Authorization — verifying permissions)

---

## 🏗️ How JWT Authentication Works

```
1. User logs in with email + password
         │
         ▼
2. Server verifies password against the hashed one in the DB
         │
         ▼
3. Server creates a JWT token containing the user's ID
         │
         ▼
4. Server returns the token to the client
         │
         ▼
5. Client stores the token (localStorage, cookies, etc.)
         │
         ▼
6. Client sends the token in every subsequent request:
   Authorization: Bearer eyJhbGci...
         │
         ▼
7. Server verifies the token and identifies the user
         │
         ▼
8. Server returns the requested data
```

---

## 🔑 What Is a JWT?

A **JSON Web Token (JWT)** is a compact, signed string that encodes a payload:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9   ← Header (algorithm)
.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6  ← Payload (your data)
.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_   ← Signature (tamper-proof)
```

The payload typically contains:
```json
{
  "sub": "1",           ← Subject (usually user ID)
  "email": "alice@example.com",
  "exp": 1742000000     ← Expiration timestamp
}
```

> JWTs are **signed** (not encrypted). Anyone can decode the payload, but nobody can forge the signature without the secret key.

---

## 📦 Installation

```bash
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

- **python-jose** — create and verify JWT tokens
- **passlib[bcrypt]** — hash and verify passwords
- **python-multipart** — required for OAuth2 form data parsing

---

## 🔧 auth.py — Authentication Utilities

```python
# auth.py
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
import models

# ── Configuration ─────────────────────────────────────────────
# In production, load this from environment variables (see Day 10)
SECRET_KEY = "your-super-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ── Password Hashing ──────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ── JWT Token Creation ────────────────────────────────────────
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ── OAuth2 Scheme (reads "Authorization: Bearer <token>" header) ──
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ── Get Current User from Token ───────────────────────────────
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if not user:
        raise credentials_exception
    return user

def get_current_active_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

---

## 🚪 routers/auth.py — Login Endpoint

```python
# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
import models
from auth import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login with email and password to receive a JWT token.
    
    Use the token in the Authorization header for protected endpoints:
    `Authorization: Bearer <your_token>`
    """
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
```

> **`OAuth2PasswordRequestForm`** automatically reads `username` and `password` from form data. FastAPI's `/docs` will display a proper login form.

---

## 🔒 Protecting Routes

Use `Depends(get_current_active_user)` to protect any endpoint:

```python
# routers/users.py (updated)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_active_user
import models, schemas

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=schemas.UserRead)
def get_my_profile(current_user: models.User = Depends(get_current_active_user)):
    """Get the currently authenticated user's profile."""
    return current_user

@router.patch("/me", response_model=schemas.UserRead)
def update_my_profile(
    updates: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update your own profile."""
    update_data = updates.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_account(
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete your own account."""
    db.delete(current_user)
    db.commit()
```

---

## 👑 Authorization — Ownership Checks

Authentication (who you are) ≠ Authorization (what you can do):

```python
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Authorization: only the post's author can delete it
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own posts"
        )
    
    db.delete(post)
    db.commit()
```

---

## 🏷️ Role-Based Access Control (RBAC)

Add a `role` field to your User model and check it:

```python
# models.py — add to User
from sqlalchemy import Enum as SQLEnum
import enum

class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"

class User(Base):
    # ... existing fields ...
    role = Column(SQLEnum(UserRole), default=UserRole.user, nullable=False)

# auth.py — add an admin check dependency
def require_admin(current_user: models.User = Depends(get_current_active_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

# Usage in a route
@router.delete("/admin/users/{user_id}")
def admin_delete_user(
    user_id: int,
    _: models.User = Depends(require_admin),  # only admins
    db: Session = Depends(get_db)
):
    ...
```

---

## 🔄 Token Refresh (Optional)

For a better user experience, implement a refresh token:

```python
# auth.py
def create_refresh_token(data: dict) -> str:
    return create_access_token(data, expires_delta=timedelta(days=7))

# routers/auth.py
class Tokens(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

@router.post("/login", response_model=Tokens)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    
    return {
        "access_token": create_access_token({"sub": str(user.id)}),
        "refresh_token": create_refresh_token({"sub": str(user.id)}),
        "token_type": "bearer"
    }
```

---

## 🧪 Testing Authentication in `/docs`

1. Open `http://127.0.0.1:8000/docs`
2. Find `POST /auth/login` and use the "Try it out" button
3. Enter your email as `username` and your password
4. Copy the `access_token` from the response
5. Click the **🔒 Authorize** button at the top of the page
6. Enter: `Bearer <your_token>` and click Authorize
7. Now protected endpoints work — they'll use your identity

---

## ✅ Updated main.py

```python
from fastapi import FastAPI
from database import engine, Base
import models
from routers import users, posts, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API with Auth")
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
```

---

## 📝 Day 8 Exercises

1. Implement the full auth flow: register → login → use token on a protected endpoint.
2. Add `GET /auth/me` that returns the currently logged-in user (just calls `get_current_active_user`).
3. Update post creation to automatically use `current_user.id` as the `author_id` instead of taking it as a query param.
4. Add authorization to post update/delete: only the author can modify their posts.
5. Add a `role` field and create an admin-only endpoint `GET /admin/users` that lists all users including their hashed passwords (admins only!).

---

## ✅ Day 8 Checklist

- [ ] I understand how JWT authentication works (issue → send → verify)
- [ ] I can hash passwords and verify them with bcrypt
- [ ] I can create and decode JWT tokens
- [ ] I've protected routes with `Depends(get_current_active_user)`
- [ ] I understand the difference between authentication and authorization
- [ ] I've implemented ownership checks (users can only modify their own data)

---

⬅️ **Previous:** [Day 7](day07.md) | ➡️ **Next:** [Day 9 — Testing FastAPI Applications](day09.md)
