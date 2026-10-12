from pydantic import BaseModel, ConfigDict


# Validates signup request data.
class UserCreate(BaseModel):
    username: str
    password: str


# Defines the user data returned by the API.
class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Read data from SQLAlchemy models.

    id: int
    username: str


# Defines the JWT authentication response.
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"