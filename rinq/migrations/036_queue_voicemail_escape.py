"""Add allow_voicemail_escape column to queues table.

When enabled, callers waiting in queue can press 1 to leave a voicemail
instead of continuing to wait. The option is announced when they first
enter the queue.
"""


def up(conn):
    conn.execute("""
        ALTER TABLE queues ADD COLUMN allow_voicemail_escape INTEGER DEFAULT 0
    """)


def down(conn):
    # SQLite doesn't support DROP COLUMN easily
    pass
