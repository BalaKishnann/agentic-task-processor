from abc import ABC, abstractmethod


class BaseTool(ABC):

    @abstractmethod
    def can_handle(self, task: str) -> bool:
        pass

    @abstractmethod
    def execute(self, task: str):
        pass
