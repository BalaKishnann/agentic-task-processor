import pytest
import re

# from datetime import datetime

from app.tools.time_tool import TimeTool
from app.agent.execution_trace import ExecutionTrace


@pytest.fixture
def time_tool():
    return TimeTool()


@pytest.fixture
def trace():
    return ExecutionTrace()


class TestCanHandle:

    @pytest.mark.parametrize(
        "task",
        [
            "what time is it",
            "give me the current time",
            "what's the time right now",
        ],
    )
    def test_recognizes_time_keywords(self, time_tool, task):
        assert time_tool.can_handle(task) is True

    @pytest.mark.parametrize(
        "task",
        [
            "calculate 5 + 3",
            "what's today's date",
            "what's the weather",
        ],
    )
    def test_rejects_non_time_tasks(self, time_tool, task):
        assert time_tool.can_handle(task) is False


class TestExecute:

    def test_returns_success_status(self, time_tool, trace):
        result = time_tool.execute("what time is it", trace)

        assert result["status"] == "SUCCESS"
        assert result["tool"] == "TimeTool"

    def test_returns_time_in_correct_format(self, time_tool, trace):
        result = time_tool.execute("what time is it", trace)

        # e.g. "02:45:09 PM" — HH:MM:SS AM/PM
        pattern = r"^\d{2}:\d{2}:\d{2} (AM|PM)$"
        assert re.match(pattern, result["result"]["value"])

    def test_response_shape_matches_contract(self, time_tool, trace):
        result = time_tool.execute("what time is it", trace)

        assert set(result.keys()) == {"tool", "status", "result", "message", "trace"}

    def test_response_includes_trace_steps(self, time_tool, trace):
        result = time_tool.execute("what time is it", trace)

        assert "Current time requested." in result["trace"]
        assert "Current time generated." in result["trace"]
