from sqlalchemy import Column, String, DateTime, text, Integer
from app.core.database import Base

class UsersModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=text("now()"))