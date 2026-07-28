import re

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

    """def execute(self, task: str):"""
    def execute(self, task: str, trace):

        expression = self.parse_expression(task)

        if expression is None:
            return {
                "tool": "Calculator",
                "status": "FAILED",
                "message": "Unable to identify a valid mathematical expression."
            }

        try:
            result = eval(expression)

            return {
                "tool": "Calculator",
                "status": "SUCCESS",
                "expression": expression,
                "result": result
            }

        except Exception as ex:
            return {
                "tool": "Calculator",
                "status": "FAILED",
                "message": str(ex)
            }

    def parse_expression(self, task: str):

        task = task.lower()

        task = task.replace("calculate", "")

        match = re.search(r'(\d+\s*[\+\-\*/]\s*\d+)', task)

        if match:
            return match.group(1)

        return None
