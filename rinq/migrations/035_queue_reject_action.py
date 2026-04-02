"""Add reject_action column to queues table.

This controls what happens when an agent actively rejects a call (presses end/reject):
- 'continue' (default): Keep ringing other devices, caller stays in queue
- 'voicemail': Cancel all ringing devices, send caller to voicemail immediately

Regional stores prefer 'voicemail' so callers don't wait in an empty queue.
Canberra prefers 'continue' so other agents can still answer.
"""


def up(conn):
    # Add reject_action column with default 'continue'
    conn.execute("""
        ALTER TABLE queues ADD COLUMN reject_action TEXT DEFAULT 'continue'
    """)


def down(conn):
    # SQLite doesn't support DROP COLUMN easily
    pass
