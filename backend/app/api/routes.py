from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.schemas.task import TaskRequest
from app.schemas.response import TaskResponse, TaskHistoryItem
from app.agent.controller import AgentController
from app.database.database import SessionLocal
from app.database.models import TaskHistory
import json
from app.core.tool_metrics import tool_metrics

# from app.main import limiter
from app.core.rate_limiter import limiter

router = APIRouter()
agent = AgentController()


@router.post("/tasks", response_model=TaskResponse)
@limiter.limit("30/minute")
async def process_task(request: Request, request_body: TaskRequest):

    response = agent.process(
        request_body.task
    )  # ← must be request_body.task, not request.task

    status_code = 200 if response.get("status") == "SUCCESS" else 400

    return JSONResponse(status_code=status_code, content=response)


@router.get("/metrics/tools")
def get_tool_metrics():
    return tool_metrics.snapshot()


@router.get("/tasks/history", response_model=list[TaskHistoryItem])
def get_task_history():

    db = SessionLocal()

    try:
        tasks = db.query(TaskHistory).order_by(TaskHistory.id.desc()).all()

        response = []

        for task in tasks:
            response.append(
                {
                    "id": task.id,
                    "task": task.task,
                    "tool": task.selected_tool,
                    "status": task.status,
                    "result": json.loads(task.result) if task.result else None,
                    "trace": json.loads(task.trace) if task.trace else [],
                    "created_at": task.created_at,
                }
            )

        return response

    except Exception as ex:
        return JSONResponse(
            status_code=500,
            content={
                "status": "FAILED",
                "message": f"Failed to fetch task history: {ex}",
            },
        )

    finally:
        db.close()
