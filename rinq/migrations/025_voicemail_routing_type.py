"""
Migration 025: Add routing_type to voicemail_destinations and link call_flows by ID

This refactors voicemail routing to be more flexible:
- routing_type: 'zendesk' (create ticket via API) or 'email' (send email)
- email becomes optional (only needed for 'email' routing type)
- call_flows now references voicemail_destination_id instead of voicemail_email

This allows Zendesk destinations to just specify a group without needing
a fake email address.
"""


def up(conn):
    # Add routing_type column (default 'email' for backward compatibility)
    conn.execute("""
        ALTER TABLE voicemail_destinations
        ADD COLUMN routing_type TEXT NOT NULL DEFAULT 'email'
    """)

    # Add voicemail_destination_id to call_flows
    conn.execute("""
        ALTER TABLE call_flows
        ADD COLUMN voicemail_destination_id INTEGER REFERENCES voicemail_destinations(id)
    """)

    # Migrate existing data: link call_flows to destinations by matching email
    conn.execute("""
        UPDATE call_flows
        SET voicemail_destination_id = (
            SELECT id FROM voicemail_destinations
            WHERE voicemail_destinations.email = call_flows.voicemail_email
        )
        WHERE voicemail_email IS NOT NULL
    """)

    # Update existing destinations that have zendesk_group_id to be 'zendesk' type
    conn.execute("""
        UPDATE voicemail_destinations
        SET routing_type = 'zendesk'
        WHERE zendesk_group_id IS NOT NULL
    """)

    conn.commit()


def down(conn):
    # Can't easily drop columns in SQLite
    pass
