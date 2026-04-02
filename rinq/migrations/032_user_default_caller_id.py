"""Add default_caller_id to users table for SIP device outbound calls.

SIP devices need a configured caller ID since they can't pick from a
dropdown like the browser softphone. This column stores the E.164
phone number to use as caller ID for outbound calls.
"""


def up(conn):
    conn.execute("""
        ALTER TABLE users ADD COLUMN default_caller_id TEXT
    """)


def down(conn):
    # SQLite doesn't support DROP COLUMN easily
    pass
