# Day 4 — Path Parameters, Query Parameters & Request Body

> **Goal:** Master the three ways to send data to a FastAPI endpoint — path parameters, query parameters, and request bodies.

---

## 📥 Three Ways to Send Data to an API

| Method | Where in HTTP request? | Example |
|--------|----------------------|---------|
| **Path parameter** | In the URL path | `/users/42` |
| **Query parameter** | After `?` in the URL | `/users?page=2&limit=10` |
| **Request body** | In the HTTP body (JSON) | `{"name": "Alice", "age": 30}` |

---

## 1️⃣ Path Parameters

Path parameters are **required** parts of the URL that capture a value.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": f"User {user_id}"}
```

- `{user_id}` in the path becomes the `user_id` parameter in your function
- FastAPI **automatically converts** the string `"42"` to the `int` `42` thanks to the type hint
- If you send a non-integer (e.g., `/users/abc`), FastAPI returns a `422` error automatically

### Multiple Path Parameters

```python
@app.get("/users/{user_id}/posts/{post_id}")
def get_user_post(user_id: int, post_id: int):
    return {
        "user_id": user_id,
        "post_id": post_id,
        "message": f"Post {post_id} by user {user_id}"
    }
```

### Order Matters — Fixed vs Dynamic Routes

```python
# This MUST come BEFORE the dynamic route below
@app.get("/users/me")
def get_current_user():
    return {"user": "the currently logged-in user"}

# This comes AFTER the fixed route
@app.get("/users/{user_id}")
def get_user(user_id: str):
    return {"user_id": user_id}
```

> ⚠️ If `{user_id}` came first, the request `GET /users/me` would match it and `"me"` would be the `user_id`.

### Path Parameter Types

```python
from uuid import UUID

@app.get("/items/{item_id}")
def get_item(item_id: int):         # Only accepts integers
    ...

@app.get("/files/{file_path:path}") # :path allows slashes
def get_file(file_path: str):
    return {"path": file_path}
# GET /files/images/photo.jpg → file_path = "images/photo.jpg"
```

---

## 2️⃣ Query Parameters

Query parameters come **after the `?`** in the URL and are optional by default.

```python
@app.get("/items")
def get_items(skip: int = 0, limit: int = 10):
    fake_items = [{"id": i, "name": f"Item {i}"} for i in range(100)]
    return fake_items[skip : skip + limit]
```

- `GET /items` → returns items 0–9 (using defaults)
- `GET /items?skip=20&limit=5` → returns items 20–24
- `GET /items?limit=50` → returns items 0–49

### Required Query Parameters

If you don't provide a default value, the parameter is **required**:

```python
@app.get("/search")
def search(q: str):  # No default — required!
    return {"query": q, "results": []}

# GET /search         → 422 Error: q is required
# GET /search?q=hello → {"query": "hello", "results": []}
```

### Optional Query Parameters

Use `Optional` from typing (or `| None` in Python 3.10+):

```python
from typing import Optional

@app.get("/items")
def get_items(
    category: Optional[str] = None,
    min_price: float = 0.0,
    max_price: float = 9999.0,
):
    return {
        "category": category,
        "price_range": [min_price, max_price]
    }
```

Or with Python 3.10+ union syntax:

```python
@app.get("/items")
def get_items(category: str | None = None):
    return {"category": category}
```

### Combining Path and Query Parameters

```python
@app.get("/users/{user_id}/posts")
def get_user_posts(
    user_id: int,          # path parameter
    page: int = 1,         # query parameter with default
    published: bool = True # query parameter with default
):
    return {
        "user_id": user_id,
        "page": page,
        "published_only": published
    }

# GET /users/5/posts?page=2&published=false
```

### Boolean Query Parameters

FastAPI accepts `true`, `1`, `on`, `yes` (and their inverses) for booleans:

```
?published=true    → True
?published=1       → True
?published=yes     → True
?published=false   → False
?published=0       → False
?published=no      → False
```

---

## 3️⃣ Request Body

The request body lets clients send structured data (like a JSON object) when creating or updating resources.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: str = ""   # optional field with default
    in_stock: bool = True

@app.post("/items")
def create_item(item: Item):
    return {
        "message": "Item created!",
        "item": item
    }
```

**Request:**
```
POST /items
Content-Type: application/json

{
  "name": "Laptop",
  "price": 999.99,
  "description": "A powerful laptop"
}
```

**Response:**
```json
{
  "message": "Item created!",
  "item": {
    "name": "Laptop",
    "price": 999.99,
    "description": "A powerful laptop",
    "in_stock": true
  }
}
```

FastAPI automatically:
- Reads the JSON body
- Validates the data against the `Item` model
- Returns a helpful `422` error if validation fails

---

## 🔀 Combining All Three

```python
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None

@app.put("/users/{user_id}/items/{item_id}")
def update_item(
    user_id: int,            # path parameter
    item_id: int,            # path parameter
    notify: bool = False,    # query parameter
    item: ItemUpdate = None  # request body
):
    return {
        "user_id": user_id,
        "item_id": item_id,
        "notify_user": notify,
        "update_data": item
    }
```

---

## ✅ Data Validation with `Query()` and `Path()`

For more advanced validation, use `Query()` and `Path()` from fastapi:

```python
from fastapi import FastAPI, Query, Path
from typing import Optional

app = FastAPI()

@app.get("/items/{item_id}")
def get_item(
    item_id: int = Path(
        ...,               # ... means required
        title="Item ID",
        description="The ID of the item to retrieve",
        ge=1,              # greater than or equal to 1
        le=1000            # less than or equal to 1000
    ),
    q: Optional[str] = Query(
        default=None,
        min_length=3,      # minimum string length
        max_length=50,     # maximum string length
        pattern="^[a-z]+$" # regex pattern
    )
):
    return {"item_id": item_id, "q": q}
```

### Validation Options

| Parameter | Applies To | Meaning |
|-----------|-----------|---------|
| `ge` | numbers | ≥ value |
| `gt` | numbers | > value |
| `le` | numbers | ≤ value |
| `lt` | numbers | < value |
| `min_length` | strings | minimum length |
| `max_length` | strings | maximum length |
| `pattern` | strings | regex pattern must match |

---

## 📝 Day 4 Exercises

Build on yesterday's books example and add:

1. **Path parameter:** `GET /books/{book_id}` — returns a specific book, or a 404-style error if not found.

2. **Query parameters:** `GET /books?author=Tolkien&year=1954&limit=5` — filter books by author and/or year, with pagination.

3. **Request body:** `POST /books` — accept a JSON body with `title`, `author`, `year`, and add the book to your list.

4. **Combined:** `PUT /books/{book_id}` — update a book's details using path param + JSON body.

5. **Validation:** Add `Path(ge=1)` to `book_id` and `Query(min_length=2)` to the author search.

---

## ✅ Day 4 Checklist

- [ ] I understand path parameters and how FastAPI converts types automatically
- [ ] I can create both required and optional query parameters
- [ ] I can receive and process a JSON request body using Pydantic models
- [ ] I know how to combine path, query, and body parameters in one endpoint
- [ ] I've used `Query()` and `Path()` for validation

---

⬅️ **Previous:** [Day 3](day03.md) | ➡️ **Next:** [Day 5 — Data Validation with Pydantic](day05.md)
