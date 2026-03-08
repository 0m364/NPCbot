import requests

from dialogue_engine.adapters.base import DialogueProvider


class OllamaProvider(DialogueProvider):
    def __init__(self, endpoint: str, model: str, timeout_seconds: int = 90):
        self._endpoint = endpoint
        self._model = model
        self._timeout = timeout_seconds

    @property
    def name(self) -> str:
        return f"ollama:{self._model}"

    def generate(
        self, system_prompt: str, user_prompt: str, temperature: float = 0.7, max_tokens: int = 250
    ) -> str:
        payload = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }
        r = requests.post(self._endpoint, json=payload, timeout=self._timeout)
        r.raise_for_status()
        data = r.json()
        return str(data.get("message", {}).get("content", "")).strip()
