"""
Migration 017: Add conference_name column to queued_calls table.

This stores the conference room name when a call is answered,
enabling hold/unhold functionality via Twilio's Conference API.
"""


def up(conn):
    """Add conference_name column."""
    conn.execute("""
        ALTER TABLE queued_calls ADD COLUMN conference_name TEXT
    """)


def down(conn):
    """Remove conference_name column (SQLite doesn't support DROP COLUMN easily)."""
    pass
