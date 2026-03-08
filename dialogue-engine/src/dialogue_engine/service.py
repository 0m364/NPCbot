import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException

from dialogue_engine.adapters.factory import build_provider
from dialogue_engine.config import load_config
from dialogue_engine.memory.sqlite_store import SQLiteMemoryStore
from dialogue_engine.prompting import build_system_prompt, build_user_prompt
from dialogue_engine.safety import apply_safety
from dialogue_engine.schemas import (
    DialogueGenerateRequest,
    DialogueGenerateResponse,
    HealthResponse,
    MemoryWriteRequest,
)


def create_app(config_path: str | Path = "config.yaml") -> FastAPI:
    cfg = load_config(config_path)
    provider = build_provider(cfg)
    memory = SQLiteMemoryStore(db_path=str(cfg.get("memory", {}).get("sqlite_path", "data/dialogue_memory.db")))
    safety_cfg = cfg.get("safety", {})

    app = FastAPI(title="Dialogue Engine", version="1.0.0")

    @app.get("/v1/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(ok=True, service="dialogue-engine")

    @app.post("/v1/memory/write")
    def memory_write(req: MemoryWriteRequest) -> dict[str, str]:
        memory.write(req.npc_id, req.key, req.value)
        return {"status": "ok"}

    @app.post("/v1/dialogue/generate", response_model=DialogueGenerateResponse)
    def dialogue_generate(req: DialogueGenerateRequest) -> DialogueGenerateResponse:
        trace_id = str(uuid.uuid4())
        mem = memory.latest_for_npc(req.npc_id)

        system_prompt = build_system_prompt(req.constraints)
        user_prompt = build_user_prompt(
            npc_id=req.npc_id,
            npc_persona=req.npc_persona,
            player_input=req.player_input,
            world_state=req.world_state,
            quest_state=req.quest_state,
            tone=req.tone,
            memory_items=mem,
        )

        try:
            raw = provider.generate(
                system_prompt, 
                user_prompt, 
                temperature=req.temperature, 
                max_tokens=req.max_tokens
            )
            safe = apply_safety(raw, safety_cfg)
            return DialogueGenerateResponse(dialogue=safe, model=provider.name, trace_id=trace_id)
        except Exception as exc:
            fallback = apply_safety("", safety_cfg)
            raise HTTPException(
                status_code=502,
                detail={
                    "trace_id": trace_id,
                    "error": str(exc),
                    "fallback": fallback,
                },
            )

    return app
