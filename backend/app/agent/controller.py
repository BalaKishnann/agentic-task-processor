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
            db.close()
            
            print("✅ Task saved successfully")
            return response
        except:
            print(f"❌ Database Error: {ex}")
        finally:
            db.close()     
