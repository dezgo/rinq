"""Add closed_message_parts to call_flows for flexible closed message sequencing.

Stores an ordered JSON array of message segments, e.g.:
[
    {"type": "audio", "audio_id": 5},
    {"type": "opentime"},
    {"type": "openday"},
    {"type": "audio", "audio_id": 6}
]
"""


def up(conn):
    conn.execute("ALTER TABLE call_flows ADD COLUMN closed_message_parts TEXT")


def down(conn):
    # SQLite doesn't support DROP COLUMN before 3.35.0
    pass
