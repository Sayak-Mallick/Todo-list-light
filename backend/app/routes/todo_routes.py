from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.todos_model import TodosModel
from app.schemas.todos_schema import TodoResponse, TodoCreate, TodoUpdateStatus, TodoUpdate

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("/", response_model=list[TodoResponse])
def get_all_todos(db: Session = Depends(get_db)):
    todos = db.query(TodosModel).all()
    return todos

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    new_todo = TodosModel(**todo.dict())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@router.get("/latest", response_model=TodoResponse)
def get_latest_todo(db: Session = Depends(get_db)):
    latest = db.query(TodosModel).order_by(TodosModel.created_at.desc()).first()
    return latest

@router.get("/{id}", response_model=list[TodoResponse])
def get_single_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(TodosModel).filter(TodosModel.id == id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {id} not found")
    return todo

@router.delete("/{id}")
def delete_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(TodosModel).filter(TodosModel.id == id).delete(synchronize_session=False)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {id} not found")
    db.commit()
    return {"message": "Todo deleted successfully!"}

@router.put("/{id}", response_model=TodoResponse)
def update_todo(id: int, todo_data: TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(TodosModel).filter(TodosModel.id == id).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {id} not found")
    todo.title = todo_data.title
    todo.description = todo_data.description
    todo.is_completed = todo_data.is_completed
    db.commit()
    db.refresh(todo)
    return todo


@router.patch("/{id}", response_model=TodoResponse)
def update_status(id: int, todo_data: TodoUpdateStatus, db: Session = Depends(get_db)):
    todo = db.query(TodosModel).filter(TodosModel.id == id).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {id} not found")
    todo.is_completed = todo_data.is_completed
    db.commit()
    db.refresh(todo)
    return todo