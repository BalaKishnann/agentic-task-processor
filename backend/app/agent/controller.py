import json
from app.agent.execution_trace import ExecutionTrace
from app.agent.tool_registry import ToolRegistry
from app.database.database import SessionLocal
from app.database.models import TaskHistory

class AgentController:

    def __init__(self):
        self.registry = ToolRegistry()

    def process(self, task: str):

        trace = ExecutionTrace()

        trace.add("Task received.")

        trace.add("Agent started processing.")

        response = self.registry.execute(task, trace)
        try:
            db = SessionLocal()

            history = TaskHistory(
                task=task,
                selected_tool=response["tool"],
                status=response["status"],
                result=json.dumps(response["result"]),
                trace=json.dumps(response["trace"])
            )

            db.add(history)
            db.commit()
            db.refresh(history)
            
            print(f"✅ Task saved successfully, ID={history.id}")
            return response
        except Exception as ex:
            db.rollback()
            print(f"❌ Database Error: {type(ex).__name__} {ex}")
            raise
            
        finally:
            db.close()     
