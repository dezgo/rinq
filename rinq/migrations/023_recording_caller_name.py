"""
Add caller_name to recording_log for searchable customer names.

For inbound calls, this captures the customer name from Clara lookup.
For outbound calls, this could capture the contact name if available.
"""


def up(conn):
    """Add caller_name column to recording_log."""
    conn.execute("""
        ALTER TABLE recording_log ADD COLUMN caller_name TEXT
    """)


def down(conn):
    """Remove caller_name column (SQLite doesn't support DROP COLUMN easily)."""
    pass
