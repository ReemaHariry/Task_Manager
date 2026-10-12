from dataclasses import asdict
from fastapi import FastAPI, HTTPException , status
from .models import Task
from .schemas import TaskCreate ,TaskResponse,TaskUpdate

app=FastAPI()

db:dict[int,Task]={}
task_id=0

def id_incremention()->int:
    global task_id
    task_id = len(db) + 1
    while task_id in db:
        task_id += 1
    return task_id

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

@app.get("/tasks")
def task_response()->list[TaskResponse]:
    db_list=[]
    
    for task in db.values():
        db_dict=asdict(task)
        response=TaskResponse(**db_dict)
        db_list.append(response)
    return db_list

@app.delete("/tasks/{task_id}")
def delete_task(task_id:int):
    if task_id not in db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"This task id {task_id} is not found ")
    db.pop(task_id)
    return {"tasks":db,"status":"the task has been deleted successfully"}

@app.patch("/tasks/{task_id}")
def update_task(task_id:int,task:TaskUpdate)->TaskResponse:
    if task_id not in db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"this task with id {task_id} is not found")
    
    old_task=asdict(db[task_id])
    updates=task.model_dump(exclude_unset=True)
    old_task.update(updates)
    final_task=Task(**old_task)
    
    db[task_id] = final_task
    return TaskResponse(**asdict(final_task))
    
    