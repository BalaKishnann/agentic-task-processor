from app.tools.base_tool import BaseTool


class CalculatorTool(BaseTool):

    def can_handle(self, task: str) -> bool:

        task = task.lower()

        keywords = [
            "calculate",
            "add",
            "subtract",
            "multiply",
            "divide"
        ]

        return any(word in task for word in keywords)

    def execute(self, task: str):

        return {
            "tool": "Calculator",
            "message": f"Calculator received: {task}"
        }
