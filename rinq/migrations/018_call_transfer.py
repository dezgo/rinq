"""
Migration 018: Add transfer tracking columns to queued_calls table.

Adds support for blind and warm call transfers:
- transfer_status: pending, consulting, completed, failed, cancelled
- transfer_type: blind, warm
- transfer_target: phone number or user email being transferred to
- transfer_consult_call_sid: for warm transfers, the consultation call SID
- transferred_by: agent who initiated the transfer
- transferred_at: when transfer was initiated/completed
"""


def up(conn):
    """Add transfer tracking columns."""
    # Transfer status: null (no transfer), pending, consulting, completed, failed, cancelled
    conn.execute("""
        ALTER TABLE queued_calls ADD COLUMN transfer_status TEXT
    """)

    # Transfer type: blind or warm
    conn.execute("""
        ALTER TABLE queued_calls ADD COLUMN transfer_type TEXT
    """)

    # Target of transfer (phone number or extension)
    conn.execute("""
        ALTER TABLE queued_calls ADD COLUMN transfer_target TEXT
    """)

    # Target display name (for UI)
    conn.execute("""
        ALTER TABLE queued_calls ADD COLUMN transfer_target_name TEXT
    """)

    # For warm transfers: the SID of the consultation call to the target
    conn.execute("""
        ALTER TABLE queued_calls ADD COLUMN transfer_consult_call_sid TEXT
    """)

    # For warm transfers: the conference room for the consultation
    conn.execute("""
        ALTER TABLE queued_calls ADD COLUMN transfer_consult_conference TEXT
    """)

    # Who initiated the transfer
    conn.execute("""
        ALTER TABLE queued_calls ADD COLUMN transferred_by TEXT
    """)

    # When transfer was initiated
    conn.execute("""
        ALTER TABLE queued_calls ADD COLUMN transferred_at TEXT
    """)


def down(conn):
    """Remove transfer columns (SQLite doesn't support DROP COLUMN easily)."""
    pass
