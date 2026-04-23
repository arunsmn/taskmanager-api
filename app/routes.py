from fastapi import APIRouter, HTTPException
from app.models import Task, TaskCreate

router = APIRouter()

# In-memory database (a simple dict for learning)
db: dict[int, Task] = {}
counter = {"id": 1}


@router.get("/tasks", response_model=list[Task])
def get_tasks():
    return list(db.values())


@router.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    task_id = counter["id"]
    new_task = Task(id=task_id, **task.model_dump())
    db[task_id] = new_task
    counter["id"] += 1
    return new_task


@router.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    if task_id not in db:
        raise HTTPException(status_code=404, detail="Task not found")
    return db[task_id]


@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated: TaskCreate):
    if task_id not in db:
        raise HTTPException(status_code=404, detail="Task not found")
    db[task_id] = Task(id=task_id, **updated.model_dump())
    return db[task_id]


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in db:
        raise HTTPException(status_code=404, detail="Task not found")
    del db[task_id]
    return {"message": "Task deleted"}
