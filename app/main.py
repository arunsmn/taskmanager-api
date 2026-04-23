from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Task Manager API",
    description="A simple task manager API built with FastAPI",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Task Manager API is running 🚀"}
