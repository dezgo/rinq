"""Add queue_managers table — separate from queue_members, for pause/operational control."""


def up(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS queue_managers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            queue_id INTEGER NOT NULL REFERENCES queues(id),
            user_email TEXT NOT NULL,
            created_at TEXT NOT NULL,
            created_by TEXT NOT NULL,
            UNIQUE (queue_id, user_email)
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_queue_managers_queue ON queue_managers(queue_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_queue_managers_email ON queue_managers(user_email)")


def down(conn):
    conn.execute("DROP TABLE IF EXISTS queue_managers")
