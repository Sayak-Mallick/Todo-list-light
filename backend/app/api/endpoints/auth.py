from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.db.database import get_db
from app.deps import get_current_user
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserOut

router = APIRouter()


@router.post("/signup", response_model=UserOut, status_code=201)
def signup(data: UserCreate, db: Session = Depends(get_db)):
    # Prevent duplicate usernames.
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    # Hash the password before saving the user.
    user = User(
        username=data.username,
        password=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)  # Load the saved user's database values.
    return user


@router.post("/login", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # Find the user by username.
    user = db.query(User).filter(User.username == form.username).first()

    # Reject invalid credentials.
    if not user or not verify_password(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # Return a signed JWT access token.
    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    """Return the currently authenticated user."""
    return user