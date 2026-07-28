from fastapi import FastAPI
from app.api.routes import router
from app.database.database import Base, engine
from app.database.models import TaskHistory

app = FastAPI(
    title="Agentic Task Processor API",
    version="1.0.0"
)

app.include_router(router)
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {
        "application": "Agentic Task Processor",
        "status": "Running"
    }


@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }
