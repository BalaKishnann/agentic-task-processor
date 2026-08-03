from app.tools.base_tool import BaseTool


class TextAnalysisTool(BaseTool):

    def can_handle(self, task: str):

        task = task.lower()

        keywords = ["count words", "analyze text", "text analysis", "count characters"]

        return any(keyword in task for keyword in keywords)

    def execute(self, task: str, trace):

        trace.add("Text analysis requested.")

        task_lower = task.lower()

        if "count words in:" in task_lower:
            text = task.split(":", 1)[1].strip()

        elif "analyze text:" in task_lower:
            text = task.split(":", 1)[1].strip()

        else:
            text = task

        words = len(text.split())
        characters = len(text)
        lines = len(text.splitlines())

        trace.add("Text statistics calculated.")

        return self.success(
            {"words": words, "characters": characters, "lines": lines},
            trace,
        )
