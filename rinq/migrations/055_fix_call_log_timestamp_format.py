"""
Migration 055: Fix call_log timestamp format for correct string comparison.

started_at was stored with ISO 'T' separator (e.g. '2026-03-30T03:00:00')
but queries use space separator ('2026-03-30 03:00:00'). Since SQLite uses
lexicographic comparison, 'T' > ' ' causes incorrect date range filtering.

Also fix answered_at and ended_at for consistency.
"""


def up(conn):
    """Replace 'T' separator with space in all timestamp columns."""
    for col in ('started_at', 'answered_at', 'ended_at'):
        conn.execute(f"""
            UPDATE call_log
            SET {col} = REPLACE({col}, 'T', ' ')
            WHERE {col} LIKE '%T%'
        """)


def down(conn):
    """No-op - space separator is the correct SQLite format."""
    pass
