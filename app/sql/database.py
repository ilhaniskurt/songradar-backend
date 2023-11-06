from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, declarative_base, sessionmaker

from app.utils.config import settings

engine = create_engine(
    settings.sqlalchemy_database_url, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: DeclarativeBase = declarative_base()
