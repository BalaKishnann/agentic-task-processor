from datetime import datetime
from app.tools.base_tool import BaseTool


class TimeTool(BaseTool):

    @property
    def name(self):
        return "Time Tool"

    def can_handle(self, task: str):

        task = task.lower()

        keywords = [
            "time",
            "current time",
            "what time"
        ]

        return any(keyword in task for keyword in keywords)

    def execute(self, task: str, trace):

        trace.add("Current time requested.")

        current_time = datetime.now().strftime("%I:%M:%S %p")

        trace.add("Current time generated.")

        return {
            "tool": self.name,
            "status": "SUCCESS",
            "result": {
                "value": current_time
            },
            "trace": trace.get_trace()
        }