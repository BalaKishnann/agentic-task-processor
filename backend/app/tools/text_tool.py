from app.tools.base_tool import BaseTool


class TextTool(BaseTool):

    def can_handle(self, task: str) -> bool:

        task = task.lower()

        return "text" in task or "uppercase" in task

    def execute(self, task: str):

        return {
            "tool": "Text",
            "message": f"Text tool received: {task}"
        }
