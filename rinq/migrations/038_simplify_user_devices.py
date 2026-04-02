"""
Migration 038: Simplify user devices

Replaces the user_devices table with two boolean columns on the users table:
- ring_browser: whether to ring the browser softphone
- ring_sip: whether to ring SIP devices (desk phone, Zoiper, etc.)

This simplification is possible because:
1. SIP and mobile_sip devices both resolve to the same SIP URI (deduplicated)
2. Mobile/external forwarding has caller ID issues - we use SIP apps instead
3. The device list was mostly cosmetic - all SIP devices ring regardless

The new model: configure your SIP credentials on any devices you want,
toggle ring_sip on/off to control whether they ring.
"""


def up(conn):
    # Add ring_browser and ring_sip columns to users table
    conn.execute("ALTER TABLE users ADD COLUMN ring_browser INTEGER DEFAULT 1")
    conn.execute("ALTER TABLE users ADD COLUMN ring_sip INTEGER DEFAULT 1")

    # Migrate existing device states
    # If user had an INACTIVE browser device, set ring_browser = 0
    conn.execute("""
        UPDATE users SET ring_browser = 0
        WHERE staff_email IN (
            SELECT user_email FROM user_devices
            WHERE device_type = 'browser' AND is_active = 0
        )
    """)

    # If user had an INACTIVE sip/mobile_sip device (and no active ones), set ring_sip = 0
    # Only disable if ALL sip-type devices are inactive
    conn.execute("""
        UPDATE users SET ring_sip = 0
        WHERE staff_email IN (
            SELECT DISTINCT user_email FROM user_devices
            WHERE device_type IN ('sip', 'mobile_sip')
            AND user_email NOT IN (
                SELECT user_email FROM user_devices
                WHERE device_type IN ('sip', 'mobile_sip') AND is_active = 1
            )
        )
    """)

    # Drop user_devices table (no longer needed)
    conn.execute("DROP TABLE IF EXISTS user_devices")


def down(conn):
    # Recreate user_devices table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user_devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            device_type TEXT NOT NULL,
            device_name TEXT,
            device_config TEXT,
            priority INTEGER DEFAULT 0,
            ring_delay INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_by TEXT
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_user_devices_email ON user_devices(user_email)")

    # Recreate device entries from users table settings
    conn.execute("""
        INSERT INTO user_devices (user_email, device_type, device_name, is_active, created_at, created_by)
        SELECT staff_email, 'browser', 'Browser Softphone', ring_browser, CURRENT_TIMESTAMP, 'system:migration_rollback'
        FROM users WHERE staff_email IS NOT NULL
    """)

    conn.execute("""
        INSERT INTO user_devices (user_email, device_type, device_name, is_active, created_at, created_by)
        SELECT staff_email, 'sip', 'Desk Phone', ring_sip, CURRENT_TIMESTAMP, 'system:migration_rollback'
        FROM users WHERE staff_email IS NOT NULL
    """)

    # Remove columns from users table
    # SQLite doesn't support DROP COLUMN easily, so we leave them
