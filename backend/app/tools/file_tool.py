from pathlib import Path
from datetime import datetime

from app.tools.base_tool import BaseTool


class FileTool(BaseTool):

    # Files can only be read from inside this directory. Any path that
    # resolves outside of it — via "../", an absolute path, or a symlink —
    # is rejected. This is the actual security boundary; the "read file:"
    # prefix parsing below is just convenience, not the safety mechanism.
    ALLOWED_DIRECTORY = (Path(__file__).parent.parent / "data" / "uploads").resolve()

    def can_handle(self, task: str) -> bool:

        task = task.lower()

        keywords = ["read file", "file content", "open file"]

        return any(keyword in task for keyword in keywords)

    def execute(self, task: str, trace):

        trace.add("File read requested.")

        filename = self._extract_filename(task)

        if filename is None:
            return self.failure(
                "Could not identify a filename. Use the format: read file: <filename>",
                trace,
            )

        try:
            resolved_path = self._resolve_safe_path(filename)
        except ValueError as ex:
            trace.add("Rejected path outside allowed directory.")
            return self.failure(str(ex), trace)

        if not resolved_path.exists():
            return self.failure(f"File '{filename}' does not exist.", trace)

        if not resolved_path.is_file():
            return self.failure(f"'{filename}' is not a file.", trace)

        try:
            content = self._read_with_fallback_encoding(resolved_path)
        except Exception as ex:
            return self.failure(f"Could not read file: {ex}", trace)

        trace.add("File content read successfully.")

        lines = content.splitlines()
        stat = resolved_path.stat()

        metadata = {
            "file_name": resolved_path.name,
            "file_size_bytes": stat.st_size,
            "created_time": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "line_count": len(lines),
            "character_count": len(content),
            "word_count": len(content.split()),
        }

        trace.add("File metadata calculated.")

        return self.success(metadata, trace)

    def _extract_filename(self, task: str) -> str | None:

        task_lower = task.lower()

        for prefix in ["read file:", "file content:", "open file:"]:
            if prefix in task_lower:
                index = task_lower.index(prefix) + len(prefix)
                return task[index:].strip()

        return None

    def _resolve_safe_path(self, filename: str) -> Path:
        """
        Resolves filename against ALLOWED_DIRECTORY and verifies the
        result is actually still inside it. Raises ValueError if the
        filename attempts to escape (e.g. "../../etc/passwd").
        """

        # Reject anything that looks like a path traversal or absolute
        # path attempt outright, before even touching the filesystem.
        candidate = Path(filename)

        if candidate.is_absolute() or ".." in candidate.parts:
            raise ValueError("Invalid filename: path traversal is not allowed.")

        resolved = (self.ALLOWED_DIRECTORY / candidate).resolve()

        # Belt-and-suspenders: even after the above check, confirm the
        # resolved path is genuinely still within the allowed directory
        # (catches symlink-based escapes the string check above can't).
        if not resolved.is_relative_to(self.ALLOWED_DIRECTORY):
            raise ValueError("Invalid filename: path traversal is not allowed.")

        return resolved

    def _read_with_fallback_encoding(self, path: Path) -> str:

        encodings = ["utf-8", "utf-16", "latin-1"]

        for encoding in encodings:
            try:
                return path.read_text(encoding=encoding)
            except UnicodeDecodeError:
                continue

        raise ValueError("Unsupported file encoding.")
