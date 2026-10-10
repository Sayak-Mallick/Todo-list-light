from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, text, Integer

from app.core.database import Base

class TodosModel(Base):
  __tablename__ = "todos"
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, nullable=False)
  description = Column(String, nullable=True)
  is_completed = Column(Boolean, nullable=False, default=False)
  created_at = Column(DateTime, nullable=False, server_default=text("now()"))
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)