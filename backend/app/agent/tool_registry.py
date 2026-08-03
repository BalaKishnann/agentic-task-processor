import logging

from app.tools.calculator_tool import CalculatorTool
from app.tools.text_tool import TextTool
from app.tools.weather_tool import WeatherTool
from app.tools.date_tool import DateTool
from app.tools.time_tool import TimeTool
from app.tools.text_analysis_tool import TextAnalysisTool
from app.tools.file_tool import FileTool
from app.tools.email_tool import EmailTool

from app.core.tool_metrics import tool_metrics

logger = logging.getLogger(__name__)


class ToolRegistry:

    def __init__(self):
        self.tools = [
            CalculatorTool(),
            TextTool(),
            WeatherTool(),
            DateTool(),
            TimeTool(),
            TextAnalysisTool(),
            FileTool(),
            EmailTool(),
        ]

    def execute(self, task: str, trace):

        trace.add("Searching registered tools.")

        for tool in self.tools:

            if tool.can_handle(task):

                tool_name = tool.__class__.__name__
                trace.add(f"{tool_name} matched the request.")

                with tool_metrics.track(tool_name):
                    result = tool.execute(task, trace)

                if result.get("status") != "SUCCESS":
                    logger.warning(
                        "Tool returned a failure result",
                        extra={
                            "tool": tool_name,
                            "tool_message": result.get("message"),
                        },
                    )

                return result

        trace.add("No matching tool found.")

        logger.info("No tool matched task", extra={"task_preview": task[:100]})

        return {
            "tool": None,
            "status": "FAILED",
            "result": None,
            "message": "No suitable tool found for this task.",
            "trace": trace.get_steps(),
        }
