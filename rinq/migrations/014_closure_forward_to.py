"""
Migration 014: Add forward_to to schedule_holidays

When a closure action is 'forward', this stores the phone number to forward to.
"""


def up(conn):
    conn.execute("""
        ALTER TABLE schedule_holidays
        ADD COLUMN forward_to TEXT
    """)
    conn.commit()


def down(conn):
    # SQLite doesn't support DROP COLUMN easily
    pass
