import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from apps.mcp_server.config import settings

# In local dev we assume running from the root of new_folder where offshore_logistics.db is
db_url = settings.DATABASE_URL
if db_url.startswith("sqlite:///"):
    pass

engine = create_engine(
    db_url,
    connect_args={"check_same_thread": False} if "sqlite" in db_url else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
