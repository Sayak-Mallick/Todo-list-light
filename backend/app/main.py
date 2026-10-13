from fastapi import FastAPI
from app.api.router import api_router
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine) # Create database tables if they do not already exist
app = FastAPI(title="Todo API")
app.include_router(api_router)

@app.get("/", tags=["health"])
def root():
    return {"status": "ok"}
