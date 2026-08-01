from datetime import datetime
from app.tools.base_tool import BaseTool


class DateTool(BaseTool):

    @property
    def name(self):
        return "Date Tool"

    def can_handle(self, task: str):

        task = task.lower()

        keywords = [
            "date",
            "today",
            "current date"
        ]

        return any(word in task for word in keywords)

    def execute(self, task: str, trace):

        # trace.add("DateTool matched the request.")

        today = datetime.now().strftime("%d %B %Y")

        trace.add("Current date generated.")

        return {
            "tool": self.name,
            "status": "SUCCESS",
            "result": {
                "value": today
            },
            "trace": trace.get_trace()
        }