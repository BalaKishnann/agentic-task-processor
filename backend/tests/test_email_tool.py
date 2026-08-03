import pytest

from app.tools.email_tool import EmailTool
from app.agent.execution_trace import ExecutionTrace


@pytest.fixture
def email_tool():
    return EmailTool()


@pytest.fixture
def trace():
    return ExecutionTrace()


class TestCanHandle:

    @pytest.mark.parametrize(
        "task",
        [
            "send an email to John",
            "mail this report",
            "email the summary",
        ],
    )
    def test_recognizes_email_keywords(self, email_tool, task):
        assert email_tool.can_handle(task) is True

    @pytest.mark.parametrize(
        "task",
        [
            "calculate 5 + 3",
            "what time is it",
        ],
    )
    def test_rejects_non_email_tasks(self, email_tool, task):
        assert email_tool.can_handle(task) is False


class TestExecute:

    def test_returns_success_status_exact_case(self, email_tool, trace):
        result = email_tool.execute("send an email", trace)

        # Deliberately asserts exact casing — routes.py checks
        # response["status"] == "SUCCESS" verbatim, so "Success" or
        # "success" would silently be treated as a failure (400).
        assert result["status"] == "SUCCESS"

    def test_tool_name_matches_class(self, email_tool, trace):
        result = email_tool.execute("send an email", trace)

        assert result["tool"] == "EmailTool"

    def test_returns_mock_recipient_and_subject(self, email_tool, trace):
        result = email_tool.execute("email the report", trace)

        assert result["result"]["recipient"] == "demo@example.com"
        assert result["result"]["subject"] == "Mock Email"

    def test_returns_confirmation_message(self, email_tool, trace):
        result = email_tool.execute("send an email", trace)

        assert "simulation" in result["message"].lower()

    def test_response_shape_matches_contract(self, email_tool, trace):
        result = email_tool.execute("send an email", trace)

        assert set(result.keys()) == {"tool", "status", "result", "message", "trace"}

    def test_response_includes_trace(self, email_tool, trace):
        result = email_tool.execute("send an email", trace)

        assert len(result["trace"]) > 0
