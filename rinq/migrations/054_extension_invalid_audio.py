"""Add extension_invalid_audio_id to call_flows.

Allows custom audio for the "invalid extension" message instead of
hardcoded TTS.
"""


def up(conn):
    conn.execute("""
        ALTER TABLE call_flows
        ADD COLUMN extension_invalid_audio_id INTEGER REFERENCES audio_files(id)
    """)


def down(conn):
    # SQLite doesn't support DROP COLUMN before 3.35.0
    # Just leave the column in place
    pass
