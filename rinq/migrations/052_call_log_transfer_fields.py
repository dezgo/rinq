"""
Migration 052: Add transfer tracking columns to call_log table.

Mirrors the transfer columns from queued_calls (migration 018) so that
non-queue calls (direct inbound, outbound) can also track transfer state.
This enables warm transfer and 3-way calling for all call types.
"""


def up(conn):
    """Add transfer tracking columns to call_log."""
    columns = [
        "transfer_status TEXT",        # null, pending, consulting, completed, failed, cancelled
        "transfer_type TEXT",          # blind, warm, three_way
        "transfer_target TEXT",        # phone number or extension
        "transfer_target_name TEXT",   # display name for UI
        "transfer_consult_call_sid TEXT",      # warm: consultation call SID
        "transfer_consult_conference TEXT",    # warm: consultation conference name
        "transferred_by TEXT",         # agent who initiated
        "transferred_at TEXT",         # when transfer was initiated
    ]
    for col in columns:
        conn.execute(f"ALTER TABLE call_log ADD COLUMN {col}")


def down(conn):
    """Remove transfer columns (SQLite doesn't support DROP COLUMN easily)."""
    pass
