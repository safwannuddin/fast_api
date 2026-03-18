# Day 5 — Data Validation with Pydantic

> **Goal:** Master Pydantic models for data validation, serialization, and creating clean request/response schemas.

---

## 🤔 What Is Pydantic?

Pydantic is a Python library for **data validation using type hints**. It's built into FastAPI and does the heavy lifting of:

1. Validating that incoming data has the right types and format
2. Converting data (e.g., string `"42"` → int `42`)
3. Serializing Python objects to JSON
4. Generating JSON Schema (used by the auto docs)

---

## 🏗️ Defining a Pydantic Model

A Pydantic model is a Python class that inherits from `BaseModel`:

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    age: int
    is_active: bool = True  # optional field with default

# Creating an instance
user = User(id=1, name="Alice", email="alice@example.com", age=30)
print(user.name)      # Alice
print(user.is_active) # True
print(user.model_dump())  # {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'age': 30, 'is_active': True}
```

### What Pydantic Does Automatically

```python
# Type coercion: Pydantic converts compatible types
user = User(id="1", name="Alice", email="alice@example.com", age="30")
print(type(user.id))  # <class 'int'> — "1" was coerced to 1

# Validation error for incompatible types
try:
    bad_user = User(id="not-a-number", name="Alice", email="x@y.com", age=30)
except Exception as e:
    print(e)  # id: Input should be a valid integer
```

---

## 📋 Optional Fields & Default Values

```python
from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str                          # required
    price: float                       # required
    description: Optional[str] = None # optional, defaults to None
    tax: float = 0.1                   # optional, defaults to 0.1
    tags: list[str] = []               # optional, defaults to empty list
```

> **Note:** In Python 3.10+, you can use `str | None` instead of `Optional[str]`.

---

## ✅ Built-in Validators with `Field()`

`Field()` lets you add validation rules directly in the model:

```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class User(BaseModel):
    username: str = Field(
        ...,               # required (... is shorthand for "no default")
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9_]+$"  # alphanumeric + underscore only
    )
    email: EmailStr        # validates email format automatically
    age: int = Field(ge=0, le=120)  # 0 ≤ age ≤ 120
    bio: Optional[str] = Field(default=None, max_length=500)
    score: float = Field(default=0.0, ge=0.0, le=10.0)
```

> To use `EmailStr`, install: `pip install pydantic[email]`

---

## 🔗 Nested Models

Models can contain other models:

```python
from pydantic import BaseModel
from typing import Optional

class Address(BaseModel):
    street: str
    city: str
    country: str
    zip_code: str

class User(BaseModel):
    id: int
    name: str
    email: str
    address: Optional[Address] = None

# Usage
user = User(
    id=1,
    name="Alice",
    email="alice@example.com",
    address={
        "street": "123 Main St",
        "city": "New York",
        "country": "USA",
        "zip_code": "10001"
    }
)
print(user.address.city)  # New York
```

### Lists of Models

```python
class Post(BaseModel):
    title: str
    content: str

class UserWithPosts(BaseModel):
    id: int
    name: str
    posts: list[Post] = []
```

---

## 🎭 Request vs Response Schemas

A best practice is to have **separate schemas** for creating, reading, and updating resources:

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Schema for creating a user (no id — DB generates it)
class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)  # will be hashed before storing

# Schema for reading a user (id included, no password!)
class UserRead(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # allows reading from ORM models (Day 6)

# Schema for updating a user (all fields optional)
class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
```

### Using Schemas in FastAPI

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/users", response_model=UserRead)
def create_user(user: UserCreate):
    # user.password would be hashed here (Day 8)
    # ... save to database ...
    return {
        "id": 1,
        "name": user.name,
        "email": user.email,
        "is_active": True,
        "created_at": datetime.now()
    }
```

The `response_model=UserRead` tells FastAPI to:
- Filter the response to only include fields defined in `UserRead` (e.g., hide `password`)
- Validate the response data
- Show the response schema in `/docs`

---

## 🔧 Custom Validators

Use `@field_validator` to write custom validation logic:

```python
from pydantic import BaseModel, field_validator, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be empty or whitespace")
        return v.title()  # Convert "alice smith" → "Alice Smith"

    @field_validator("password")
    @classmethod
    def password_must_be_strong(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v
```

### Model-Level Validator (cross-field)

```python
from pydantic import BaseModel, model_validator

class UserCreate(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def passwords_must_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
```

---

## 📤 Serialization

```python
user = UserRead(id=1, name="Alice", email="alice@example.com", 
                is_active=True, created_at=datetime.now())

# To dict
user.model_dump()
# {'id': 1, 'name': 'Alice', ...}

# To JSON string
user.model_dump_json()
# '{"id":1,"name":"Alice",...}'

# Exclude None values
user.model_dump(exclude_none=True)

# Exclude specific fields
user.model_dump(exclude={"created_at"})

# Include only specific fields
user.model_dump(include={"id", "name"})
```

---

## 🗂️ Using Enums

Use Python's `Enum` for fields that can only take specific values:

```python
from enum import Enum
from pydantic import BaseModel

class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    moderator = "moderator"

class User(BaseModel):
    name: str
    role: UserRole = UserRole.user

# FastAPI will validate that only "admin", "user", or "moderator" are accepted
# The API docs will show a dropdown with these options!
```

---

## 🔄 Putting It All Together

Here's a complete example combining everything:

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from enum import Enum
from datetime import datetime

app = FastAPI()

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)
    role: UserRole = UserRole.user

    @field_validator("name")
    @classmethod
    def capitalize_name(cls, v: str) -> str:
        return v.title()

class UserRead(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True

# Simulated database
users_db = []
next_id = 1

@app.post("/users", response_model=UserRead, status_code=201)
def create_user(user: UserCreate):
    global next_id
    new_user = {
        "id": next_id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "created_at": datetime.now()
    }
    users_db.append(new_user)
    next_id += 1
    return new_user

@app.get("/users", response_model=list[UserRead])
def list_users():
    return users_db
```

---

## 📝 Day 5 Exercises

1. Create a `Product` model with: `name` (required, 1–100 chars), `price` (required, must be positive), `category` (an Enum: `electronics`, `clothing`, `food`), `description` (optional), `stock` (int, defaults to 0).

2. Create separate `ProductCreate`, `ProductRead`, and `ProductUpdate` schemas.

3. Add a custom validator that ensures product names don't contain special characters.

4. Build a full products API with `POST /products` (returns `ProductRead`), `GET /products`, and `GET /products/{id}`.

5. Add a nested model: each product can have a `Supplier` with `name`, `email`, and `country`.

---

## ✅ Day 5 Checklist

- [ ] I can create Pydantic models with required and optional fields
- [ ] I can use `Field()` for validation rules (min/max length, ranges)
- [ ] I understand the difference between request and response schemas
- [ ] I can use `response_model` in FastAPI to control response shape
- [ ] I can write `@field_validator` and `@model_validator` functions
- [ ] I know how to use Enums for fixed-value fields

---

⬅️ **Previous:** [Day 4](day04.md) | ➡️ **Next:** [Day 6 — Database Integration with SQLAlchemy](day06.md)
