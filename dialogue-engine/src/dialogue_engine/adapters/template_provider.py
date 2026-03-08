from dialogue_engine.adapters.base import DialogueProvider


class TemplateProvider(DialogueProvider):
    @property
    def name(self) -> str:
        return "template-local"

    def generate(
        self, system_prompt: str, user_prompt: str, temperature: float = 0.7, max_tokens: int = 250
    ) -> str:
        return (
            "Intro: We can talk, but keep your voice down.\n"
            "Option A: What happened here?\n"
            "NPC A: Machines stopped obeying, and people panicked.\n"
            "Option B: Is this area safe?\n"
            "NPC B: Safer than the ruins, not safe enough to relax.\n"
            "Option C: What do you need from me?\n"
            "NPC C: Bring power cells and I'll open the old gate path.\n"
            "Farewell: Stay alert, and watch the rooftops."
        )
