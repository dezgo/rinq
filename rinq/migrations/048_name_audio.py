"""
Add name audio columns to staff_extensions for TTS-generated name clips.

name_audio_path: relative URL path to the audio file (e.g. /audio/name_ext_1042.mp3)
name_audio_text: the text that was spoken, used to detect when regeneration is needed
"""


def up(conn):
    conn.execute("ALTER TABLE staff_extensions ADD COLUMN name_audio_path TEXT")
    conn.execute("ALTER TABLE staff_extensions ADD COLUMN name_audio_text TEXT")


def down(conn):
    # SQLite doesn't support DROP COLUMN before 3.35.0
    pass
