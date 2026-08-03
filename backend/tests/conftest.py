import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.database.database import Base
from app.main import app


@pytest.fixture(scope="function")
def test_db(monkeypatch):

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # <-- keeps one connection alive for the whole engine,
        #     so every SessionLocal() call hits the same
        #     in-memory database instead of a fresh empty one
    )

    TestSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    monkeypatch.setattr("app.api.routes.SessionLocal", TestSessionLocal)
    monkeypatch.setattr("app.agent.controller.SessionLocal", TestSessionLocal)

    yield TestSessionLocal

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    return TestClient(app)
