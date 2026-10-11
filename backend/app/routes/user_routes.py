from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.users_model import UsersModel
from app.schemas.users_schema import UserResponse, UserCreate, UserUpdate

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    """This route returns all users"""
    users = db.query(UsersModel).all()
    return users

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate ,db: Session = Depends(get_db)):
    """This route creates a new user"""
    existed_user = db.query(UsersModel).filter(UsersModel.email == user.email).first()
    if existed_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email {user.email} already exists")
    new_user = UsersModel(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=UserResponse)
def get_single_user(id: int, db: Session = Depends(get_db)):
    """This route returns a particular user"""
    user = db.query(UsersModel).filter(UsersModel.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user

@router.put("/{id}", response_model=UserResponse)
def update_user(user_data: UserUpdate, id: str, db: Session = Depends(get_db)):
    """This route updates an existing user"""
    user = db.query(UsersModel).filter(UsersModel.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")

    for key, value in user_data.dict().items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    """This route deletes an existing user"""
    user = db.query(UsersModel).filter(UsersModel.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}