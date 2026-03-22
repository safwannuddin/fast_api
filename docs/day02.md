# Day 2 - HTTP and REST Deep Dive for Beginners

Goal: Understand exactly how APIs communicate using HTTP and how to design clean REST endpoints.

## 1) HTTP basics
HTTP is the protocol used between client and server.
Every exchange has:
- request: method + URL + headers + optional body
- response: status code + headers + optional body

## 2) Request anatomy
Example request:
```http
POST /users HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "Safwan",
  "email": "safwan@example.com"
}
```

Key parts:
- Method: action (GET, POST, PUT, PATCH, DELETE)
- Path: resource target
- Headers: metadata
- Body: payload for create/update

## 3) Response anatomy
Example response:
```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": 1,
  "name": "Safwan"
}
```

## 4) Status codes you must master
- 200 OK: request succeeded
- 201 Created: new resource created
- 204 No Content: success, no response body
- 400 Bad Request: malformed request
- 401 Unauthorized: missing/invalid auth
- 403 Forbidden: authenticated but not allowed
- 404 Not Found: resource missing
- 409 Conflict: duplicate or state conflict
- 422 Unprocessable Entity: validation failure
- 500 Internal Server Error: server bug

## 5) REST design fundamentals
Use nouns for resources:
- GET /users
- GET /users/1
- POST /users
- PATCH /users/1
- DELETE /users/1

Avoid action-style URLs:
- /createUser
- /deleteUser

## 6) Idempotency and method semantics
- GET should not modify state.
- PUT should replace resource representation.
- PATCH should partially update.
- DELETE should remove target.

Idempotent methods (same call repeated gives same effect):
- GET, PUT, DELETE (normally)
- POST is not idempotent by default.

## 7) Query parameters for reads
Use query params for:
- filtering: /users?role=admin
- sorting: /users?sort=created_at
- pagination: /users?skip=0&limit=20

## 8) Hands-on API design exercise
Design endpoints for a task manager:
- tasks CRUD
- comments on tasks
- user assignment
- filter by status and priority

Write:
1. endpoint path
2. method
3. expected status code
4. sample response shape

## 9) Postman workflow for learning
For every endpoint test:
1. send valid request
2. send invalid request
3. test edge case (missing required field)
4. verify status code and body shape

## 10) Interview questions
1. Difference between 401 and 403?
2. When would you use 409?
3. Explain idempotency with examples.
4. Why should GET be side-effect free?

## Day 2 completion checklist
- I can explain full HTTP request and response structure.
- I can choose correct method and status code.
- I can design clean REST paths.
- I can test APIs systematically with Postman.

Previous: Day 1 | Next: Day 3
