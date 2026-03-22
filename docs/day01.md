# Day 1 - Backend Foundations for Absolute Beginners

Goal: Understand what backend development is, how the web works end-to-end, and how FastAPI fits into real software systems.

## 1) What is backend development?
Backend is the part of software that handles data, business logic, security, and communication with databases or external services.

If frontend is what users see, backend is the system that decides:
- what data is valid
- who is allowed to do what
- where data is stored
- what response should be sent back

## 2) How a web request actually works
When a user clicks "Login" in an app:
1. Browser/mobile app sends an HTTP request.
2. Backend receives request at an endpoint.
3. Backend validates input.
4. Backend checks DB or external services.
5. Backend creates response (success/error).
6. Frontend renders response.

This request-response loop is the core of backend engineering.

## 3) Key backend terms you must know
- Client: app that sends request (browser/mobile/postman).
- Server: application that receives request and returns response.
- API: rules/endpoints clients use to talk to server.
- Endpoint: route like /users or /orders/5.
- Database: persistent storage for application data.
- JSON: common data format used in APIs.
- Stateless: server does not remember request context unless stored explicitly.

## 4) FastAPI in the backend ecosystem
FastAPI is a Python framework to build APIs quickly and safely using type hints.

Why teams use FastAPI:
- Fast performance
- Automatic validation
- Automatic docs (/docs and /redoc)
- Clean developer experience

## 5) Python concepts you need before FastAPI
You do not need advanced Python, but you must be comfortable with:
- functions
- dictionaries and lists
- classes
- type hints
- imports and virtual environments

Example:
```python
def add(a: int, b: int) -> int:
    return a + b
```

Type hints become powerful in FastAPI because they drive validation and docs.

## 6) Development environment setup
1. Install Python 3.10+.
2. Create project folder.
3. Create virtual environment.
4. Install dependencies.

Commands (Windows PowerShell):
```bash
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn[standard] pydantic sqlalchemy pytest httpx python-jose[cryptography] passlib[bcrypt]
```

## 7) Beginner mistakes to avoid
- coding without virtual environment
- mixing unrelated code in one file without structure
- ignoring HTTP status codes
- copying code without understanding request flow

## 8) Practical exercise (must do)
1. Write 3 Python functions with type hints.
2. Create one dictionary and one list of dictionaries.
3. Explain in your own words: "what happens when I open a URL in browser?"
4. Install dependencies in a new venv.

## 9) Interview starter questions
1. Difference between frontend and backend?
2. What is an API endpoint?
3. What does stateless mean in web APIs?
4. Why use virtual environments?

## Day 1 completion checklist
- I can explain client-server architecture in simple language.
- I understand request-response cycle.
- I can set up a Python project correctly.
- I know the role of FastAPI in backend development.

Previous: README | Next: Day 2
