from fastapi import FastAPI

from app.core.database import engine, Base
from app.routes.todo_routes import router as todo_router
from app.routes.user_routes import router as user_router
from app.routes.auth_routes import router as auth_router

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(todo_router)
app.include_router(user_router)
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}