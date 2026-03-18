# Day 9 — Testing FastAPI Applications

> **Goal:** Write automated tests for your FastAPI API using pytest and FastAPI's built-in TestClient. Learn how to test routes, authentication, and database interactions.

---

## 🤔 Why Test Your API?

- **Catch bugs early** — before they reach production
- **Refactor with confidence** — tests tell you if you broke something
- **Documentation** — tests show how your API is supposed to work
- **Required for teams** — CI/CD pipelines run tests automatically

---

## 🛠️ Tools We'll Use

| Tool | Purpose |
|------|---------|
| **pytest** | Python's most popular testing framework |
| **httpx** | HTTP client used by FastAPI's TestClient |
| **TestClient** | Built into FastAPI — sends test requests without a real server |
| **SQLite (in-memory)** | Separate test database that resets between tests |

Install:

```bash
pip install pytest httpx
```

---

## 📁 Project Structure

```
blog_api/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
├── routers/
│   ├── users.py
│   ├── posts.py
│   └── auth.py
└── tests/
    ├── __init__.py
    ├── conftest.py       ← Shared fixtures (test DB, client, auth)
    ├── test_users.py
    ├── test_posts.py
    └── test_auth.py
```

---

## ⚙️ conftest.py — Shared Test Configuration

`conftest.py` is a special pytest file for shared **fixtures** (reusable test setup/teardown):

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db

# Use in-memory SQLite for tests (fresh database each session)
TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create tables before tests, drop them after."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def db():
    """Provide a fresh database session for each test, rolling back after."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db):
    """TestClient that uses the test database."""
    def override_get_db():
        yield db
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


# ── Helper fixtures ───────────────────────────────────────────

@pytest.fixture()
def sample_user(client):
    """Create and return a test user."""
    response = client.post("/users/", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "SecurePass1"
    })
    assert response.status_code == 201
    return response.json()


@pytest.fixture()
def auth_headers(client, sample_user):
    """Return Authorization headers for the test user."""
    response = client.post("/auth/login", data={
        "username": "test@example.com",
        "password": "SecurePass1"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
```

---

## 🧪 tests/test_users.py

```python
# tests/test_users.py
import pytest


class TestCreateUser:
    def test_create_user_success(self, client):
        response = client.post("/users/", json={
            "name": "Alice",
            "email": "alice@example.com",
            "password": "SecurePass1"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Alice"
        assert data["email"] == "alice@example.com"
        assert "id" in data
        assert "password" not in data       # Password must NEVER be in response
        assert "hashed_password" not in data

    def test_create_user_duplicate_email(self, client, sample_user):
        response = client.post("/users/", json={
            "name": "Another User",
            "email": "test@example.com",  # already used by sample_user
            "password": "SecurePass1"
        })
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()

    def test_create_user_invalid_email(self, client):
        response = client.post("/users/", json={
            "name": "Bob",
            "email": "not-an-email",
            "password": "SecurePass1"
        })
        assert response.status_code == 422  # Validation error

    def test_create_user_short_password(self, client):
        response = client.post("/users/", json={
            "name": "Bob",
            "email": "bob@example.com",
            "password": "short"  # less than 8 characters
        })
        assert response.status_code == 422


class TestListUsers:
    def test_list_users(self, client, sample_user):
        response = client.get("/users/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) >= 1

    def test_list_users_pagination(self, client):
        # Create 5 users
        for i in range(5):
            client.post("/users/", json={
                "name": f"User {i}",
                "email": f"user{i}@example.com",
                "password": "SecurePass1"
            })
        
        response = client.get("/users/?limit=3")
        assert response.status_code == 200
        assert len(response.json()) <= 3


class TestGetUser:
    def test_get_existing_user(self, client, sample_user):
        user_id = sample_user["id"]
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["id"] == user_id

    def test_get_nonexistent_user(self, client):
        response = client.get("/users/99999")
        assert response.status_code == 404


class TestUpdateUser:
    def test_update_own_profile(self, client, auth_headers):
        response = client.patch("/users/me", json={"name": "Updated Name"}, 
                                headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Name"

    def test_update_requires_auth(self, client):
        response = client.patch("/users/me", json={"name": "Test"})
        assert response.status_code == 401
```

---

## 🧪 tests/test_auth.py

```python
# tests/test_auth.py
import pytest


class TestLogin:
    def test_login_success(self, client, sample_user):
        response = client.post("/auth/login", data={
            "username": "test@example.com",
            "password": "SecurePass1"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, sample_user):
        response = client.post("/auth/login", data={
            "username": "test@example.com",
            "password": "WrongPassword"
        })
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        response = client.post("/auth/login", data={
            "username": "nobody@example.com",
            "password": "SecurePass1"
        })
        assert response.status_code == 401


class TestProtectedRoutes:
    def test_access_without_token(self, client):
        response = client.get("/users/me")
        assert response.status_code == 401

    def test_access_with_invalid_token(self, client):
        response = client.get("/users/me", 
                              headers={"Authorization": "Bearer invalid.token.here"})
        assert response.status_code == 401

    def test_access_with_valid_token(self, client, auth_headers):
        response = client.get("/users/me", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"
```

---

## 🧪 tests/test_posts.py

```python
# tests/test_posts.py
import pytest


@pytest.fixture()
def sample_post(client, auth_headers):
    """Create a test post."""
    response = client.post("/posts/", json={
        "title": "Test Post",
        "content": "This is test content.",
        "published": False
    }, headers=auth_headers)
    assert response.status_code == 201
    return response.json()


class TestCreatePost:
    def test_create_post_authenticated(self, client, auth_headers):
        response = client.post("/posts/", json={
            "title": "My First Post",
            "content": "Hello world!",
            "published": True
        }, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "My First Post"
        assert data["published"] is True

    def test_create_post_unauthenticated(self, client):
        response = client.post("/posts/", json={
            "title": "My Post",
            "content": "Content"
        })
        assert response.status_code == 401

    def test_create_post_missing_title(self, client, auth_headers):
        response = client.post("/posts/", json={"content": "Content"},
                               headers=auth_headers)
        assert response.status_code == 422


class TestListPosts:
    def test_list_all_posts(self, client, sample_post):
        response = client.get("/posts/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_filter_published_only(self, client, auth_headers):
        # Create unpublished post
        client.post("/posts/", json={"title": "Draft", "content": "...", 
                                     "published": False}, headers=auth_headers)
        # Create published post
        client.post("/posts/", json={"title": "Live", "content": "...",
                                     "published": True}, headers=auth_headers)
        
        response = client.get("/posts/?published_only=true")
        assert response.status_code == 200
        posts = response.json()
        assert all(p["published"] for p in posts)


class TestDeletePost:
    def test_delete_own_post(self, client, auth_headers, sample_post):
        post_id = sample_post["id"]
        response = client.delete(f"/posts/{post_id}", headers=auth_headers)
        assert response.status_code == 204
        
        # Verify it's gone
        get_response = client.get(f"/posts/{post_id}")
        assert get_response.status_code == 404

    def test_cannot_delete_others_post(self, client, sample_post):
        # Create another user
        client.post("/users/", json={
            "name": "Bob", "email": "bob@example.com", "password": "SecurePass1"
        })
        login = client.post("/auth/login", data={
            "username": "bob@example.com", "password": "SecurePass1"
        })
        bob_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
        
        post_id = sample_post["id"]
        response = client.delete(f"/posts/{post_id}", headers=bob_headers)
        assert response.status_code == 403  # Forbidden
```

---

## ▶️ Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific file
pytest tests/test_users.py

# Run a specific class
pytest tests/test_users.py::TestCreateUser

# Run a specific test
pytest tests/test_users.py::TestCreateUser::test_create_user_success

# Run with coverage report
pip install pytest-cov
pytest --cov=. --cov-report=html
# Open htmlcov/index.html in your browser
```

---

## 🎯 Test Best Practices

### 1. AAA Pattern: Arrange, Act, Assert

```python
def test_create_user_success(self, client):
    # Arrange: prepare test data
    user_data = {"name": "Alice", "email": "alice@example.com", "password": "SecurePass1"}
    
    # Act: do the thing you're testing
    response = client.post("/users/", json=user_data)
    
    # Assert: verify the result
    assert response.status_code == 201
    assert response.json()["name"] == "Alice"
```

### 2. Test Edge Cases

Always test:
- ✅ Happy path (valid input, expected output)
- ❌ Missing required fields
- ❌ Invalid field types
- ❌ Boundary values (min/max lengths, ranges)
- ❌ Non-existent resources (404 cases)
- 🔒 Unauthenticated access (401 cases)
- 🚫 Unauthorized access (403 cases)

### 3. One Assertion Per Concept

```python
# ✅ Good — each test checks one thing
def test_response_status(self, client):
    assert client.get("/users/").status_code == 200

def test_response_is_list(self, client):
    assert isinstance(client.get("/users/").json(), list)

# ❌ Avoid — too many things in one test (hard to identify what failed)
def test_everything(self, client):
    r = client.get("/users/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) == 0
    ...
```

---

## 📝 Day 9 Exercises

1. Run the test suite and make sure all tests pass.
2. Write tests for the `POST /posts/` endpoint: what happens with an empty title? Content that's too long?
3. Write a test verifying that password is never included in any user response.
4. Add a test for the pagination: create 20 posts, then verify `GET /posts/?limit=5` returns exactly 5.
5. Generate a coverage report and identify which code paths aren't tested yet. Write tests for them.

---

## ✅ Day 9 Checklist

- [ ] I understand the difference between unit tests and integration tests
- [ ] I've set up a separate in-memory test database
- [ ] I can write fixtures in `conftest.py` and use them across test files
- [ ] I can test both happy paths and error cases
- [ ] I've tested authentication flows (login, token validation, protected routes)
- [ ] I can run tests with `pytest` and understand the output

---

⬅️ **Previous:** [Day 8](day08.md) | ➡️ **Next:** [Day 10 — Deployment & Production Best Practices](day10.md)
