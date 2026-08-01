from app.tools.file_tool import FileTool


tool = FileTool()


result = tool.execute(
    "requirements.txt"
)


print(result)