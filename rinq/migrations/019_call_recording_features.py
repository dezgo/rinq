"""
Add call recording management features.

- Add record_calls_default to users table (per-user setting)
- Expand recording_log with google_message_id, call_type, staff_email
"""


def up(conn):
    """Add call recording columns."""

    # Add per-user recording default setting
    conn.execute("""
        ALTER TABLE users ADD COLUMN record_calls_default INTEGER DEFAULT 1
    """)

    # Add fields for Google Group storage and call metadata
    conn.execute("""
        ALTER TABLE recording_log ADD COLUMN google_message_id TEXT
    """)

    conn.execute("""
        ALTER TABLE recording_log ADD COLUMN call_type TEXT
    """)

    conn.execute("""
        ALTER TABLE recording_log ADD COLUMN staff_email TEXT
    """)

    # Create index for staff email lookups
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_recording_log_staff
        ON recording_log(staff_email)
    """)


def down(conn):
    """Remove call recording columns (SQLite limitation - columns can't be dropped easily)."""
    pass
