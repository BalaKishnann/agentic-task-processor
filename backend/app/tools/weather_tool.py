from app.tools.base_tool import BaseTool


class WeatherTool(BaseTool):

    def can_handle(self, task: str) -> bool:

        return "weather" in task.lower()

    def execute(self, task: str):

        return {
            "tool": "Weather",
            "message": f"Weather tool received: {task}"
        }
