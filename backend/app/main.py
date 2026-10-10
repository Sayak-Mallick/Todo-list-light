from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db, engine, Base
from app.schemas.todos_schema import TodoCreate, TodoResponse
from app.models.todos_model import TodosModel
from app.models.users_model import UsersModel

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/todos", response_model=list[TodoResponse])
def get_all_todos(db: Session = Depends(get_db)):
    todos = db.query(TodosModel).all()
    return todos

@app.post("/todos", status_code=status.HTTP_201_CREATED, response_model=TodoResponse)
def create_todo(new_todo: TodoCreate):
    print(new_todo.dict())
    return {"message": "Todo created successfully!", "data": new_todo.dict()}

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo_by_id(todo_id: int):
    if todo_id < 1 or todo_id > len(todos):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return {"data": todos[todo_id - 1]}

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    if todo_id < 1 or todo_id > len(todos):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    todos.pop(todo_id - 1)
    return {"message": "Todo deleted successfully!"}

@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, new_todo: TodoCreate):
    if todo_id < 1 or todo_id > len(todos):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    todos[todo_id - 1] = new_todo.dict()
    return {"message": "Todo updated successfully!", "data": new_todo.dict()}