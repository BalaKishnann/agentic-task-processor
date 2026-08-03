from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.task import TaskRequest
from app.schemas.response import TaskResponse, TaskHistoryItem
from app.agent.controller import AgentController
from app.database.database import SessionLocal
from app.database.models import TaskHistory
from app.core.tool_metrics import tool_metrics
from app.core.rate_limiter import limiter
import json

router = APIRouter()
agent = AgentController()


@router.post("/tasks", response_model=TaskResponse)
@limiter.limit("30/minute")
async def process_task(request: Request, request_body: TaskRequest):

    response = agent.process(request_body.task)

    status_code = 200 if response.get("status") == "SUCCESS" else 400

    return JSONResponse(status_code=status_code, content=response)


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


@router.delete("/tasks/history")
def clear_task_history():
    """Deletes all task history rows."""

    db = SessionLocal()

    try:
        deleted_count = db.query(TaskHistory).delete()
        db.commit()

        return {
            "status": "SUCCESS",
            "message": f"Deleted {deleted_count} task history entries.",
        }

    except Exception as ex:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"status": "FAILED", "message": f"Failed to clear history: {ex}"},
        )

    finally:
        db.close()


@router.delete("/tasks/history/{task_id}")
def delete_task_history_entry(task_id: int):
    """Deletes a single task history row by ID."""

    db = SessionLocal()

    try:
        task = db.query(TaskHistory).filter(TaskHistory.id == task_id).first()

        if task is None:
            raise HTTPException(
                status_code=404, detail=f"Task history entry {task_id} not found."
            )

        db.delete(task)
        db.commit()

        return {
            "status": "SUCCESS",
            "message": f"Deleted task history entry {task_id}.",
        }

    except HTTPException:
        raise
    except Exception as ex:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"status": "FAILED", "message": f"Failed to delete entry: {ex}"},
        )

    finally:
        db.close()


@router.get("/metrics/tools")
def get_tool_metrics():
    return tool_metrics.snapshot()
