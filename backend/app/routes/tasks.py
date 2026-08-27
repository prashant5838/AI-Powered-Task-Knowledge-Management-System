from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.auth import get_db, get_current_user, require_role
from app import crud
from app.schemas import TaskCreate, TaskOut

router = APIRouter()


@router.post("/", response_model=TaskOut)
def create_task(payload: TaskCreate, db: Session = Depends(get_db), current_user=Depends(require_role("admin"))):
    task = crud.create_task(db, title=payload.title, description=payload.description, assigned_to=payload.assigned_to)
    crud.log_activity(db, current_user.id, "create_task", str(task.id))
    return task


@router.get("/", response_model=list[TaskOut])
def list_tasks(status: Optional[str] = None, assigned_to: Optional[int] = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    q = db.query(crud.models.Task)
    if status:
        q = q.filter(crud.models.Task.status == status)
    if assigned_to:
        q = q.filter(crud.models.Task.assigned_to == assigned_to)
    tasks = q.order_by(crud.models.Task.created_at.desc()).all()
    return tasks


@router.patch("/{task_id}/status", response_model=TaskOut)
def update_status(task_id: int, status: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = crud.update_task_status(db, task_id, status)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.log_activity(db, current_user.id, "update_task", f"{task_id}:{status}")
    return task
