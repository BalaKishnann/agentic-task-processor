import os

from openai import OpenAI

from app.llm.base_llm import BaseLLM
from app.llm.prompt_builder import PromptBuilder


class OpenAILLMService(BaseLLM):

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def choose_tool(self, task: str, tools: list[str]) -> str:

        prompt = PromptBuilder.build_tool_selection_prompt(
            task,
            tools
        )

        response = self.client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[
                {
                    "role": "system",
                    "content": "You are an AI agent."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0

        )

        return response.choices[0].message.content.strip()