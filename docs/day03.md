# Day 3 — FastAPI Setup & Your First API

> **Goal:** Install FastAPI, understand its core concepts, create your first working API endpoints, and explore the automatic interactive documentation.

---

## ⚡ Why FastAPI?

FastAPI is a modern Python web framework for building APIs. Here's why it's excellent:

| Feature | Benefit |
|---------|---------|
| **Fast** | One of the fastest Python frameworks (on par with Node.js) |
| **Automatic docs** | Interactive API docs generated automatically (Swagger UI & ReDoc) |
| **Type-based validation** | Uses Python type hints to validate data automatically |
| **Easy to learn** | Clean, intuitive syntax |
| **Production-ready** | Used by Microsoft, Uber, Netflix, and more |

---

## 📦 Installation

Make sure your virtual environment is active, then:

```bash
pip install fastapi uvicorn[standard]
```

- **fastapi** — the framework itself
- **uvicorn** — an ASGI server that runs your FastAPI app (like the engine for your car)

---

## 🚀 Your First FastAPI Application

Create a file called `main.py`:

```python
from fastapi import FastAPI

# Create the FastAPI application instance
app = FastAPI()

# Define a route: GET /
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
```

Run it:

```bash
uvicorn main:app --reload
```

- `main` → the filename (`main.py`)
- `app` → the FastAPI instance variable name
- `--reload` → automatically restart when you save changes (dev mode only)

Open your browser and visit:
- **http://127.0.0.1:8000** → your API response
- **http://127.0.0.1:8000/docs** → interactive Swagger UI ✨
- **http://127.0.0.1:8000/redoc** → alternative ReDoc documentation

---

## 🗺️ Understanding Routes

A **route** (or endpoint) connects a URL path and HTTP method to a Python function:

```python
@app.get("/")          # HTTP method + path
def read_root():       # handler function (called when route is hit)
    return {...}       # response data (automatically converted to JSON)
```

FastAPI provides decorators for all HTTP methods:

```python
@app.get("/items")      # Read
@app.post("/items")     # Create
@app.put("/items/{id}") # Replace
@app.patch("/items/{id}") # Partially update
@app.delete("/items/{id}") # Delete
```

---

## 📖 Expanding Our API

Let's build a simple items API step by step:

```python
from fastapi import FastAPI

app = FastAPI(
    title="My First API",
    description="Learning FastAPI step by step",
    version="1.0.0"
)

# In-memory "database" (a list of dicts)
items = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Mouse",  "price": 29.99},
    {"id": 3, "name": "Keyboard", "price": 79.99},
]

@app.get("/")
def root():
    return {"message": "Welcome to My First API!"}

@app.get("/items")
def get_all_items():
    return items

@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}
```

Save and visit **http://127.0.0.1:8000/docs** — FastAPI automatically:
- Lists all your routes
- Shows what parameters they accept
- Lets you test them right in the browser (click "Try it out")

---

## 🔍 Interactive Documentation

FastAPI auto-generates two documentation UIs from your code:

### Swagger UI (`/docs`)

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

- Click any endpoint to expand it
- Click **"Try it out"** to test it
- Fill in parameters and click **"Execute"**
- See the real response

### ReDoc (`/redoc`)

- Cleaner, read-only documentation
- Great for sharing with frontend developers
- Auto-generated from your code + docstrings

### OpenAPI Schema (`/openapi.json`)

FastAPI also exposes the raw OpenAPI spec at `/openapi.json`. This is used by the docs UIs and can be imported into Postman.

---

## 🏷️ Adding Metadata

You can enrich your docs with titles, descriptions, and tags:

```python
from fastapi import FastAPI

app = FastAPI(
    title="Items API",
    description="""
## Items API

Manage your items easily.

### Features
- Create items
- Read items  
- Update items
- Delete items
""",
    version="0.1.0",
    contact={
        "name": "Your Name",
        "email": "you@example.com",
    }
)

@app.get("/items", tags=["items"], summary="List all items")
def get_items():
    """
    Returns a list of all items in the store.
    
    Each item has:
    - **id**: unique identifier
    - **name**: item name
    - **price**: price in USD
    """
    return items
```

---

## ⚙️ Async Support

FastAPI supports both regular (`def`) and async (`async def`) functions:

```python
import asyncio

@app.get("/sync")
def sync_endpoint():
    # Regular function - fine for most use cases
    return {"type": "sync"}

@app.get("/async")
async def async_endpoint():
    # Async function - use when calling async libraries (databases, HTTP clients)
    await asyncio.sleep(0)  # simulate async work
    return {"type": "async"}
```

**When to use `async def`:**
- When using async database drivers (e.g., `asyncpg`, `databases`)
- When making HTTP requests with `httpx` or `aiohttp`
- When using async file I/O

**When to use `def`:**
- When using standard synchronous libraries (e.g., `sqlalchemy` synchronous ORM)
- For simple logic without I/O

> For this course, we'll mostly use regular `def` to keep things simple. Both work perfectly with FastAPI.

---

## 🛠️ Project Structure (Best Practice)

As your project grows, organize it like this:

```
my_fastapi_project/
├── main.py            ← App entry point
├── requirements.txt
├── routers/
│   ├── __init__.py
│   ├── items.py       ← Item-related routes
│   └── users.py       ← User-related routes
├── models/
│   ├── __init__.py
│   └── item.py        ← Pydantic models / DB models
├── database.py        ← DB connection setup
└── tests/
    └── test_main.py
```

We'll gradually build toward this structure over the next 7 days.

---

## 📝 Day 3 Exercises

1. Create `main.py` and run the FastAPI hello world app. Visit `/docs` and explore.

2. Add these endpoints to your app:
   - `GET /` → returns `{"message": "Hello!"}`
   - `GET /about` → returns info about the API (your name, version, etc.)
   - `GET /health` → returns `{"status": "ok"}` (health check endpoint)

3. Add a list of 5 books (with `id`, `title`, `author`, `year`) and create:
   - `GET /books` → return all books
   - `GET /books/{book_id}` → return a single book by ID

4. Add docstrings to your endpoint functions and see how they appear in `/docs`.

5. Add metadata to your `FastAPI()` instance (title, description, version).

---

## ✅ Day 3 Checklist

- [ ] I've installed FastAPI and uvicorn
- [ ] I can create and run a FastAPI application
- [ ] I understand how `@app.get()` and other decorators work
- [ ] I've explored the auto-generated `/docs` and `/redoc` pages
- [ ] I know the difference between `def` and `async def` in FastAPI

---

⬅️ **Previous:** [Day 2](day02.md) | ➡️ **Next:** [Day 4 — Path Params, Query Params & Request Body](day04.md)
