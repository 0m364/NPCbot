from typing import Iterable


def build_system_prompt(constraints: str) -> str:
    return (
        "You are an expert game dialogue writer for a post-apocalyptic RPG. "
        "Your task is to write strictly character dialogue without any narrative prose, actions, or stage directions. "
        "Write exactly in the requested Output Format and do not add any conversational filler. "
        f"Constraints: {constraints}"
    )


def build_user_prompt(
    npc_id: str,
    npc_persona: str,
    player_input: str,
    world_state: str,
    quest_state: str,
    tone: str,
    memory_items: Iterable[tuple[str, str]],
) -> str:
    memory_lines = "\n".join([f"- {k}: {v}" for k, v in memory_items]) or "- none"
    return (
        f"NPC: {npc_id}\n"
        f"Persona: {npc_persona}\n"
        f"Tone: {tone}\n"
        f"World State: {world_state or 'none'}\n"
        f"Quest State: {quest_state or 'none'}\n"
        f"Recent Memory:\n{memory_lines}\n\n"
        f"Player says: {player_input}\n\n"
        "Output format (strict):\n"
        "Intro: [NPC's opening line of dialogue.]\n"
        "Option A: [A short player dialogue option.]\n"
        "NPC A: [NPC's response to Option A.]\n"
        "Option B: [A short player dialogue option.]\n"
        "NPC B: [NPC's response to Option B.]\n"
        "Option C: [A short player dialogue option.]\n"
        "NPC C: [NPC's response to Option C.]\n"
        "Farewell: [NPC's closing line of dialogue.]\n"
        "Provide no other text."
    )
