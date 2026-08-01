from importlib.resources import path
from pathlib import Path
from datetime import datetime


class FileTool:

    name = "file_tool"

    description = """
    Reads a text file and extracts metadata.
    """

    def read_file_content(path):

        encodings = [
            "utf-8",
            "utf-16",
            "latin-1"
        ]

        for encoding in encodings:

            try:
                return path.read_text(
                    encoding=encoding
                )

            except UnicodeDecodeError:
                continue


        raise Exception(
            "Unsupported file encoding"
        )


    def execute(self, file_path: str):

        path = Path(file_path)

        if not path.exists():
            return {
                "error": "File does not exist"
            }


        if not path.is_file():
            return {
                "error": "Path is not a file"
            }


        # Read file
        try:
            #content = self.read_file_content(path)
            content = path.read_text(
                encoding="utf-8"
            )
        except UnicodeDecodeError:
            content = path.read_text(
            encoding="utf-16"
            )

        # Count lines
        lines = content.splitlines()


        metadata = {

            "file_name": path.name,

            "file_size_bytes": path.stat().st_size,

            "created_time":
                datetime.fromtimestamp(
                    path.stat().st_ctime
                ).isoformat(),

            "modified_time":
                datetime.fromtimestamp(
                    path.stat().st_mtime
                ).isoformat(),

            "line_count":
                len(lines),

            "character_count":
                len(content),

            "word_count":
                len(content.split())

        }


        return metadata