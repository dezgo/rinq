"""
Add local file storage for call recordings.

Recordings are saved locally as a cache for direct playback in Tina.
Google Group is the permanent archive (source of truth).
Local files are fetched on-demand if not present and purged after X days.
"""


def up(conn):
    """Add local storage columns to recording_log."""
    # Path to locally cached recording file
    conn.execute("""
        ALTER TABLE recording_log ADD COLUMN local_file_path TEXT
    """)
    # Track when recording was last accessed for cache purge decisions
    conn.execute("""
        ALTER TABLE recording_log ADD COLUMN last_accessed_at TEXT
    """)


def down(conn):
    """Remove columns (SQLite limitation - can't easily drop columns)."""
    pass
