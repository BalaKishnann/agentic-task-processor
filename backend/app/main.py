from dotenv import load_dotenv
from fastapi import FastAPI
from app.api.routes import router
from app.database.database import Base, engine
from app.database.models import TaskHistory
from fastapi.middleware.cors import CORSMiddleware
from app.llm.openai_llm_service import OpenAILLMService

load_dotenv()

app = FastAPI(
    title="Agentic Task Processor API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
