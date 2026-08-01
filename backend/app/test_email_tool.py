from app.tools.email_tool import EmailTool

tool = EmailTool()

tasks = [
    "Send an email",
    "Email Bala about the meeting",
    "Mail the report to John",
    "What's the weather today?"
]

for task in tasks:

    if tool.can_handle(task):
        print(tool.execute(task))
    else:
        print(f"Cannot handle: {task}")