"""Convert escape settings from seconds to music play counts.

Both escape_announcement_delay and escape_repeat_interval were stored in
seconds but announcements can only play between music cycles, so seconds
gave false precision. Now both store music play counts.
"""


def up(conn):
    # Convert escape_repeat_interval: seconds -> cycle count
    # 0 stays as 0 (announce once only)
    # 60 -> 1, 120 -> 2, 180 -> 3, etc.
    conn.execute("""
        UPDATE queues
        SET escape_repeat_interval = CASE
            WHEN escape_repeat_interval = 0 THEN 0
            WHEN escape_repeat_interval <= 60 THEN 1
            ELSE MAX(1, ROUND(escape_repeat_interval / 60.0))
        END
        WHERE escape_repeat_interval > 10
    """)

    # Convert escape_announcement_delay: seconds -> cycle count
    # 0 stays as 0 (announce immediately)
    # 60 -> 1 (after first track), 120 -> 2, etc.
    conn.execute("""
        UPDATE queues
        SET escape_announcement_delay = CASE
            WHEN escape_announcement_delay = 0 THEN 0
            WHEN escape_announcement_delay <= 60 THEN 1
            ELSE MAX(1, ROUND(escape_announcement_delay / 60.0))
        END
        WHERE escape_announcement_delay > 10
    """)


def down(conn):
    conn.execute("""
        UPDATE queues
        SET escape_repeat_interval = escape_repeat_interval * 60
        WHERE escape_repeat_interval <= 10 AND escape_repeat_interval > 0
    """)
    conn.execute("""
        UPDATE queues
        SET escape_announcement_delay = escape_announcement_delay * 60
        WHERE escape_announcement_delay <= 10 AND escape_announcement_delay > 0
    """)
