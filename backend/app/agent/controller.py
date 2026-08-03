import json
from app.agent.execution_trace import ExecutionTrace
from app.agent.tool_registry import ToolRegistry
from app.database.database import SessionLocal
from app.database.models import TaskHistory


class AgentController:

    def __init__(self):
        self.registry = ToolRegistry()

    def process(self, task: str) -> dict:

        trace = ExecutionTrace()
        trace.add("Task received.")
        trace.add("Agent started processing.")

        response = self.registry.execute(task, trace)

        # Every tool now returns via BaseTool.success()/failure(), and the
        # registry's own no-match branch matches the same shape — so these
        # keys are guaranteed to exist. .get() is kept as a defensive
        # fallback in case a tool is ever updated incorrectly.
        db = SessionLocal()
        try:
            history = TaskHistory(
                task=task,
                selected_tool=response.get("tool"),
                status=response.get("status", "FAILED"),
                result=json.dumps(response.get("result")),
                trace=json.dumps(response.get("trace", [])),
            )

            db.add(history)
            db.commit()
            db.refresh(history)

            print(f"✅ Task saved successfully, ID={history.id}")

        except Exception as ex:
            db.rollback()
            print(f"❌ Database Error: {type(ex).__name__} {ex}")
            # DB failure shouldn't be silently swallowed, but it also
            # shouldn't be indistinguishable from a tool failure — mark it.
            response = {
                "tool": response.get("tool"),
                "status": "FAILED",
                "result": None,
                "message": "Task processed, but saving to history failed.",
                "trace": response.get("trace", []),
            }
        finally:
            db.close()

        return response
