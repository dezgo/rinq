"""Add ring_attempts table for tracking outbound ring calls across gunicorn workers.

Replaces in-memory _conference_ring_calls, _agent_calls_by_customer, and
_customer_by_agent_call dicts which broke across separate worker processes.
"""


def up(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ring_attempts (
            id INTEGER PRIMARY KEY,
            group_key TEXT NOT NULL,
            call_sid TEXT NOT NULL,
            group_type TEXT NOT NULL,
            metadata TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            UNIQUE(group_key, call_sid)
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_ring_attempts_group ON ring_attempts(group_key)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_ring_attempts_sid ON ring_attempts(call_sid)")


def down(conn):
    conn.execute("DROP TABLE IF EXISTS ring_attempts")
