"""Add general bot_settings table for configuration values."""


def up(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS bot_settings (
            id INTEGER PRIMARY KEY,
            setting_key TEXT UNIQUE NOT NULL,
            setting_value TEXT,
            description TEXT,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_by TEXT
        )
    """)

    # Add Drive folder setting with empty default (must be configured)
    conn.execute("""
        INSERT OR IGNORE INTO bot_settings (setting_key, setting_value, description)
        VALUES (
            'drive_recordings_folder_id',
            NULL,
            'Google Drive folder ID for recording storage (12-month retention)'
        )
    """)


def down(conn):
    conn.execute("DROP TABLE IF EXISTS bot_settings")
