"""Move default_caller_id from users (SIP credentials) to staff_extensions.

Caller ID preference belongs on the staff extension, not the SIP credential,
since browser softphone users don't necessarily have SIP credentials.
"""


def up(conn):
    conn.execute("""
        ALTER TABLE staff_extensions ADD COLUMN default_caller_id TEXT
    """)

    # Copy existing caller ID preferences from users table
    conn.execute("""
        UPDATE staff_extensions
        SET default_caller_id = (
            SELECT u.default_caller_id
            FROM users u
            WHERE u.staff_email = staff_extensions.email
            AND u.default_caller_id IS NOT NULL
        )
        WHERE EXISTS (
            SELECT 1 FROM users u
            WHERE u.staff_email = staff_extensions.email
            AND u.default_caller_id IS NOT NULL
        )
    """)


def down(conn):
    # SQLite doesn't support DROP COLUMN easily; leave the column
    pass
