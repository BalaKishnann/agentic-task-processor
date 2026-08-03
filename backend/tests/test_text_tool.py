import pytest

from app.tools.text_tool import TextTool
from app.agent.execution_trace import ExecutionTrace


@pytest.fixture
def text_tool():
    return TextTool()


@pytest.fixture
def trace():
    return ExecutionTrace()


class TestCanHandle:

    @pytest.mark.parametrize(
        "task",
        [
            "process this text",
            "convert to uppercase",
            "UPPERCASE this string",
        ],
    )
    def test_recognizes_text_keywords(self, text_tool, task):
        assert text_tool.can_handle(task) is True

    @pytest.mark.parametrize(
        "task",
        [
            "calculate 5 + 3",
            "what's the weather today",
            "what time is it",
        ],
    )
    def test_rejects_non_text_tasks(self, text_tool, task):
        assert text_tool.can_handle(task) is False


class TestExecute:

    def test_returns_success_status(self, text_tool, trace):
        result = text_tool.execute("process this text", trace)

        assert result["status"] == "SUCCESS"
        assert result["tool"] == "TextTool"

    def test_message_includes_original_task(self, text_tool, trace):
        result = text_tool.execute("uppercase hello world", trace)

        assert "uppercase hello world" in result["result"]["message"]

    def test_response_shape_matches_contract(self, text_tool, trace):
        result = text_tool.execute("some text task", trace)

        assert set(result.keys()) == {"tool", "status", "result", "message", "trace"}

    def test_response_includes_trace(self, text_tool, trace):
        result = text_tool.execute("some text task", trace)

        assert isinstance(result["trace"], list)
        assert len(result["trace"]) > 0
