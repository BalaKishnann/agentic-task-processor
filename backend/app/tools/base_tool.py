from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseTool(ABC):

    @abstractmethod
    def can_handle(self, task: str) -> bool:
        pass

    @abstractmethod
    def execute(self, task: str, trace) -> dict:
        pass

    # --- Shared response builders: every tool should return via these,  ---
    # --- so the shape is identical regardless of which tool handled it. ---

    def success(self, result: Any, trace, message: Optional[str] = None) -> dict:
        return {
            "tool": self.__class__.__name__,
            "status": "SUCCESS",
            "result": result,
            "message": message,
            "trace": trace.get_steps(),
        }

    def failure(self, message: str, trace, result: Any = None) -> dict:
        return {
            "tool": self.__class__.__name__,
            "status": "FAILED",
            "result": result,
            "message": message,
            "trace": trace.get_steps(),
        }
