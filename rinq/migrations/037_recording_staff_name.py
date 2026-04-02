"""Add staff_name column to recording_log and fix staff_email format.

The staff_email column sometimes contains raw Twilio client identities like
'client:chris_savage_at_watsonblinds_com_au' instead of proper email addresses.
This migration:
1. Adds a staff_name column for friendly display
2. Fixes existing staff_email values that are in the wrong format
"""


def up(conn):
    # Add staff_name column
    conn.execute("""
        ALTER TABLE recording_log ADD COLUMN staff_name TEXT
    """)

    # Fix existing staff_email values in client:user_at_domain format
    # Convert: client:chris_savage_at_watsonblinds_com_au -> chris_savage@watsonblinds.com.au
    rows = conn.execute("""
        SELECT id, staff_email FROM recording_log
        WHERE staff_email LIKE 'client:%'
    """).fetchall()

    for row in rows:
        old_email = row['staff_email']
        # Remove 'client:' prefix
        identity = old_email[7:]
        # Convert back: user_at_domain_com -> user@domain.com
        new_email = identity.replace('_at_', '@').replace('_', '.')
        # Extract friendly name
        staff_name = new_email.split('@')[0].replace('_', ' ').title() if '@' in new_email else None

        conn.execute("""
            UPDATE recording_log
            SET staff_email = ?, staff_name = ?
            WHERE id = ?
        """, (new_email, staff_name, row['id']))

    # Also populate staff_name for existing records that have proper emails
    conn.execute("""
        UPDATE recording_log
        SET staff_name = REPLACE(
            REPLACE(
                SUBSTR(staff_email, 1, INSTR(staff_email, '@') - 1),
                '_', ' '
            ),
            '.', ' '
        )
        WHERE staff_email IS NOT NULL
          AND staff_email LIKE '%@%'
          AND staff_name IS NULL
    """)


def down(conn):
    # SQLite doesn't support DROP COLUMN easily
    pass
