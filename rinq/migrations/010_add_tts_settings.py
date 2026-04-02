"""Add TTS settings table for storing default provider/voice preferences."""


def up(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tts_settings (
            id INTEGER PRIMARY KEY,
            setting_key TEXT UNIQUE NOT NULL,
            setting_value TEXT,
            updated_at TEXT,
            updated_by TEXT
        )
    """)

    # Insert default settings
    conn.execute("""
        INSERT OR IGNORE INTO tts_settings (setting_key, setting_value)
        VALUES ('default_provider', 'elevenlabs')
    """)
    conn.execute("""
        INSERT OR IGNORE INTO tts_settings (setting_key, setting_value)
        VALUES ('default_voice', 'cjVigY5qzO86Huf0OWal')
    """)


def down(conn):
    conn.execute("DROP TABLE IF EXISTS tts_settings")
