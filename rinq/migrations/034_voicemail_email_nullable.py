"""
Migration 034: Make voicemail_destinations.email nullable

Migration 025 added routing_type to support Zendesk ticket routing (which
doesn't need an email), but didn't actually remove the NOT NULL constraint
on the email column. This migration fixes that by recreating the table
with email as nullable.
"""


def up(conn):
    # SQLite doesn't support ALTER COLUMN, so we need to recreate the table

    # Step 1: Create new table with correct schema (email nullable, no UNIQUE)
    conn.execute("""
        CREATE TABLE voicemail_destinations_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            description TEXT,
            is_active INTEGER NOT NULL DEFAULT 1,
            zendesk_group_id INTEGER,
            routing_type TEXT NOT NULL DEFAULT 'email',
            created_at TEXT NOT NULL,
            created_by TEXT,
            updated_at TEXT NOT NULL,
            updated_by TEXT
        )
    """)

    # Step 2: Copy data from old table
    conn.execute("""
        INSERT INTO voicemail_destinations_new
            (id, name, email, description, is_active, zendesk_group_id,
             routing_type, created_at, created_by, updated_at, updated_by)
        SELECT id, name, email, description, is_active, zendesk_group_id,
               routing_type, created_at, created_by, updated_at, updated_by
        FROM voicemail_destinations
    """)

    # Step 3: Drop old table
    conn.execute("DROP TABLE voicemail_destinations")

    # Step 4: Rename new table
    conn.execute("ALTER TABLE voicemail_destinations_new RENAME TO voicemail_destinations")

    conn.commit()


def down(conn):
    # Can't easily revert to NOT NULL without data loss
    pass
