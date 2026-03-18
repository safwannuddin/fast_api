# Day 1 — Introduction to Backend Development & Python Essentials

> **Goal:** Understand what backend development is, how the web works at a high level, and refresh the Python concepts you'll use throughout this course.

---

## 🌐 What Is Backend Development?

When you open a website or mobile app, what you *see* is the **frontend** — buttons, images, forms. But what *powers* it — storing your data, checking your password, sending emails — is the **backend**.

```
User (browser/app)
       │
       │ HTTP request
       ▼
  [ Backend Server ]  ←── Your FastAPI code lives here
       │
       │ SQL queries
       ▼
  [ Database ]
```

As a backend developer, your job is to:
- Receive **requests** from clients (browsers, mobile apps, other services)
- Process those requests (validate data, apply business logic)
- Interact with a **database** to store or retrieve information
- Send back a **response** (usually JSON)

---

## 🧱 Key Backend Concepts

| Term | Meaning |
|------|---------|
| **Server** | A computer (or program) that listens for and responds to requests |
| **Client** | Anything that sends requests (browser, mobile app, another API) |
| **API** | Application Programming Interface — a set of rules for how clients talk to the server |
| **Database** | Persistent storage for your data (users, posts, products…) |
| **JSON** | JavaScript Object Notation — the most common data format for APIs |
| **Endpoint** | A specific URL that your API exposes (e.g., `/users`, `/products/5`) |

---

## 🐍 Python Refresher — Concepts You'll Use Every Day

### 1. Functions & Type Hints

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

print(greet("Alice"))  # Hello, Alice!
```

Type hints (`name: str`, `-> str`) are **optional** in standard Python but FastAPI **requires** them — it uses them to validate and document your API automatically.

### 2. Dictionaries

```python
user = {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
}

print(user["name"])   # Alice
print(user.get("age", 0))  # 0 (default when key is missing)
```

JSON data maps directly to Python dictionaries.

### 3. Lists

```python
users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
]

for user in users:
    print(user["name"])
```

### 4. Classes & `__init__`

```python
class User:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

alice = User(id=1, name="Alice", email="alice@example.com")
print(alice.name)  # Alice
```

FastAPI uses a special kind of class called a **Pydantic model** (Day 5), which builds on this idea.

### 5. Decorators

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before the function")
        result = func(*args, **kwargs)
        print("After the function")
        return result
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
# Before the function
# Hello!
# After the function
```

FastAPI uses decorators like `@app.get("/")` to register routes — you'll see this on Day 3.

### 6. Virtual Environments

Always work inside a virtual environment to keep project dependencies isolated:

```bash
# Create
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Deactivate when done
deactivate
```

### 7. Installing Packages with pip

```bash
pip install fastapi
pip install uvicorn[standard]

# Save dependencies so others can install them too
pip freeze > requirements.txt

# Install from a requirements file
pip install -r requirements.txt
```

---

## 🔧 Setting Up Your Environment

1. **Install Python 3.10+**
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify: `python --version`

2. **Install VS Code**
   - Download from [code.visualstudio.com](https://code.visualstudio.com/)
   - Install the **Python extension** by Microsoft

3. **Create your project folder**

```bash
mkdir my_fastapi_project
cd my_fastapi_project
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
```

4. **Install course dependencies**

```bash
pip install fastapi uvicorn[standard] sqlalchemy pydantic python-jose[cryptography] passlib[bcrypt] python-multipart pytest httpx
```

---

## 📝 Day 1 Exercises

1. Write a Python function `add(a: int, b: int) -> int` that adds two numbers.
2. Create a dictionary representing a book with keys: `title`, `author`, `year`, `pages`.
3. Create a `Book` class with those same attributes and an `__init__` method.
4. Write a decorator `@timer` that prints how long a function takes to run. *(Hint: use `import time`)*
5. Create a virtual environment, install `fastapi`, and run `pip freeze > requirements.txt`.

---

## ✅ Day 1 Checklist

- [ ] I understand what a backend is and what it does
- [ ] I know the difference between client and server
- [ ] I can write Python functions with type hints
- [ ] I understand dictionaries, lists, classes, and decorators
- [ ] I've set up my development environment with a virtual environment

---

➡️ **Next:** [Day 2 — HTTP, REST & APIs](day02.md)
