# Day 3 - FastAPI Core: From First App to Clean Routing

Goal: Build your first correct FastAPI service and understand how request handling works under the hood.

## 1) FastAPI lifecycle at high level
When request reaches FastAPI:
1. Router matches path + method.
2. Parameters are parsed and validated.
3. Dependencies are resolved.
4. Endpoint function executes.
5. Response is serialized to JSON.

## 2) Minimal app
```python
from fastapi import FastAPI

app = FastAPI(title="Learning API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "API running"}
```

Run:
```bash
uvicorn main:app --reload
```

## 3) Why /docs is important
Swagger docs in FastAPI are auto-generated from your code.
This gives:
- quick API testing
- shared contract with frontend
- fewer documentation mismatches

## 4) Route patterns and order
Static routes should usually be defined before dynamic routes that might conflict.

Example:
```python
@app.get("/users/me")
def me():
    return {"user": "current"}

@app.get("/users/{user_id}")
def by_id(user_id: int):
    return {"id": user_id}
```

## 5) Response standards
Always be intentional with status codes:
- GET success: 200
- POST created: 201
- DELETE success without body: 204

And be consistent in error format (FastAPI default detail is good start).

## 6) Sync vs async in FastAPI
- Use `def` when using sync DB libraries or CPU-light work.
- Use `async def` when calling async I/O libraries.

Do not force async everywhere without reason.

## 7) Better beginner project structure
Start simple but separate concerns early:
- main.py: app startup and router registration
- routers/: route modules
- schemas.py: Pydantic schemas
- models.py/database.py: from Day 6 onward

## 8) Hands-on coding tasks
1. Build routes:
   - GET /
   - GET /health
   - GET /about
2. Build resource routes:
   - GET /items
   - GET /items/{id}
   - POST /items
3. Verify all in /docs.
4. Return 404 for missing item.

## 9) Debug drills
- Hit unknown route and inspect 404.
- Send invalid path param type and inspect 422.
- Trigger validation error in POST body.

## 10) Interview questions
1. What advantages does FastAPI provide over plain Flask for API contracts?
2. Explain what happens when FastAPI receives an invalid path parameter.
3. When would you use async def in API endpoints?
4. Why are auto-generated docs useful in teams?

## Day 3 completion checklist
- I can run FastAPI locally and test through /docs.
- I can design simple routes correctly.
- I understand validation and error behavior basics.
- I can explain FastAPI request lifecycle at beginner level.

Previous: Day 2 | Next: Day 4
