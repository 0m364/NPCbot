import requests

from dialogue_engine.adapters.base import DialogueProvider


class OpenAICompatibleProvider(DialogueProvider):
    def __init__(self, endpoint: str, model: str, api_key: str = "", timeout_seconds: int = 90):
        self._endpoint = endpoint
        self._model = model
        self._timeout = timeout_seconds
        self._api_key = api_key

    @property
    def name(self) -> str:
        return f"openai-compatible:{self._model}"

    def generate(
        self, system_prompt: str, user_prompt: str, temperature: float = 0.7, max_tokens: int = 250
    ) -> str:
        headers = {"Content-Type": "application/json"}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"

        payload = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        r = requests.post(self._endpoint, json=payload, headers=headers, timeout=self._timeout)
        r.raise_for_status()
        data = r.json()
        choices = data.get("choices", [])
        if choices and isinstance(choices, list):
            return str(choices[0].get("message", {}).get("content", "")).strip()
        return ""
