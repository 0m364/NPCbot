from pydantic import BaseModel, Field


class DialogueGenerateRequest(BaseModel):
    npc_id: str = Field(min_length=1, max_length=80)
    player_input: str = Field(min_length=1, max_length=1200)
    npc_persona: str = Field(default="Practical, grounded, concise")
    world_state: str = Field(default="")
    quest_state: str = Field(default="")
    tone: str = Field(default="grounded, cinematic")
    constraints: str = Field(default="Teen-safe content. Keep it concise.")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=250, ge=10, le=4000)


class DialogueGenerateResponse(BaseModel):
    dialogue: str
    model: str
    trace_id: str


class MemoryWriteRequest(BaseModel):
    npc_id: str = Field(min_length=1, max_length=80)
    key: str = Field(min_length=1, max_length=120)
    value: str = Field(min_length=1, max_length=4000)


class HealthResponse(BaseModel):
    ok: bool
    service: str
