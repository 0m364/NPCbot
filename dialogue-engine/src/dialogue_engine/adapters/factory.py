from typing import Any

from dialogue_engine.adapters.base import DialogueProvider
from dialogue_engine.adapters.ollama_provider import OllamaProvider
from dialogue_engine.adapters.openai_compatible_provider import OpenAICompatibleProvider
from dialogue_engine.adapters.template_provider import TemplateProvider
from dialogue_engine.adapters.builtin_provider import BuiltInProvider


def build_provider(cfg: dict[str, Any]) -> DialogueProvider:
    model_cfg = cfg.get("model", {})
    provider = str(model_cfg.get("provider", "template")).strip().lower()

    if provider == "ollama":
        return OllamaProvider(
            endpoint=str(model_cfg.get("endpoint", "http://127.0.0.1:11434/api/chat")),
            model=str(model_cfg.get("name", "tinyllama:1.1b")),
            timeout_seconds=int(model_cfg.get("timeout_seconds", 90)),
        )

    if provider == "openai_compatible":
        return OpenAICompatibleProvider(
            endpoint=str(model_cfg.get("endpoint", "http://127.0.0.1:1234/v1/chat/completions")),
            model=str(model_cfg.get("name", "local-model")),
            api_key=str(model_cfg.get("api_key", "")),
            timeout_seconds=int(model_cfg.get("timeout_seconds", 90)),
        )

    if provider == "built_in":
        return BuiltInProvider(
            repo_id=str(model_cfg.get("repo_id", "bartowski/SmolLM2-1.7B-Instruct-GGUF")),
            filename=str(model_cfg.get("filename", "SmolLM2-1.7B-Instruct-Q4_K_M.gguf")),
            n_ctx=int(model_cfg.get("n_ctx", 2048)),
        )

    return TemplateProvider()
