"""
Add password column to users table for SIP credential storage.

Allows admins to view SIP passwords after initial creation,
rather than having to regenerate them each time.
"""


def up(conn):
    """Add password column to users table."""
    conn.execute("""
        ALTER TABLE users ADD COLUMN password TEXT
    """)


def down(conn):
    """Remove password column (SQLite doesn't support DROP COLUMN easily)."""
    pass
