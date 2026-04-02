"""Add is_active_locked to staff_extensions.

When is_active_locked=1, auto-activation won't change the is_active status.
This lets admins manually deactivate someone and have it stick, even if
they have call history or other usage signals.

When is_active_locked=0 (default), the system can auto-activate staff
based on usage signals (call history, queue membership, etc).
"""


def up(conn):
    conn.execute("""
        ALTER TABLE staff_extensions ADD COLUMN is_active_locked INTEGER DEFAULT 0
    """)


def down(conn):
    pass
