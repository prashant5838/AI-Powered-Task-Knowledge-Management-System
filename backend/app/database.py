import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    try:
        import pymysql  # type: ignore
        DATABASE_URL = "mysql+pymysql://root:password@127.0.0.1:3306/ai_mvp"
    except Exception:
        # fallback to sqlite for local/dev when PyMySQL isn't installed
        DATABASE_URL = "sqlite:///./dev.db"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

def init_db():
    # create tables
    from app import models
    Base.metadata.create_all(bind=engine)
