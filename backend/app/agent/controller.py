from app.agent.execution_trace import ExecutionTrace
from app.agent.tool_registry import ToolRegistry


class AgentController:

    def __init__(self):
        self.registry = ToolRegistry()

    def process(self, task: str):

        trace = ExecutionTrace()

        trace.add("Task received.")

        trace.add("Agent started processing.")

        return self.registry.execute(task, trace)
