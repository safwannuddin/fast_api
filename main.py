from fastapi import FastAPI
from pydantic import BaseModel
from random import randrange

app = FastAPI(
    title="My First API",
    description="Learning FastAPI step by step",
    version="1.0.0"
)

# ------------------ Pydantic Models ------------------

class Post(BaseModel):
    title: str
    content: str

class Todo(BaseModel):
    title: str
    completed: bool


my_posts = [
    {
        "title": "My First Post",
        "content": "This is the content of my first post.",
        "id": 1
    },
    {
        "title": "My Second Post",
        "content": "I like cricket.",
        "id": 2
    }
]


items = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Mouse",  "price": 29.99},
    {"id": 3, "name": "Keyboard", "price": 79.99},
]


# ------------------ Routes ------------------

@app.get("/")
def root():
    return {"message": "Welcome to My First API!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/createpost")
def create_post(new_post: Post):
    post_dict = new_post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append()
    print(new_post)
    return {"data": "New post created successfully"}


@app.get("/items")
def get_all_items():
    return items


@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}


@app.post("/todos")
def create_todo(todo: Todo):
    return todo