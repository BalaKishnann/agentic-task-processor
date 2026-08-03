from datetime import datetime
from app.tools.base_tool import BaseTool


class DateTool(BaseTool):

    def can_handle(self, task: str):

        task = task.lower()

        keywords = ["date", "today", "current date"]

        return any(word in task for word in keywords)

    def execute(self, task: str, trace):

        today = datetime.now().strftime("%d %B %Y")

        trace.add("Current date generated.")

        return self.success(
            {"value": today},
            trace,
        )
