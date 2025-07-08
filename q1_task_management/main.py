from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
from datetime import datetime
from models import Task, TaskCreate, TaskUpdate

# Initialize FastAPI app
app = FastAPI(
    title="Task Management API",
    description="A simple FastAPI application with in-memory storage for task management",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# In-memory storage for tasks (simple list)
tasks: List[dict] = []


def get_next_task_id() -> int:
    """Generate the next task ID using list length + 1"""
    # Note: This is simplified for demo purposes. In production, use UUID or database auto-increment
    return len(tasks) + 1


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main web UI"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    """Get all tasks"""
    return [Task(**task) for task in tasks]


@app.post("/tasks", response_model=Task, status_code=201)
async def create_task(task: TaskCreate):
    """Create a new task"""
    task_id = get_next_task_id()
    now = datetime.now()
    
    task_dict = {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": now,
        "updated_at": now
    }
    
    tasks.append(task_dict)
    return Task(**task_dict)


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskUpdate):
    """Update an existing task"""
    # Find task by ID
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update only provided fields
    if task_update.title is not None:
        task["title"] = task_update.title
    if task_update.description is not None:
        task["description"] = task_update.description
    if task_update.completed is not None:
        task["completed"] = task_update.completed
    
    task["updated_at"] = datetime.now()
    
    return Task(**task)


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    """Delete a task"""
    # Find task by ID
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    tasks.remove(task)


# Web UI endpoints for form handling
@app.post("/tasks/create")
async def create_task_form(
    title: str = Form(...),
    description: str = Form("")
):
    """Handle task creation from web form"""
    task_data = TaskCreate(title=title, description=description if description else None)
    await create_task(task_data)
    return RedirectResponse(url="/", status_code=303)


@app.post("/tasks/{task_id}/toggle")
async def toggle_task(task_id: int):
    """Toggle task completion status"""
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task["completed"] = not task["completed"]
    task["updated_at"] = datetime.now()
    
    return RedirectResponse(url="/", status_code=303)


@app.post("/tasks/{task_id}/delete")
async def delete_task_form(task_id: int):
    """Handle task deletion from web form"""
    await delete_task(task_id)
    return RedirectResponse(url="/", status_code=303)


# Add some sample data for demonstration
@app.on_event("startup")
async def startup_event():
    """Initialize with sample data"""
    sample_tasks = [
        {"title": "Learn FastAPI", "description": "Study FastAPI framework and build a simple API", "completed": True},
        {"title": "Create Task Manager", "description": "Build a task management application", "completed": False},
        {"title": "Write Documentation", "description": "Document the project and create README", "completed": False}
    ]
    
    for i, sample_task in enumerate(sample_tasks, 1):
        now = datetime.now()
        task_dict = {
            "id": i,
            "title": sample_task["title"],
            "description": sample_task["description"],
            "completed": sample_task["completed"],
            "created_at": now,
            "updated_at": now
        }
        tasks.append(task_dict)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 