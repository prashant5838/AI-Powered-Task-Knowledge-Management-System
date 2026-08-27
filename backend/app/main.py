import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, documents, tasks, search, analytics
from app.database import init_db


def create_app():
    app = FastAPI(title="AI Task & Knowledge MVP")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # include routers
    app.include_router(auth.router, prefix="/auth")
    app.include_router(tasks.router, prefix="/tasks")
    app.include_router(documents.router, prefix="/documents")
    app.include_router(search.router, prefix="/search")
    app.include_router(analytics.router, prefix="/analytics")
    return app


app = create_app()


@app.on_event("startup")
def on_startup():
    init_db()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
