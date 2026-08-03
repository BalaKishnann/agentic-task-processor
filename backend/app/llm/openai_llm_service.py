import os
import logging

from openai import OpenAI

from app.llm.base_llm import BaseLLM
from app.llm.prompt_builder import PromptBuilder

logger = logging.getLogger(__name__)


class OpenAILLMService(BaseLLM):

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def choose_tool(self, task: str, tools: list[str]) -> str | None:
        """
        Returns the selected tool name, or None if the model's response
        doesn't exactly match a known tool (including if the model was
        successfully manipulated into returning something else entirely —
        this allowlist check is what actually neutralizes injection here,
        not the prompt wording alone).
        """

        prompt = PromptBuilder.build_tool_selection_prompt(task, tools)

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI agent. You only ever return a single tool name, nothing else.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )

        raw_output = response.choices[0].message.content.strip()

        if raw_output not in tools:
            logger.warning(
                "LLM tool selection returned an unrecognized value",
                extra={"raw_output": raw_output[:200]},
            )
            return None

        return raw_output
