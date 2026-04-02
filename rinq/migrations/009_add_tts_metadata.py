"""
Add TTS metadata fields to audio_files table.

Stores the original text and voice settings for AI-generated audio files
so they can be regenerated or updated later.
"""


def up(conn):
    """Add TTS metadata columns to audio_files."""
    # TTS text - the original text used to generate the audio
    conn.execute("""
        ALTER TABLE audio_files
        ADD COLUMN tts_text TEXT
    """)

    # TTS provider - 'elevenlabs', 'google', etc
    conn.execute("""
        ALTER TABLE audio_files
        ADD COLUMN tts_provider TEXT
    """)

    # TTS voice - voice ID or name
    conn.execute("""
        ALTER TABLE audio_files
        ADD COLUMN tts_voice TEXT
    """)

    # TTS settings - JSON blob with stability, speed, etc
    conn.execute("""
        ALTER TABLE audio_files
        ADD COLUMN tts_settings TEXT
    """)


def down(conn):
    """Remove TTS metadata columns (not easily reversible in SQLite)."""
    # SQLite doesn't support DROP COLUMN easily
    pass
