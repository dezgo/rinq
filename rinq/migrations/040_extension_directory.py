"""
Add extension directory as a call flow open_action option.

Adds extension_prompt_audio_id and extension_no_answer_action columns
to call_flows for the auto-attendant extension dialing feature.
"""


def up(conn):
    # Custom audio prompt for "please enter the extension of the person you're trying to reach"
    conn.execute("""
        ALTER TABLE call_flows
        ADD COLUMN extension_prompt_audio_id INTEGER REFERENCES audio_files(id)
    """)

    # What happens when extension user doesn't answer or invalid extension
    # Options: 'voicemail', 'ai_receptionist', 'queue'
    conn.execute("""
        ALTER TABLE call_flows
        ADD COLUMN extension_no_answer_action TEXT DEFAULT 'voicemail'
    """)

    conn.commit()


def down(conn):
    # SQLite doesn't support DROP COLUMN before 3.35.0
    pass
