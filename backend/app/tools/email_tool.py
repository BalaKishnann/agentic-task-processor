from app.tools.base_tool import BaseTool


class EmailTool(BaseTool):

    def can_handle(self, task: str) -> bool:

        keywords = [
            "email",
            "mail",
            "send"
        ]

        return any(
            keyword in task.lower()
            for keyword in keywords
        )

    def execute(self, task: str):

        return {
            "tool": "EmailMockTool",
            "status": "Success",
            "recipient": "demo@example.com",
            "subject": "Mock Email",
            "message": "Email sent successfully (simulation)."
        }