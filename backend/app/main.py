from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="Agentic Task Processor API",
    version="1.0.0"
)

app.include_router(router)


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
