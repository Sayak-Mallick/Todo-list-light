from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

url = settings.DATABASE_URL

engine = create_engine(url) # Connect to the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Create database sessions.
Base = declarative_base() # Base class for all database models.


def get_db():
    db = SessionLocal()  # Create a new database session.
    try:
        yield db # Provide the session to the API endpoint.
    finally:
        db.close() # Close the session after use.
