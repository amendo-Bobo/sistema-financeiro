"""Database configuration e models base"""
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.config import get_settings

settings = get_settings()

# Criar engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# SessionLocal para dependência
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para models
Base = declarative_base()

# Dependency para FastAPI
def get_db() -> Session:
    """Retorna uma sessão de banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
