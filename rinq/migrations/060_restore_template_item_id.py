"""Restore template_item_id column on schedule_holidays.

Migration 006 added this column, but migration 053 recreated the table
without it, dropping the column. This restores it.
"""


def up(conn):
    # Check if column already exists (in case 006 ran after 053 on some installs)
    columns = [row[1] for row in conn.execute("PRAGMA table_info(schedule_holidays)").fetchall()]
    if 'template_item_id' not in columns:
        conn.execute("""
            ALTER TABLE schedule_holidays
            ADD COLUMN template_item_id INTEGER REFERENCES holiday_template_items(id)
        """)


def down(conn):
    pass  # SQLite can't drop columns easily; leave it
