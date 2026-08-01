class PromptBuilder:

    @staticmethod
    def build_tool_selection_prompt(task: str, tools: list[str]) -> str:

        tool_list = "\n".join(f"- {tool}" for tool in tools)

        return f"""
You are an AI Agent.

Available tools:

{tool_list}

User Request:
{task}

Return ONLY the exact tool name that should handle the request.

Do not explain.
Do not add extra text.
Return only one tool name.
"""