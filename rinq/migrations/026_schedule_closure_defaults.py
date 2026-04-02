"""
Migration 026: Add default closure settings to schedules

Allows schedules to define default action, audio, and forward_to for closures.
Individual closures can still override these defaults when needed.

Fields added to schedules:
- default_closure_action: 'message', 'voicemail', 'forward' (NULL = no default)
- default_closure_audio_id: FK to audio_files for default audio
- default_closure_forward_to: Phone number for forward action

Usage:
- When a closure has action=NULL, it inherits default_closure_action from schedule
- When a closure has audio_id=NULL and action is message/voicemail, it inherits default_closure_audio_id
- When a closure has forward_to=NULL and action is forward, it inherits default_closure_forward_to
"""


def up(conn):
    # Default action for closures (NULL = use call flow's closed_action)
    conn.execute("""
        ALTER TABLE schedules
        ADD COLUMN default_closure_action TEXT
    """)

    # Default audio file for closure messages/voicemail
    conn.execute("""
        ALTER TABLE schedules
        ADD COLUMN default_closure_audio_id INTEGER REFERENCES audio_files(id)
    """)

    # Default forward number for closure forward action
    conn.execute("""
        ALTER TABLE schedules
        ADD COLUMN default_closure_forward_to TEXT
    """)

    conn.commit()


def down(conn):
    # SQLite doesn't easily support DROP COLUMN
    pass
