from app.tools.base_tool import BaseTool


class TextTool(BaseTool):

    def can_handle(self, task: str) -> bool:

        task = task.lower()

        return "text" in task or "uppercase" in task

    def execute(self, task: str, trace):

        trace.add("Text tool processing request.")

        return self.success(
            {"message": f"Text tool received: {task}"},
            trace,
        )
