import logging
from pathlib import Path
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

from dialogue_engine.adapters.base import DialogueProvider


class BuiltInProvider(DialogueProvider):
    def __init__(self, repo_id: str, filename: str, n_ctx: int = 2048):
        self._repo_id = repo_id
        self._filename = filename
        self._n_ctx = n_ctx
        
        logging.info(f"Loading built-in model: {repo_id} / {filename}")
        
        # Download model if not present locally (huggingface_hub handles caching)
        try:
            model_path = hf_hub_download(repo_id=repo_id, filename=filename)
            logging.info(f"Model ready at: {model_path}")
        except Exception as e:
            logging.error(f"Failed to download model {repo_id}/{filename}: {e}")
            raise RuntimeError(f"Model download failed: {e}") from e

        # Initialize Llama instance
        self._llm = Llama(
            model_path=model_path,
            n_ctx=self._n_ctx,
            verbose=False,  # Set to True for debugging if needed
        )

    @property
    def name(self) -> str:
        return f"built_in:{self._repo_id}:{self._filename}"

    def generate(
        self, system_prompt: str, user_prompt: str, temperature: float = 0.7, max_tokens: int = 250
    ) -> str:
        # Use ChatML format or let llama_cpp handle the default chat format if available
        # Llama.create_chat_completion automatically applies the chat template built into the GGUF.
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        
        try:
            response = self._llm.create_chat_completion(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=False
            )
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            return str(content).strip()
        except Exception as e:
            logging.error(f"Inference error in BuiltInProvider: {e}")
            raise RuntimeError(f"BuiltIn inference failed: {e}") from e
