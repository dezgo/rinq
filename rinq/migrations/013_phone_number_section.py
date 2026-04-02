"""
Migration 013: Add section to phone_numbers

Associates phone numbers with business sections (e.g., "CANBERRA", "SYDNEY")
so caller ID can be auto-selected based on the user's section from Peter.
"""


def up(conn):
    # Add section column to phone numbers
    conn.execute("""
        ALTER TABLE phone_numbers ADD COLUMN section TEXT
    """)

    # Index for section lookups
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_phone_numbers_section
        ON phone_numbers(section)
    """)


def down(conn):
    # SQLite doesn't support DROP COLUMN easily
    pass
