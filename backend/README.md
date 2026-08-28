# AI Task & Knowledge MVP

## Local setup

Create a virtual environment and install the backend dependencies from the
repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
```

### Run locally without Docker

The local Windows fallback uses SQLite. Run the backend from `backend`:

```powershell
$env:DATABASE_URL = "sqlite:///./dev.db"
Set-Location backend
..\.venv\Scripts\python.exe scripts\init_db.py
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

In a second terminal, start the frontend:

```powershell
Set-Location frontend
npm.cmd install
npm.cmd start
```

Open the application at <http://localhost:3000>. The backend API and Swagger
documentation are available at <http://localhost:8000> and
<http://localhost:8000/docs>. The initialized development account is
`admin@example.com` with password `adminpass`.

To use MySQL instead, set `DATABASE_URL` to a reachable MySQL connection before
starting the backend, for example:

```powershell
$env:DATABASE_URL = "mysql+pymysql://root:rootpass@127.0.0.1:3306/ai_mvp"
```

## Docker

Docker Desktop must be installed and running. From the repository root:

```bash
docker compose up --build
```

Docker Compose starts MySQL on port `3306`, the backend on port `8000`, and the
frontend on port `3000`.

When running locally without Docker on Windows, the project uses SQLite plus a
lightweight fallback embedding/vector store when the native embedding stack is
unavailable.

## Tests and screenshots

Run the tests from the backend directory:

```powershell
Set-Location backend
..\.venv\Scripts\python.exe -m pytest -q
```

Generate placeholder screenshots with:

```powershell
..\.venv\Scripts\python.exe scripts\generate_screenshots.py
```

Generated screenshots are saved to `backend/docs/screenshots`.

## API endpoints

- `POST /auth/login` and `GET /auth/me`
- `GET /tasks` and `POST /tasks`
- `PATCH /tasks/{task_id}/status`
- `POST /documents/upload`
- `GET /search`
- `GET /analytics`
