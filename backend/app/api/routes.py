from fastapi import APIRouter
from app.schemas.task import TaskRequest
from app.agent.controller import AgentController
from app.database.database import SessionLocal
from app.database.models import TaskHistory
import json

router = APIRouter()
agent = AgentController()

@router.post("/tasks")
def process_task(request: TaskRequest):

    return agent.process(request.task)

@router.get("/tasks/history")
def get_task_history():

    db = SessionLocal()

    try:
        tasks = (
            db.query(TaskHistory)
            .order_by(TaskHistory.id.desc())
            .all()
        )

        response = []

        for task in tasks:
            response.append({
                "id": task.id,
                "task": task.task,
                "tool": task.selected_tool,
                "status": task.status,
                "result": json.loads(task.result),
                "trace": json.loads(task.trace),
                "created_at": task.created_at
            })

        return response

    finally:
        db.close()
