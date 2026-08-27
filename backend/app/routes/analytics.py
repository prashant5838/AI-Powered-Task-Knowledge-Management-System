from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth import get_db, require_role
from app import crud, models

router = APIRouter()


@router.get("/")
def analytics(db: Session = Depends(get_db), current_user=Depends(require_role("admin"))):
    total_tasks = db.query(models.Task).count()
    completed = db.query(models.Task).filter(models.Task.status == 'completed').count()
    pending = db.query(models.Task).filter(models.Task.status != 'completed').count()
    # most searched queries: we stored raw query in activity_logs metadata for search
    q = db.query(models.ActivityLog).filter(models.ActivityLog.action == 'search').all()
    counts = {}
    for a in q:
        key = (a.metadata or '').strip()
        counts[key] = counts.get(key, 0) + 1
    top_searches = sorted([{"query": k, "count": v} for k, v in counts.items()], key=lambda x: x['count'], reverse=True)[:10]
    return {"total_tasks": total_tasks, "completed": completed, "pending": pending, "top_searches": top_searches}
