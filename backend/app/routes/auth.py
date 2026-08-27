from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.auth import create_access_token, verify_password, get_db, get_current_user
from app import crud
from app.schemas import AuthResponse
from app.schemas import UserOut

router = APIRouter()


@router.post("/login", response_model=AuthResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    role = user.role.name if user.role else 'user'
    token = create_access_token({"sub": str(user.id), "role": role})
    crud.log_activity(db, user.id, "login", None)
    return {"access_token": token, "token_type": "bearer", "role": role, "user": user}


@router.get('/me')
def me(current_user=Depends(get_current_user)):
    # return current user and role
    if current_user is None:
        raise HTTPException(status_code=401, detail='Not authenticated')
    role = current_user.role.name if current_user.role else 'user'
    return {"user": UserOut.from_orm(current_user), "role": role}
