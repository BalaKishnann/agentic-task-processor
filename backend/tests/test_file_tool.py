import pytest

# from pathlib import Path

from app.tools.file_tool import FileTool
from app.agent.execution_trace import ExecutionTrace


@pytest.fixture
def file_tool():
    return FileTool()


@pytest.fixture
def trace():
    return ExecutionTrace()


@pytest.fixture
def sample_file(file_tool):
    """Creates and cleans up a real file inside the allowed directory."""

    file_tool.ALLOWED_DIRECTORY.mkdir(parents=True, exist_ok=True)
    path = file_tool.ALLOWED_DIRECTORY / "sample.txt"
    path.write_text("hello world\nsecond line", encoding="utf-8")

    yield path

    path.unlink(missing_ok=True)


class TestCanHandle:

    @pytest.mark.parametrize(
        "task",
        [
            "read file: sample.txt",
            "show me the file content: notes.txt",
            "open file: data.csv",
        ],
    )
    def test_recognizes_file_keywords(self, file_tool, task):
        assert file_tool.can_handle(task) is True

    @pytest.mark.parametrize(
        "task",
        [
            "calculate 5 + 3",
            "what time is it",
        ],
    )
    def test_rejects_non_file_tasks(self, file_tool, task):
        assert file_tool.can_handle(task) is False


class TestExecute:

    def test_reads_existing_file_successfully(self, file_tool, trace, sample_file):
        result = file_tool.execute("read file: sample.txt", trace)

        assert result["status"] == "SUCCESS"
        assert result["result"]["file_name"] == "sample.txt"
        assert result["result"]["line_count"] == 2
        assert result["result"]["word_count"] == 4

    def test_missing_file_returns_failure(self, file_tool, trace):
        result = file_tool.execute("read file: does_not_exist.txt", trace)

        assert result["status"] == "FAILED"
        assert "does not exist" in result["message"]

    def test_no_filename_extracted_returns_failure(self, file_tool, trace):
        result = file_tool.execute("read file without a colon", trace)

        assert result["status"] == "FAILED"
        assert "Could not identify a filename" in result["message"]


class TestPathTraversalSecurity:
    """
    Directly targets the security fix — confirms escape attempts are
    rejected regardless of how they're phrased.
    """

    def test_rejects_relative_traversal(self, file_tool, trace):
        result = file_tool.execute("read file: ../../etc/passwd", trace)

        assert result["status"] == "FAILED"
        assert "traversal" in result["message"].lower()

    def test_rejects_absolute_path(self, file_tool, trace):
        result = file_tool.execute("read file: /etc/passwd", trace)

        assert result["status"] == "FAILED"
        assert "traversal" in result["message"].lower()

    def test_rejects_windows_style_traversal(self, file_tool, trace):
        result = file_tool.execute(
            r"read file: ..\..\Windows\System32\config\SAM", trace
        )

        assert result["status"] == "FAILED"

    def test_resolve_safe_path_directly_raises_on_traversal(self, file_tool):
        with pytest.raises(ValueError, match="traversal"):
            file_tool._resolve_safe_path("../../etc/passwd")

    def test_resolve_safe_path_accepts_valid_filename(self, file_tool):
        resolved = file_tool._resolve_safe_path("sample.txt")
        assert resolved.is_relative_to(file_tool.ALLOWED_DIRECTORY)
