import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Defaults to the existing local dev behavior (a file in the working
# directory) if DATABASE_URL isn't set. In Docker, this gets overridden
# via docker-compose.yml to point at the mounted volume, so data
# survives container rebuilds.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///agent.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()
