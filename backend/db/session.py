from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://openmind_user:openmind@localhost:5432/openmind"

# Create engine
engine = create_engine(DATABASE_URL, echo=True, future=True)

# Session factory (your original)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# Base class for all models
Base = declarative_base()
