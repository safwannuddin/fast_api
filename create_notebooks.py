import json
import os

# Day 1 Notebook
day1_notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Day 1 - Backend Foundations for Absolute Beginners\n",
                "\n",
                "**Goal:** Understand what backend development is, how the web works end-to-end, and how FastAPI fits into real software systems."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1) What is backend development?\n",
                "\n",
                "Backend is the part of software that handles data, business logic, security, and communication with databases or external services.\n",
                "\n",
                "**If frontend is what users see, backend is the system that decides:**\n",
                "- what data is valid\n",
                "- who is allowed to do what\n",
                "- where data is stored\n",
                "- what response should be sent back"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2) How a web request actually works\n",
                "\n",
                "When a user clicks \"Login\" in an app:\n",
                "1. Browser/mobile app sends an HTTP request\n",
                "2. Backend receives request at an endpoint\n",
                "3. Backend validates input\n",
                "4. Backend checks DB or external services\n",
                "5. Backend creates response (success/error)\n",
                "6. Frontend renders response\n",
                "\n",
                "**This request-response loop is the core of backend engineering.**"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3) Key backend terms\n",
                "\n",
                "| Term | Meaning |\n",
                "|------|----------|\n",
                "| **Client** | App that sends request |\n",
                "| **Server** | App that receives & responds |\n",
                "| **API** | Rules for client-server talk |\n",
                "| **Endpoint** | Route like /users or /orders/5 |\n",
                "| **Database** | Persistent data storage |\n",
                "| **JSON** | Data format for APIs |\n",
                "| **Stateless** | Server doesn't remember unless stored |"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4) FastAPI in backend ecosystem\n",
                "\n",
                "FastAPI is a Python framework to build APIs with type hints.\n",
                "\n",
                "**Why teams use it:**\n",
                "- ⚡ Fast performance\n",
                "- ✅ Automatic validation\n",
                "- 📖 Auto-generated docs\n",
                "- 😊 Clean developer experience"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5) Python concepts you need\n",
                "\n",
                "Be comfortable with:\n",
                "- functions\n",
                "- dictionaries and lists\n",
                "- classes\n",
                "- type hints\n",
                "- imports and virtual environments"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Example: Function with type hints\n",
                "def add(a: int, b: int) -> int:\n",
                "    \"\"\"Add two integers.\"\"\"\n",
                "    return a + b\n",
                "\n",
                "result = add(5, 3)\n",
                "print(f\"5 + 3 = {result}\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "Type hints are **powerful in FastAPI** because they drive validation and docs."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 6) Setting up development environment\n",
                "\n",
                "1. Install Python 3.10+\n",
                "2. Create project folder\n",
                "3. Create virtual environment\n",
                "4. Install dependencies\n",
                "\n",
                "**Windows PowerShell:**"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Run in PowerShell terminal (not here)\n",
                "# python -m venv venv\n",
                "# venv\\\\Scripts\\\\activate\n",
                "# pip install fastapi uvicorn[standard]\n",
                "\n",
                "print(\"Copy above commands to your PowerShell\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 7) Common beginner mistakes\n",
                "\n",
                "❌ Coding without virtual environment\n",
                "❌ Mixing unrelated code in one file\n",
                "❌ Ignoring HTTP status codes\n",
                "❌ Copying code without understanding"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 8) Practice exercises\n",
                "\n",
                "1. Write 3 Python functions with type hints\n",
                "2. Create one dict and one list of dicts\n",
                "3. Explain: What happens when you open a URL?\n",
                "4. Install dependencies in a venv"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Exercise 1: Functions with type hints\n",
                "def multiply(x: int, y: int) -> int:\n",
                "    return x * y\n",
                "\n",
                "def greet(name: str) -> str:\n",
                "    return f\"Hello, {name}!\"\n",
                "\n",
                "def is_adult(age: int) -> bool:\n",
                "    return age >= 18\n",
                "\n",
                "print(multiply(4, 5))\n",
                "print(greet(\"Safwan\"))\n",
                "print(f\"Is 25 an adult? {is_adult(25)}\")"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Exercise 2: Dictionary and list\n",
                "user = {\n",
                "    \"id\": 1,\n",
                "    \"name\": \"Safwan\",\n",
                "    \"email\": \"safwan@example.com\",\n",
                "    \"age\": 25\n",
                "}\n",
                "\n",
                "users = [\n",
                "    {\"id\": 1, \"name\": \"Alice\", \"role\": \"admin\"},\n",
                "    {\"id\": 2, \"name\": \"Bob\", \"role\": \"user\"},\n",
                "    {\"id\": 3, \"name\": \"Charlie\", \"role\": \"user\"},\n",
                "]\n",
                "\n",
                "print(\"Single user:\", user)\n",
                "print(\"\\nAll users:\")\n",
                "for u in users:\n",
                "    print(f\"  - {u['name']} ({u['role']})\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 9) Interview starter questions\n",
                "\n",
                "1. Difference between frontend and backend?\n",
                "2. What is an API endpoint?\n",
                "3. What does stateless mean?\n",
                "4. Why use virtual environments?"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## ✅ Day 1 Checklist\n",
                "\n",
                "- [ ] I can explain client-server architecture\n",
                "- [ ] I understand request-response cycle\n",
                "- [ ] I can set up projects correctly\n",
                "- [ ] I know FastAPI's role in backend\n",
                "\n",
                "---\n",
                "\n",
                "**Next:** Day 2"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.11.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# Day 2 Notebook
day2_notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Day 2 - HTTP and REST Deep Dive\n",
                "\n",
                "**Goal:** Understand exactly how APIs communicate using HTTP and design clean REST endpoints."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1) HTTP basics\n",
                "\n",
                "HTTP is the protocol between client and server.\n",
                "\n",
                "Every exchange has:\n",
                "- **Request:** method + URL + headers + optional body\n",
                "- **Response:** status code + headers + optional body"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2) Request anatomy\n",
                "\n",
                "Example:\n",
                "```http\n",
                "POST /users HTTP/1.1\n",
                "Host: api.example.com\n",
                "Content-Type: application/json\n",
                "Authorization: Bearer <token>\n",
                "\n",
                "{\n",
                "  \"name\": \"Safwan\",\n",
                "  \"email\": \"safwan@example.com\"\n",
                "}\n",
                "```\n",
                "\n",
                "**Key parts:**\n",
                "- Method: action (GET, POST, PUT, PATCH, DELETE)\n",
                "- Path: resource target\n",
                "- Headers: metadata\n",
                "- Body: payload for create/update"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3) Response anatomy\n",
                "\n",
                "Example:\n",
                "```http\n",
                "HTTP/1.1 201 Created\n",
                "Content-Type: application/json\n",
                "\n",
                "{\n",
                "  \"id\": 1,\n",
                "  \"name\": \"Safwan\"\n",
                "}\n",
                "```"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4) Status codes you must master\n",
                "\n",
                "| Code | Meaning |\n",
                "|------|----------|\n",
                "| **200** | OK - request succeeded |\n",
                "| **201** | Created - new resource made |\n",
                "| **204** | No Content - success, no body |\n",
                "| **400** | Bad Request - malformed |\n",
                "| **401** | Unauthorized - missing auth |\n",
                "| **403** | Forbidden - not allowed |\n",
                "| **404** | Not Found - resource missing |\n",
                "| **409** | Conflict - duplicate/state error |\n",
                "| **422** | Unprocessable - validation failed |\n",
                "| **500** | Internal Error - server bug |"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 5) REST design fundamentals\n",
                "\n",
                "**Use nouns for resources:**\n",
                "```\n",
                "GET    /users        # list users\n",
                "GET    /users/1      # get user 1\n",
                "POST   /users        # create user\n",
                "PATCH  /users/1      # update user 1\n",
                "DELETE /users/1      # delete user 1\n",
                "```\n",
                "\n",
                "**Avoid action-style URLs:**\n",
                "```\n",
                "❌ /createUser\n",
                "❌ /deleteUser\n",
                "```"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 6) Idempotency and method semantics\n",
                "\n",
                "| Method | Modifies state? | Idempotent? | Use |\n",
                "|--------|-----------------|------------|------|\n",
                "| GET | No | Yes | Read |\n",
                "| PUT | Yes | Yes | Replace |\n",
                "| PATCH | Yes | No | Partial update |\n",
                "| DELETE | Yes | Yes (usually) | Delete |\n",
                "| POST | Yes | No | Create |\n",
                "\n",
                "**Idempotent:** Same call repeated = same effect"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 7) Query parameters for reads\n",
                "\n",
                "Use query params for:\n",
                "- **Filtering:** `/users?role=admin`\n",
                "- **Sorting:** `/users?sort=created_at`\n",
                "- **Pagination:** `/users?skip=0&limit=20`"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Example: URLs with query parameters\n",
                "\n",
                "urls = [\n",
                "    \"GET /users\",\n",
                "    \"GET /users?skip=0&limit=10\",\n",
                "    \"GET /users?role=admin&sort=name\",\n",
                "    \"POST /users\",\n",
                "    \"PATCH /users/5\",\n",
                "    \"DELETE /users/5\",\n",
                "]\n",
                "\n",
                "for url in urls:\n",
                "    print(url)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 8) Hands-on: Design APIs for a task manager\n",
                "\n",
                "Tasks CRUD:\n",
                "- GET /tasks\n",
                "- GET /tasks/{task_id}\n",
                "- POST /tasks\n",
                "- PATCH /tasks/{task_id}\n",
                "- DELETE /tasks/{task_id}\n",
                "\n",
                "Comments on tasks:\n",
                "- GET /tasks/{task_id}/comments\n",
                "- POST /tasks/{task_id}/comments\n",
                "- DELETE /comments/{comment_id}"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 9) Testing with Postman\n",
                "\n",
                "For each endpoint:\n",
                "1. Send valid request\n",
                "2. Send invalid request\n",
                "3. Test edge case (missing field)\n",
                "4. Verify status code\n",
                "5. Verify response shape"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 10) Interview questions\n",
                "\n",
                "1. Difference between 401 and 403?\n",
                "2. When would you use 409 status?\n",
                "3. Explain idempotency with examples\n",
                "4. Why should GET be side-effect free?"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## ✅ Day 2 Checklist\n",
                "\n",
                "- [ ] I can explain HTTP request/response structure\n",
                "- [ ] I can choose correct methods & status codes\n",
                "- [ ] I can design clean REST paths\n",
                "- [ ] I can test APIs with Postman\n",
                "\n",
                "---\n",
                "\n",
                "**Previous:** Day 1 | **Next:** Day 3"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.11.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# Write notebooks
with open(r'c:\Users\safwa\Downloads\fast_api\docs\day01.ipynb', 'w') as f:
    json.dump(day1_notebook, f, indent=2)
print("✅ Day 1 notebook created")

with open(r'c:\Users\safwa\Downloads\fast_api\docs\day02.ipynb', 'w') as f:
    json.dump(day2_notebook, f, indent=2)
print("✅ Day 2 notebook created")

print("\n🎉 All notebooks ready! Open them in Jupyter or VS Code.")
