"""Initial master database schema.

Stores tenants, users, and the phone number -> tenant mapping.
"""


def up(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tenants (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            twilio_account_sid TEXT,
            twilio_auth_token TEXT,
            twilio_api_key TEXT,
            twilio_api_secret TEXT,
            twilio_twiml_app_sid TEXT,
            twilio_default_caller_id TEXT,
            twilio_sip_credential_list_sid TEXT,
            webhook_base_url TEXT,
            integration_provider TEXT DEFAULT 'none',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            name TEXT,
            picture TEXT,
            google_sub TEXT,
            is_superadmin INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tenant_users (
            tenant_id TEXT NOT NULL REFERENCES tenants(id),
            user_id INTEGER NOT NULL REFERENCES users(id),
            role TEXT DEFAULT 'admin',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (tenant_id, user_id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tenant_phone_numbers (
            phone_number TEXT PRIMARY KEY,
            tenant_id TEXT NOT NULL REFERENCES tenants(id)
        )
    """)


def down(conn):
    conn.execute("DROP TABLE IF EXISTS tenant_phone_numbers")
    conn.execute("DROP TABLE IF EXISTS tenant_users")
    conn.execute("DROP TABLE IF EXISTS users")
    conn.execute("DROP TABLE IF EXISTS tenants")
