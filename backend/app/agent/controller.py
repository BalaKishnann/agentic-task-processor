from app.agent.tool_registry import ToolRegistry


class AgentController:

    def __init__(self):
        self.registry = ToolRegistry()

    def process(self, task: str):

        return self.registry.execute(task)
