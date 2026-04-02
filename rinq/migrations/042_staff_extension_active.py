"""Add is_active flag to staff_extensions.

Tracks whether a staff member has officially migrated to Tina.
Logging in creates an extension, but is_active=0 until an admin
activates them. Only active users get their phone info synced to Peter.
"""


def up(conn):
    conn.execute("""
        ALTER TABLE staff_extensions ADD COLUMN is_active INTEGER DEFAULT 0
    """)


def down(conn):
    # SQLite doesn't support DROP COLUMN easily
    pass
