# Day 2 — How the Web Works: HTTP, REST & APIs

> **Goal:** Understand the protocol that powers the internet, learn REST principles, and practice sending requests with Postman.

---

## 🌍 How the Web Works

Every time your browser loads a page or your app fetches data, it follows this cycle:

```
1. Client sends an HTTP Request  →  Server
2. Server processes the request
3. Server sends an HTTP Response  →  Client
```

This is called the **request-response cycle**, and it uses the **HTTP protocol**.

---

## 📡 HTTP — HyperText Transfer Protocol

HTTP is the language clients and servers use to communicate. Every HTTP message has:

### HTTP Request

```
GET /users/1 HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGci...
Content-Type: application/json

{ "name": "Alice" }
```

| Part | Description |
|------|-------------|
| **Method** | The action you want to perform (`GET`, `POST`, etc.) |
| **Path** | The resource you're targeting (`/users/1`) |
| **Headers** | Metadata about the request (auth tokens, content type) |
| **Body** | Data you're sending (only for POST, PUT, PATCH) |

### HTTP Response

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com"
}
```

| Part | Description |
|------|-------------|
| **Status Code** | A 3-digit number indicating success or failure |
| **Headers** | Metadata about the response |
| **Body** | The data the server sends back (usually JSON) |

---

## 🔢 HTTP Status Codes

You'll encounter these every day as a backend developer:

| Code | Name | Meaning |
|------|------|---------|
| **200** | OK | Request succeeded |
| **201** | Created | Resource was successfully created |
| **204** | No Content | Success, but no data to return |
| **400** | Bad Request | Client sent invalid data |
| **401** | Unauthorized | Authentication required |
| **403** | Forbidden | Authenticated but not allowed |
| **404** | Not Found | Resource doesn't exist |
| **422** | Unprocessable Entity | Validation failed (FastAPI uses this a lot) |
| **500** | Internal Server Error | Something broke on the server |

> **Rule of thumb:** 2xx = success, 4xx = client error, 5xx = server error

---

## 🔧 HTTP Methods (Verbs)

| Method | Purpose | Has Body? |
|--------|---------|-----------|
| **GET** | Retrieve data | No |
| **POST** | Create a new resource | Yes |
| **PUT** | Replace a resource entirely | Yes |
| **PATCH** | Update part of a resource | Yes |
| **DELETE** | Delete a resource | Usually No |

---

## 🏗️ REST — Representational State Transfer

REST is a set of conventions for designing APIs that are **predictable** and **easy to use**.

### REST Principles

1. **Stateless** — Each request contains all the info the server needs. The server doesn't remember previous requests.
2. **Resource-based** — URLs represent *things* (nouns), not *actions* (verbs).
3. **Use HTTP methods correctly** — GET to read, POST to create, etc.
4. **Consistent responses** — Use JSON and standard status codes.

### ✅ Good REST API Design

```
GET    /users           → Get all users
GET    /users/1         → Get user with ID 1
POST   /users           → Create a new user
PUT    /users/1         → Replace user 1 entirely
PATCH  /users/1         → Update part of user 1
DELETE /users/1         → Delete user 1
```

### ❌ Bad REST API Design

```
GET  /getUsers         ← Don't use verbs in URLs
POST /createUser       ← Same issue
GET  /deleteUser/1     ← Never use GET to delete!
```

---

## 📦 JSON — JavaScript Object Notation

JSON is the standard data format for REST APIs. It's human-readable and maps perfectly to Python dictionaries.

```json
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com",
  "age": 30,
  "is_active": true,
  "tags": ["admin", "user"],
  "address": {
    "city": "New York",
    "country": "USA"
  }
}
```

JSON supports these types:
- `string` → `"text"`
- `number` → `42`, `3.14`
- `boolean` → `true`, `false`
- `null` → `null`
- `array` → `[1, 2, 3]`
- `object` → `{ "key": "value" }`

---

## 🛠️ Using Postman to Test APIs

Postman is a GUI tool for sending HTTP requests. It's essential for testing your APIs.

### Installing Postman

1. Download from [postman.com](https://www.postman.com/downloads/)
2. Create a free account (or skip)
3. Click **"New"** → **"HTTP Request"**

### Making Your First Request

Let's test a public API — [JSONPlaceholder](https://jsonplaceholder.typicode.com/):

1. Set method to **GET**
2. Enter URL: `https://jsonplaceholder.typicode.com/users/1`
3. Click **Send**
4. You'll see a JSON response with user data

### Try These Requests

```
GET  https://jsonplaceholder.typicode.com/posts        → all posts
GET  https://jsonplaceholder.typicode.com/posts/1      → post #1
GET  https://jsonplaceholder.typicode.com/users        → all users
POST https://jsonplaceholder.typicode.com/posts        → create post
     Body (JSON): {"title": "My Post", "body": "Hello", "userId": 1}
```

---

## 🔍 Headers Deep Dive

Headers are key-value pairs that provide context for requests and responses.

### Common Request Headers

```
Content-Type: application/json    ← Tell server you're sending JSON
Authorization: Bearer <token>     ← Send your auth token
Accept: application/json          ← Tell server you want JSON back
```

### Setting Headers in Postman

1. Click the **Headers** tab in Postman
2. Add `Content-Type: application/json` for POST requests

---

## 🆚 REST vs Other API Types

| Style | Description | When to Use |
|-------|-------------|-------------|
| **REST** | Resource-based URLs, HTTP methods | Most web APIs — simple and universal |
| **GraphQL** | Single endpoint, flexible queries | Complex data requirements |
| **gRPC** | Binary protocol, very fast | Microservices communicating internally |
| **WebSockets** | Persistent two-way connection | Real-time apps (chat, live updates) |

> For this course, we focus on REST — it's the most widely used and what FastAPI excels at.

---

## 📝 Day 2 Exercises

1. Open Postman and fetch all posts from `https://jsonplaceholder.typicode.com/posts`. How many are there?
2. Send a `POST` request to `https://jsonplaceholder.typicode.com/posts` with a JSON body `{"title": "Test", "body": "Learning APIs", "userId": 1}`. What status code do you get?
3. What status code would you expect if you request a user that doesn't exist? Try `GET /users/99999` on JSONPlaceholder.
4. Design the REST endpoints for a **Blog API** with posts and comments. What URLs and methods would you use?
5. What's the difference between PUT and PATCH?

---

## ✅ Day 2 Checklist

- [ ] I understand how HTTP requests and responses work
- [ ] I know the most common HTTP status codes (200, 201, 400, 401, 404, 500)
- [ ] I know when to use GET, POST, PUT, PATCH, DELETE
- [ ] I understand REST principles and can design clean API routes
- [ ] I've sent requests using Postman and read JSON responses

---

⬅️ **Previous:** [Day 1](day01.md) | ➡️ **Next:** [Day 3 — FastAPI Setup & First API](day03.md)
