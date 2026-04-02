"""Add child_call_sid to call_log for tracking outbound call legs.

When a Dial creates a child call, we store the child SID so the hold
feature can redirect it into a conference on demand.
"""


def up(conn):
    conn.execute("""
        ALTER TABLE call_log ADD COLUMN child_call_sid TEXT
    """)


def down(conn):
    pass  # SQLite doesn't support DROP COLUMN easily
