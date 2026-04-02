"""
Add audio_id to schedule_holidays for holiday-specific messages.

Allows different audio messages for different holidays:
- Regular closed: "We're currently closed"
- Public holiday: "We're closed for the public holiday"
- Christmas break: "We're closed for the Christmas/New Year break"
- One-off closure: "We're temporarily closed today"
"""


def up(conn):
    # Add audio_id column to schedule_holidays
    conn.execute("""
        ALTER TABLE schedule_holidays
        ADD COLUMN audio_id INTEGER REFERENCES audio_files(id)
    """)
    conn.commit()


def down(conn):
    # SQLite doesn't easily support DROP COLUMN, so we'd need to recreate the table
    # For now, leave the column in place
    pass
