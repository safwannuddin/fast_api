

from fastapi import FastAPI
from pydantic import BaseModel

from fastapi import Body

app = FastAPI()

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