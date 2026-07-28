from fastapi import FastAPI

app = FastAPI(
    title="Agentic Task Processor API",
    description="Enterprise-grade Agentic Task Processing System",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "application": "Agentic Task Processor",
        "status": "Running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }
