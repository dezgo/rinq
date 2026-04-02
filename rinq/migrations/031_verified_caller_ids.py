"""Add verified_caller_ids table for external numbers used as caller ID.

These are numbers verified in Twilio that aren't owned/ported yet,
but can be used as outbound caller ID. They won't be affected by
phone number syncs.
"""


def up(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS verified_caller_ids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT NOT NULL UNIQUE,
            friendly_name TEXT,
            section TEXT,
            is_active INTEGER DEFAULT 1,
            notes TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_by TEXT
        )
    """)

    # Create index for section lookups
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_verified_caller_ids_section
        ON verified_caller_ids(section)
    """)

    # Seed the Bay number (verified in Twilio but not owned/ported yet)
    conn.execute("""
        INSERT OR IGNORE INTO verified_caller_ids
        (phone_number, friendly_name, section, notes, is_active, created_at, created_by, updated_at, updated_by)
        VALUES ('+61244094006', 'Bay', 'Batemans Bay', 'Verified in Twilio - awaiting port', 1,
                CURRENT_TIMESTAMP, 'system:migration_031', CURRENT_TIMESTAMP, 'system:migration_031')
    """)


def down(conn):
    conn.execute("DROP TABLE IF EXISTS verified_caller_ids")
