from sqlalchemy.orm import Session
from app import models
# avoid circular import: import get_password_hash inside create_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, email: str, password: str, full_name: str = None, role=None):
    from app.auth import get_password_hash
    hashed = get_password_hash(password)
    user = models.User(email=email, hashed_password=hashed, full_name=full_name)
    if role:
        user.role = role
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_role_if_not_exists(db: Session, name: str):
    role = db.query(models.Role).filter(models.Role.name == name).first()
    if not role:
        role = models.Role(name=name)
        db.add(role)
        db.commit()
        db.refresh(role)
    return role

def create_document(db: Session, filename: str, content: str, uploaded_by: int | None = None):
    doc = models.Document(filename=filename, content=content, uploaded_by=uploaded_by)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

def create_task(db: Session, title: str, description: str = None, assigned_to: int | None = None):
    task = models.Task(title=title, description=description, assigned_to=assigned_to)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task_status(db: Session, task_id: int, status: str):
    task = db.query(models.Task).get(task_id)
    if not task:
        return None
    task.status = status
    db.commit()
    db.refresh(task)
    return task

def log_activity(db: Session, user_id: int | None, action: str, metadata: str | None = None):
    a = models.ActivityLog(user_id=user_id, action=action, meta=metadata)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a
