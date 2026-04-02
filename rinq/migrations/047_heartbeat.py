"""Add last_heartbeat to staff_extensions for online presence tracking."""


def up(conn):
    conn.execute("""
        ALTER TABLE staff_extensions ADD COLUMN last_heartbeat TEXT
    """)


def down(conn):
    # SQLite doesn't support DROP COLUMN before 3.35
    pass
