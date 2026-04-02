"""
Initial schema for Phoebe.

Creates tables for:
- phone_numbers: Twilio phone numbers and forwarding rules
- users: SIP credentials for staff
- recording_log: Call recording history
- activity_log: Audit trail
"""


def up(conn):
    """Create initial tables."""

    # Phone numbers - Twilio numbers we manage
    conn.execute("""
        CREATE TABLE IF NOT EXISTS phone_numbers (
            sid TEXT PRIMARY KEY,
            phone_number TEXT NOT NULL UNIQUE,
            friendly_name TEXT,
            forward_to TEXT,
            is_active INTEGER DEFAULT 1,
            synced_at TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT,
            updated_by TEXT
        )
    """)

    # Users - SIP credentials linked to staff
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            sid TEXT PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            friendly_name TEXT,
            staff_email TEXT,
            extension TEXT,
            is_active INTEGER DEFAULT 1,
            synced_at TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT,
            updated_by TEXT
        )
    """)

    # Recording log - tracks call recordings we've processed
    conn.execute("""
        CREATE TABLE IF NOT EXISTS recording_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recording_sid TEXT NOT NULL UNIQUE,
            call_sid TEXT,
            from_number TEXT,
            to_number TEXT,
            duration_seconds INTEGER,
            recording_url TEXT,
            emailed_to TEXT,
            emailed_at TEXT,
            deleted_from_twilio INTEGER DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Activity log - audit trail
    conn.execute("""
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            target TEXT,
            details TEXT,
            performed_by TEXT,
            performed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Indexes
    conn.execute("CREATE INDEX IF NOT EXISTS idx_phone_numbers_number ON phone_numbers(phone_number)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(staff_email)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_recording_log_created ON recording_log(created_at)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_activity_log_performed ON activity_log(performed_at)")


def down(conn):
    """Drop tables."""
    conn.execute("DROP TABLE IF EXISTS activity_log")
    conn.execute("DROP TABLE IF EXISTS recording_log")
    conn.execute("DROP TABLE IF EXISTS users")
    conn.execute("DROP TABLE IF EXISTS phone_numbers")
