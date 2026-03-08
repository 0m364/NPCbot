import sqlite3
from pathlib import Path


class SQLiteMemoryStore:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(str(self.db_path))

    def _init_db(self) -> None:
        with self._connect() as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS dialogue_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    npc_id TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            con.commit()

    def write(self, npc_id: str, key: str, value: str) -> None:
        with self._connect() as con:
            con.execute(
                "INSERT INTO dialogue_memory (npc_id, key, value) VALUES (?, ?, ?)",
                (npc_id, key, value),
            )
            con.commit()

    def latest_for_npc(self, npc_id: str, limit: int = 6) -> list[tuple[str, str]]:
        with self._connect() as con:
            cur = con.execute(
                "SELECT key, value FROM dialogue_memory WHERE npc_id = ? ORDER BY id DESC LIMIT ?",
                (npc_id, limit),
            )
            rows = cur.fetchall()
        return [(str(k), str(v)) for k, v in rows]
