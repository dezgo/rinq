"""
Add Google Drive file ID to recording_log for cloud storage.

Call recordings are now stored in three tiers:
1. Local (3 weeks) - for instant playback
2. Google Drive (12 months) - warm storage with proper API access
3. Google Groups (forever) - cold archive via email
"""


def up(conn):
    """Add drive_file_id column for Google Drive storage."""
    conn.execute("""
        ALTER TABLE recording_log ADD COLUMN drive_file_id TEXT
    """)


def down(conn):
    """Remove drive_file_id column (SQLite doesn't support DROP COLUMN easily)."""
    pass
