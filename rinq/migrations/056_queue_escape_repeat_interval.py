"""Add escape_repeat_interval to queues.

Controls how often the voicemail/callback escape announcement repeats
after the initial announcement. Default 120 seconds (2 minutes).
Set to 0 to only announce once.
"""


def up(conn):
    conn.execute("""
        ALTER TABLE queues
        ADD COLUMN escape_repeat_interval INTEGER NOT NULL DEFAULT 120
    """)


def down(conn):
    pass  # SQLite doesn't support DROP COLUMN easily
