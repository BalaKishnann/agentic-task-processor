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

  def execute(self, task: str, trace):

        trace.add("Searching registered tools.")

        for tool in self.tools:

            if tool.can_handle(task):

                trace.add(f"{tool.__class__.__name__} matched the request.")

                return tool.execute(task, trace)

        trace.add("No matching tool found.")

        return {
            "status": "FAILED",
            "message": "No suitable tool found.",
            "trace": trace.get_steps()
        }
