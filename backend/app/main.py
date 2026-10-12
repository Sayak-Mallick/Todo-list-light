from fastapi import FastAPI
from app.db.database import Base, engine
from app.routers import auth, todos

Base.metadata.create_all(bind=engine)
"""Create all tables stored in this metadata. 
   Conditional by default, will not attempt to recreate tables already present in the target database.
"""
app = FastAPI(title="Todo API")
app.include_router(auth.router)
app.include_router(todos.router)


@app.get("/", tags=["health"])
def root():
    return {"status": "ok"}
