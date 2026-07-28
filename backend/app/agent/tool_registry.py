from app.tools.calculator_tool import CalculatorTool
from app.tools.text_tool import TextTool
from app.tools.weather_tool import WeatherTool


class ToolRegistry:

    def __init__(self):

        self.tools = [
            CalculatorTool(),
            TextTool(),
            WeatherTool()
        ]

    def execute(self, task: str):

        for tool in self.tools:

            if tool.can_handle(task):
                return tool.execute(task)

        return {
            "tool": "Unknown",
            "message": "No suitable tool found."
        }
