import pytest
from datetime import datetime

from app.tools.date_tool import DateTool
from app.agent.execution_trace import ExecutionTrace


@pytest.fixture
def date_tool():
    return DateTool()


@pytest.fixture
def trace():
    return ExecutionTrace()


class TestCanHandle:

    @pytest.mark.parametrize(
        "task",
        [
            "what's today's date",
            "give me the current date",
            "what date is it",
        ],
    )
    def test_recognizes_date_keywords(self, date_tool, task):
        assert date_tool.can_handle(task) is True

    @pytest.mark.parametrize(
        "task",
        [
            "calculate 5 + 3",
            "what time is it",
            "what's the weather",
        ],
    )
    def test_rejects_non_date_tasks(self, date_tool, task):
        assert date_tool.can_handle(task) is False


class TestExecute:

    def test_returns_success_status(self, date_tool, trace):
        result = date_tool.execute("what's today's date", trace)

        assert result["status"] == "SUCCESS"
        assert result["tool"] == "DateTool"

    def test_returns_correctly_formatted_date(self, date_tool, trace):
        result = date_tool.execute("what's today's date", trace)

        expected = datetime.now().strftime("%d %B %Y")
        assert result["result"]["value"] == expected

    def test_response_shape_matches_contract(self, date_tool, trace):
        result = date_tool.execute("what's the date", trace)

        assert set(result.keys()) == {"tool", "status", "result", "message", "trace"}

    def test_response_includes_trace(self, date_tool, trace):
        result = date_tool.execute("what's the date", trace)

        assert "Current date generated." in result["trace"]
