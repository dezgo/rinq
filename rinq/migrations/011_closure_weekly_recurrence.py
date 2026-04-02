"""
Add weekly recurrence support to closures (schedule_holidays).

Allows closures to repeat weekly (e.g., "Saturday showroom hours" every Saturday 9am-1pm)
with their own audio and action, separate from regular closed behavior.

Fields added:
- recurrence: 'once' (default, existing behavior) or 'weekly'
- day_of_week: 0-6 (Mon-Sun) for weekly recurrence
- start_time: HH:MM for time-based closures (NULL = all day)
- end_time: HH:MM for time-based closures
- action: what to do during this closure (NULL = use schedule's closed_action)

Example: Saturday 9am-1pm showroom hours
- recurrence = 'weekly'
- day_of_week = 5 (Saturday)
- start_time = '09:00'
- end_time = '13:00'
- audio_id = (showroom open message)
- action = 'voicemail'
"""


def up(conn):
    # Add recurrence type: 'once' (specific date) or 'weekly' (repeats)
    conn.execute("""
        ALTER TABLE schedule_holidays
        ADD COLUMN recurrence TEXT NOT NULL DEFAULT 'once'
    """)

    # Day of week for weekly recurrence (0=Monday, 6=Sunday)
    conn.execute("""
        ALTER TABLE schedule_holidays
        ADD COLUMN day_of_week INTEGER
    """)

    # Time range for the closure (NULL = all day)
    conn.execute("""
        ALTER TABLE schedule_holidays
        ADD COLUMN start_time TEXT
    """)

    conn.execute("""
        ALTER TABLE schedule_holidays
        ADD COLUMN end_time TEXT
    """)

    # Action to take during this closure (NULL = use schedule's closed_action)
    # Options: 'message', 'voicemail', 'forward'
    conn.execute("""
        ALTER TABLE schedule_holidays
        ADD COLUMN action TEXT
    """)

    conn.commit()


def down(conn):
    # SQLite doesn't support DROP COLUMN easily
    # Columns will remain but be unused
    pass
