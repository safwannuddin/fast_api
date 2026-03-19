

from fastapi import FastAPI
from pydantic import BaseModel

from fastapi import Body




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
class Todo(BaseModel):
    title: str
    completed: bool

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/root")
def root():
    return {"Hello": "SAfwan uddin 123 "}

@app.post("/todos")
def create_todo(todo: Todo):
    return todo

@app.post("/createpost")
def create_post(payload: dict =Body(...)):
    print(payload)
    return {"message": "Post created successfully"}