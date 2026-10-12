from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.db.database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
