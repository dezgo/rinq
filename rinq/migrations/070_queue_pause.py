"""Add scheduled pause window to queues."""


def up(conn):
    conn.execute("ALTER TABLE queues ADD COLUMN paused_from TEXT")
    conn.execute("ALTER TABLE queues ADD COLUMN paused_until TEXT")


def down(conn):
    # SQLite doesn't support DROP COLUMN in older versions; leave columns in place
    pass
