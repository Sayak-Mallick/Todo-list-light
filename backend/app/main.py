from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db, engine, Base
from app.schemas.todos_schema import TodoCreate, TodoResponse, TodoUpdate
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
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    new_todo = TodosModel(**todo.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@app.get("/todos/id", response_model=list[TodoResponse])
def get_todo_by_id(id: int, db: Session = Depends(get_db)):
    todo = db.query(TodosModel).filter(TodosModel.id == id).filter()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The todo item with the id: {id} was not found.")
    return todo

@app.delete("/todos/id", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(TodosModel).filter(TodosModel.id == id).delete(synchronize_session=False)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The todo item with the id: {id} was not found.")
    db.commit()
    return {"message": "Todo deleted successfully!"}

@app.put("/todos/id", response_model=TodoResponse)
def update_todo(id: int, todo_data: TodoUpdate,db: Session = Depends(get_db)):
    todo = db.query(TodosModel).filter(TodosModel.id == id).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cannot find the todo with the id: {id}")
    todo.title = todo_data.title
    todo.description = todo_data.description
    todo.is_completed = todo_data.is_completed
    db.commit()
    db.refresh(todo)
    return todo