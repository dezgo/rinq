"""Add configurable audio for queue announcements.

Replaces hardcoded <Say> messages with optional recorded audio:
- welcome_audio_id: played when caller first enters queue (e.g. "press 1 for voicemail, press 2 for callback")
- callback_reminder_audio_id: played after callback threshold (e.g. "press 2 to request a callback")
"""


def up(conn):
    conn.execute("""
        ALTER TABLE queues ADD COLUMN welcome_audio_id INTEGER REFERENCES audio_files(id)
    """)
    conn.execute("""
        ALTER TABLE queues ADD COLUMN callback_reminder_audio_id INTEGER REFERENCES audio_files(id)
    """)


def down(conn):
    # SQLite doesn't support DROP COLUMN easily
    pass
