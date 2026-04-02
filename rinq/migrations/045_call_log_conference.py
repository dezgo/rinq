"""Add conference_name column to call_log for hold support on all call types."""


def up(conn):
    conn.execute("""
        ALTER TABLE call_log ADD COLUMN conference_name TEXT
    """)


def down(conn):
    pass
