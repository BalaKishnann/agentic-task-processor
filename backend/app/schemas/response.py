from typing import Any, List, Optional
from pydantic import BaseModel


class TaskResponse(BaseModel):
    """Standard shape returned by every tool and by /tasks."""

    tool: Optional[str] = None
    status: str  # "SUCCESS" or "FAILED"
    result: Optional[Any] = None
    message: Optional[str] = None
    trace: List[str] = []


class TaskHistoryItem(BaseModel):
    id: int
    task: str
    tool: Optional[str] = None
    status: str
    result: Optional[Any] = None
    trace: List[str] = []
    created_at: Any  # datetime, left loose to match your existing model
