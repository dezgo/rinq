"""Add duration_seconds to audio_files.

Stores the audio file duration so it can be displayed in the UI,
particularly for hold music selection where track length affects
how often queue announcements can play.
"""


def up(conn):
    # Check if column already exists before adding
    columns = [row[1] for row in conn.execute("PRAGMA table_info(audio_files)").fetchall()]
    if 'duration_seconds' not in columns:
        conn.execute("""
            ALTER TABLE audio_files
            ADD COLUMN duration_seconds INTEGER
        """)


def down(conn):
    pass  # SQLite can't drop columns
