"""
Add browser ring fields to phone_numbers.

Allows incoming calls to ring browser softphones in addition to (or instead of)
forwarding to a phone number.
"""


def up(conn):
    # Add ring_browser flag - if true, ring connected browser clients
    conn.execute("""
        ALTER TABLE phone_numbers
        ADD COLUMN ring_browser INTEGER DEFAULT 0
    """)

    # Add browser_identity - specific client identity to ring (optional)
    # If null and ring_browser=1, rings all connected clients
    conn.execute("""
        ALTER TABLE phone_numbers
        ADD COLUMN browser_identity TEXT
    """)


def down(conn):
    # SQLite doesn't support DROP COLUMN easily
    pass
