import uvicorn

from dialogue_engine.config import load_config
from dialogue_engine.service import create_app


def main() -> None:
    cfg = load_config("config.yaml")
    server = cfg.get("server", {})
    host = str(server.get("host", "127.0.0.1"))
    port = int(server.get("port", 8787))

    app = create_app("config.yaml")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
