from fastapi import APIRouter

from app.schemas.task import TaskRequest
from app.agent.controller import AgentController

router = APIRouter()

agent = AgentController()


@router.post("/tasks")
def process_task(request: TaskRequest):

    return agent.process(request.task)
