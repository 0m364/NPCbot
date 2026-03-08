from typing import Any


def apply_safety(text: str, cfg: dict[str, Any]) -> str:
    if not text.strip():
        intro = str(cfg.get("fallback_intro", "I need a moment to think."))
        opt = str(cfg.get("fallback_option", "Tell me more."))
        return (
            f"Intro: {intro}\n"
            f"Option A: {opt}\n"
            "NPC A: I can help if you give me a little more context.\n"
            f"Option B: {opt}\n"
            "NPC B: I can help if you give me a little more context.\n"
            f"Option C: {opt}\n"
            "NPC C: I can help if you give me a little more context.\n"
            "Farewell: Let's continue when you are ready."
        )

    max_chars = int(cfg.get("max_output_chars", 2400))
    return text[:max_chars]
