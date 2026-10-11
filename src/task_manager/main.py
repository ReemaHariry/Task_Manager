from dataclasses import asdict
from fastapi import FastAPI, HTTPException , status
from .models import Task
from .schemas import TaskCreate ,TaskResponse,TaskUpdate

app=FastAPI()

db:dict[int,Task]={}
task_id=0

def id_incremention()->int:
    new_id = len(db) + 1
    while new_id in db:
        new_id += 1
    return new_id

@app.post("/tasks")
def create_task(task: TaskCreate) -> TaskResponse:
    task_id = id_incremention()

    task_create = Task(
        task_id=task_id,
        **task.model_dump()
    )

    db[task_id] = task_create

    response = asdict(task_create)
    return TaskResponse(**response)

    