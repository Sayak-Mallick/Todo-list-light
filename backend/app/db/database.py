from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

engine = create_engine(         # Connect to the database.
    settings.database_url,
    pool_size= settings.database_pool_size,
    max_overflow = settings.database_max_overflow
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Create database sessions.
Base = declarative_base() # Base class for all database models.


def get_db():
    db = SessionLocal()  # Create a new database session.
    try:
        yield db # Provide the session to the API endpoint.
    finally:
        db.close() # Close the session after use.
