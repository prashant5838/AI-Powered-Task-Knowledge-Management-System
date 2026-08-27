# AI Task & Knowledge MVP (Backend)

Quick setup:

1. Create a Python venv and activate it.

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Prepare MySQL and environment variables. See `.env.example`.

3. Create DB and run the app:

```bash
export DATABASE_URL="mysql+pymysql://root:password@127.0.0.1:3306/ai_mvp"
uvicorn app.main:app --reload
```

Notes:
- Uses SentenceTransformers locally for embeddings and FAISS for vector store.
- Endpoints: `/auth/login`, `/tasks`, `/documents/upload`, `/search`, `/analytics`.

Docker (recommended)
--------------------
The easiest way to run the full stack (with FAISS and sentence-transformers) is via Docker Compose.

1. Build and start services:

```bash
docker-compose up --build
```

This brings up:
- MySQL on port `3306`
- Backend FastAPI on port `8000`
- Frontend dev server on port `3000`

Notes:
- When running locally without Docker on Windows, the project uses a lightweight pure-Python fallback embedding and vector store to avoid native build issues. For production/assessment, use Docker so the real embedding stack (FAISS + sentence-transformers) is installed in a Linux container.

Running tests and generating screenshots
--------------------------------------
1. Install test dependencies inside the backend venv (or in Docker):

```bash
cd backend
pip install -r requirements.txt
```

2. Run tests:

```bash
pytest -q
```

3. Generate placeholder screenshots (used for submission):

```bash
python scripts/generate_screenshots.py
```

Generated screenshots are saved to `backend/docs/screenshots`.
