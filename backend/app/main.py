import logging
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.api.routes import router
from app.core.config import get_settings
from app.core.logging_config import configure_logging
from app.database.database import Base, engine

# from app.database.models import TaskHistory
# from app.llm.openai_llm_service import OpenAILLMService

settings = get_settings()
configure_logging(settings.LOG_LEVEL, json_format=settings.LOG_JSON)
logger = logging.getLogger(__name__)

logger.info(
    "Starting Agentic Task Processor API", extra={"environment": settings.ENVIRONMENT}
)

app = FastAPI(title="Agentic Task Processor API", version="1.0.0")

# --- Rate limiting ---
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"],
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- CORS, hardened: explicit methods/headers instead of "*" ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=settings.cors_methods_list,
    allow_headers=settings.cors_headers_list,
)


@app.middleware("http")
async def log_requests(request: Request, call_next):

    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    logger.info(
        "Request received",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
        },
    )

    try:
        response = await call_next(request)
    except Exception:
        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        logger.error(
            "Request failed with unhandled exception",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "duration_ms": duration_ms,
            },
            exc_info=True,
        )
        raise

    duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

    logger.info(
        "Request completed",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
        },
    )

    response.headers["X-Request-ID"] = request_id

    return response


app.include_router(router)
Base.metadata.create_all(bind=engine)

logger.info("Database tables initialized.")


@app.get("/")
def root():
    return {"application": "Agentic Task Processor", "status": "Running"}


@app.get("/health")
def health():
    return {"status": "Healthy"}
