"""Add do-not-disturb flag to staff_extensions."""


def up(conn):
    conn.execute("""
        ALTER TABLE staff_extensions ADD COLUMN dnd_enabled INTEGER NOT NULL DEFAULT 0
    """)


def down(conn):
    # SQLite doesn't support DROP COLUMN before 3.35
    pass
