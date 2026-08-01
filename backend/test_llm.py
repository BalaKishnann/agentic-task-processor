from dotenv import load_dotenv

load_dotenv()

from app.llm.openai_llm_service import OpenAILLMService


llm = OpenAILLMService()

tools = [

    "File Tool",

    "Weather Tool",

    "Email Tool",

    "Text Analysis Tool"

]

task = "Please count the words in this paragraph."

selected = llm.choose_tool(task, tools)

print(selected)