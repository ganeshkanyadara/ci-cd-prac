from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
#changes
app = FastAPI(title="Task Manager")

tasks = []
next_id = 1


class TaskInput(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    completed: bool


@app.get("/api/tasks")
def get_tasks():
    return tasks


@app.post("/api/tasks", status_code=201)
def add_task(data: TaskInput):
    global next_id

    title = data.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Task title is required")

    task = {
        "id": next_id,
        "title": title,
        "completed": False
    }
    next_id += 1
    tasks.append(task)
    return task


@app.patch("/api/tasks/{task_id}")
def update_task(task_id: int, data: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = data.completed
            return task

    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return

    raise HTTPException(status_code=404, detail="Task not found")


# Serve the frontend after defining the API routes.
app.mount("/", StaticFiles(directory="static", html=True), name="static")
