from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.deps import get_current_user
from app.models.todo import Todo
from app.models.user import User
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate, TodoStatusUpdate

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(data: TodoCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    todo = Todo(title=data.title, description=data.description, user_id=user.id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.get("/", response_model=List[TodoResponse])
def list_todos(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    todos = db.query(Todo).filter(Todo.user_id == user.id).all()
    return todos


@router.get("/{id}", response_model=TodoResponse)
def get_todo(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == id, Todo.user_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo


@router.put("/{id}", response_model=TodoResponse)
def update_todo(id: int, data: TodoUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    for key, value in data.dict().items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return todo

@router.patch("/{id}", response_model=TodoResponse)
def update_status(id:int, data: TodoStatusUpdate, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    todo.completed = data.completed
    db.commit()
    db.refresh(todo)
    return todo

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == id, Todo.user_id == user.id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message":"Todo deleted successfully"}