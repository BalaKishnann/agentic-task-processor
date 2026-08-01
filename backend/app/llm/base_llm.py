from abc import ABC, abstractmethod


class BaseLLM(ABC):

    @abstractmethod
    def choose_tool(self, task: str, tools: list[str]) -> str:
        """
        Returns the selected tool name.
        """
        pass