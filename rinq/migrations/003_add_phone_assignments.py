"""Add phone_assignments table for linking staff to phone numbers."""


def up(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS phone_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number_sid TEXT NOT NULL,
            staff_email TEXT NOT NULL,
            can_receive INTEGER DEFAULT 1,
            can_make INTEGER DEFAULT 1,
            created_at TEXT NOT NULL,
            created_by TEXT,
            updated_at TEXT NOT NULL,
            updated_by TEXT,
            FOREIGN KEY (phone_number_sid) REFERENCES phone_numbers(sid),
            UNIQUE(phone_number_sid, staff_email)
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_phone_assignments_email
        ON phone_assignments(staff_email)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_phone_assignments_sid
        ON phone_assignments(phone_number_sid)
    """)


def down(conn):
    conn.execute("DROP INDEX IF EXISTS idx_phone_assignments_email")
    conn.execute("DROP INDEX IF EXISTS idx_phone_assignments_sid")
    conn.execute("DROP TABLE IF EXISTS phone_assignments")
