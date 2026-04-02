"""
Migration 024: Add zendesk_group_id to voicemail_destinations

Allows voicemail tickets to be routed to specific Zendesk groups
based on which phone number received the call.

The zendesk_group_id is optional - if not set, tickets go to
Zendesk's default group (existing behavior).
"""


def up(conn):
    conn.execute("""
        ALTER TABLE voicemail_destinations
        ADD COLUMN zendesk_group_id INTEGER
    """)
    conn.commit()


def down(conn):
    # SQLite doesn't easily support DROP COLUMN
    # Would need to recreate table - skipping for simplicity
    pass
