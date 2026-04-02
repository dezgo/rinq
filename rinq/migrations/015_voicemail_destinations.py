"""
Migration 015: Add voicemail_destinations table

Stores email addresses that can receive voicemail recordings.
These are typically store-specific Zendesk channels or support emails.
"""


def up(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS voicemail_destinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            description TEXT,
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL,
            created_by TEXT,
            updated_at TEXT NOT NULL,
            updated_by TEXT
        )
    """)
    conn.commit()


def down(conn):
    conn.execute("DROP TABLE IF EXISTS voicemail_destinations")
    conn.commit()
