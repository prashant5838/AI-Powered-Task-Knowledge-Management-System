from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import get_db, get_current_user
from app.services.embeddings import embed_texts
from app.services.vectorstore import store
from app import crud

router = APIRouter()


@router.get("/")
def search(q: str, top_k: int = 5, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not q:
        raise HTTPException(status_code=400, detail="query missing")
    emb = embed_texts([q])[0]
    results = store.search(emb, top_k=top_k)
    crud.log_activity(db, current_user.id, "search", q)
    return {"query": q, "results": results}
