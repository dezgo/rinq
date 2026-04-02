"""
Add voicemail transcription support.

Stores transcription text and Zendesk ticket ID so we can update
the ticket when transcription arrives (async from Twilio).
"""


def up(conn):
    """Add transcription columns to recording_log."""
    # Transcription text from Twilio
    conn.execute("""
        ALTER TABLE recording_log ADD COLUMN transcription TEXT
    """)
    # Zendesk ticket ID for updating when transcription arrives
    conn.execute("""
        ALTER TABLE recording_log ADD COLUMN zendesk_ticket_id INTEGER
    """)


def down(conn):
    """Remove columns (SQLite limitation - can't easily drop columns)."""
    pass
