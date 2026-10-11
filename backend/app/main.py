from fastapi import FastAPI

from app.core.database import engine, Base
from app.routes.todo_routes import router as todo_router

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(todo_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}