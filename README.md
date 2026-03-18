# 🚀 Master Backend Development & FastAPI in 10 Days

A complete, beginner-friendly learning guide that takes you from zero to building and deploying production-ready REST APIs with Python and FastAPI.

---

## 🎯 Who Is This For?

This guide is designed for **absolute beginners** who want to:
- Understand how the web and backend systems work
- Build APIs using Python and FastAPI
- Connect APIs to a database
- Secure APIs with authentication
- Test and deploy their applications

No prior backend experience is required — only basic Python knowledge is helpful.

---

## 📅 10-Day Curriculum

| Day | Topic | What You'll Learn |
|-----|-------|-------------------|
| [Day 1](docs/day01.md) | Intro to Backend & Python Recap | How the internet works, what a backend is, Python essentials |
| [Day 2](docs/day02.md) | HTTP, REST & APIs | HTTP methods, status codes, REST principles, Postman |
| [Day 3](docs/day03.md) | FastAPI Setup & First API | Install FastAPI, create your first endpoint, interactive docs |
| [Day 4](docs/day04.md) | Path Params, Query Params & Request Body | Receiving data from clients, type hints |
| [Day 5](docs/day05.md) | Data Validation with Pydantic | Models, validators, response schemas |
| [Day 6](docs/day06.md) | Database Integration (SQLAlchemy) | SQLite, ORM basics, sessions, models |
| [Day 7](docs/day07.md) | Full CRUD Application | Create, Read, Update, Delete with a real database |
| [Day 8](docs/day08.md) | Authentication & Security (JWT) | Password hashing, JWT tokens, protected routes |
| [Day 9](docs/day09.md) | Testing FastAPI Apps | pytest, TestClient, writing unit & integration tests |
| [Day 10](docs/day10.md) | Deployment & Production Best Practices | Docker, environment variables, Render/Railway/VPS deploy |

---

## 🛠️ Prerequisites

- Python 3.10+ installed ([download here](https://www.python.org/downloads/))
- A code editor — [VS Code](https://code.visualstudio.com/) is recommended
- Terminal / Command Prompt basics
- [Postman](https://www.postman.com/) or [Thunder Client](https://www.thunderclient.com/) (VS Code extension) for testing APIs

---

## ⚡ Quick Start

```bash
# Clone this repository
git clone https://github.com/safwannuddin/fast_api.git
cd fast_api

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# Install dependencies
pip install fastapi uvicorn[standard] sqlalchemy pydantic python-jose[cryptography] passlib[bcrypt] python-multipart pytest httpx
```

Then open [Day 1](docs/day01.md) and start learning! 🎉

---

## 📂 Repository Structure

```
fast_api/
├── README.md               ← You are here (course overview)
├── docs/
│   ├── day01.md            ← Day 1 learning content
│   ├── day02.md
│   ├── ...
│   └── day10.md
└── examples/               ← Working code examples (created during the course)
```

---

## 💡 Tips for Success

1. **Code along** — don't just read, type every example yourself.
2. **Experiment** — break things and fix them; that's how you learn.
3. **Take notes** — write down concepts in your own words.
4. **Build something** — by Day 10, build a small project of your own.
5. **Ask for help** — open an issue in this repo if you're stuck.

---

Happy coding! 🐍✨