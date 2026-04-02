"""
Migration 012: Staff Extensions and Self-Service Queues

Adds:
- staff_extensions table for auto-generated extensions and forwarding settings
- allow_self_service column to queues table
"""


def up(conn):
    # Staff extensions - every staff member gets an extension
    conn.execute("""
        CREATE TABLE IF NOT EXISTS staff_extensions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,           -- Staff email (links to Peter)
            extension TEXT NOT NULL UNIQUE,       -- 3-digit extension (100-999)

            -- Visibility
            show_in_pam INTEGER DEFAULT 0,        -- Show extension in PAM directory

            -- Call forwarding
            forward_to TEXT,                      -- AU mobile number (+614XXXXXXXX format)
            forward_mode TEXT DEFAULT 'always',   -- 'always' or 'no_answer'

            -- Audit
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_by TEXT
        )
    """)

    # Index for extension lookups
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_staff_extensions_extension
        ON staff_extensions(extension)
    """)

    # Add self-service flag to queues
    conn.execute("""
        ALTER TABLE queues ADD COLUMN allow_self_service INTEGER DEFAULT 0
    """)


def down(conn):
    conn.execute("DROP TABLE IF EXISTS staff_extensions")
    # Note: SQLite doesn't support DROP COLUMN easily, so allow_self_service stays
