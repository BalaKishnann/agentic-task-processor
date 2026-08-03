import pytest

from app.tools.text_analysis_tool import TextAnalysisTool
from app.agent.execution_trace import ExecutionTrace


@pytest.fixture
def text_analysis_tool():
    return TextAnalysisTool()


@pytest.fixture
def trace():
    return ExecutionTrace()


class TestCanHandle:

    @pytest.mark.parametrize(
        "task",
        [
            "count words in this sentence",
            "analyze text: hello world",
            "please do a text analysis",
            "count characters in this",
        ],
    )
    def test_recognizes_analysis_keywords(self, text_analysis_tool, task):
        assert text_analysis_tool.can_handle(task) is True

    @pytest.mark.parametrize(
        "task",
        [
            "calculate 5 + 3",
            "what time is it",
            "what's the weather",
        ],
    )
    def test_rejects_non_analysis_tasks(self, text_analysis_tool, task):
        assert text_analysis_tool.can_handle(task) is False


class TestExecute:

    def test_returns_success_status(self, text_analysis_tool, trace):
        result = text_analysis_tool.execute("analyze text: hello world", trace)

        assert result["status"] == "SUCCESS"
        assert result["tool"] == "TextAnalysisTool"

    def test_extracts_text_after_count_words_in_prefix(self, text_analysis_tool, trace):
        result = text_analysis_tool.execute(
            "count words in: the quick brown fox", trace
        )

        assert result["result"]["words"] == 4

    def test_extracts_text_after_analyze_text_prefix(self, text_analysis_tool, trace):
        result = text_analysis_tool.execute("analyze text: one two three", trace)

        assert result["result"]["words"] == 3

    def test_falls_back_to_full_task_when_no_prefix(self, text_analysis_tool, trace):
        # "text analysis" matches can_handle's keyword but has no colon
        # prefix, so the whole task string is analyzed as-is.
        result = text_analysis_tool.execute("text analysis of something", trace)

        assert result["result"]["words"] == 4

    def test_character_count(self, text_analysis_tool, trace):
        result = text_analysis_tool.execute("analyze text: abc", trace)

        assert result["result"]["characters"] == 3

    def test_line_count_single_line(self, text_analysis_tool, trace):
        result = text_analysis_tool.execute("analyze text: one line here", trace)

        assert result["result"]["lines"] == 1

    def test_line_count_multiple_lines(self, text_analysis_tool, trace):
        result = text_analysis_tool.execute(
            "analyze text: line one\nline two\nline three", trace
        )

        assert result["result"]["lines"] == 3

    def test_empty_text_after_prefix(self, text_analysis_tool, trace):
        result = text_analysis_tool.execute("analyze text:", trace)

        assert result["result"]["words"] == 0
        assert result["result"]["characters"] == 0
        assert result["result"]["lines"] == 0

    def test_response_shape_matches_contract(self, text_analysis_tool, trace):
        result = text_analysis_tool.execute("analyze text: sample", trace)

        assert set(result.keys()) == {"tool", "status", "result", "message", "trace"}
