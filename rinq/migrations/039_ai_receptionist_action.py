"""
Add AI receptionist as a call flow action option.

Adds open_no_answer_action to call_flows to control what happens when
staff don't answer during open hours (voicemail, ai_receptionist, etc).

The closed_action column already exists and can now also be set to 'ai_receptionist'.
"""


def up(conn):
    # Add open_no_answer_action to call_flows
    # Default 'ai_receptionist' so all queues use Rosie unless explicitly changed
    conn.execute("""
        ALTER TABLE call_flows
        ADD COLUMN open_no_answer_action TEXT DEFAULT 'ai_receptionist'
    """)

    conn.commit()


def down(conn):
    # SQLite doesn't support DROP COLUMN before 3.35.0
    # Just leave the column - it's harmless if unused
    pass
