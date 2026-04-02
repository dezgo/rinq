"""Add escape_announcement_delay to queues.

Configurable delay (in seconds) before playing the "press 1 for voicemail,
press 2 for callback" announcement. Gives staff time to answer before
callers hear IVR options. Default 60 seconds.
"""


def up(conn):
    conn.execute("""
        ALTER TABLE queues
        ADD COLUMN escape_announcement_delay INTEGER NOT NULL DEFAULT 60
    """)


def down(conn):
    # SQLite doesn't support DROP COLUMN before 3.35.0
    pass
