import os
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.auth import get_db, get_current_user, require_role
from app import crud
from app.services.embeddings import extract_text_from_pdf, embed_texts
from app.services.vectorstore import store

router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db), current_user=Depends(require_role("admin"))):
    # accept txt and pdf
    fname = file.filename
    dest = os.path.join(UPLOAD_DIR, fname)
    with open(dest, "wb") as f:
        f.write(file.file.read())
    text = None
    if fname.lower().endswith('.pdf'):
        text = extract_text_from_pdf(dest)
    elif fname.lower().endswith('.txt'):
        with open(dest, 'r', encoding='utf-8') as rf:
            text = rf.read()
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    doc = crud.create_document(db, filename=fname, content=text, uploaded_by=current_user.id)
    # split into chunks
    chunks = [text[i:i+1000] for i in range(0, len(text or ''), 1000)] if text else []
    if chunks:
        embs = embed_texts(chunks)
        metas = [{"doc_id": doc.id, "chunk_index": idx, "text": chunk[:500]} for idx, chunk in enumerate(chunks)]
        store.add(embs, metas)
    crud.log_activity(db, current_user.id, "upload_document", fname)
    return {"id": doc.id, "filename": fname}
