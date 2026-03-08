from abc import ABC, abstractmethod


class DialogueProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def generate(
        self, system_prompt: str, user_prompt: str, temperature: float = 0.7, max_tokens: int = 250
    ) -> str:
        raise NotImplementedError
