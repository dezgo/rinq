"""Make schedule_holidays.date nullable for weekly recurring closures.

Weekly closures use day_of_week instead of date, but the original schema
defined date as NOT NULL, preventing weekly closures from being saved.
"""


def up(conn):
    # SQLite doesn't support ALTER COLUMN, so recreate the table
    conn.execute("ALTER TABLE schedule_holidays RENAME TO schedule_holidays_old")

    conn.execute("""
        CREATE TABLE schedule_holidays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            schedule_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            date TEXT,
            is_recurring INTEGER DEFAULT 0,
            recurrence TEXT DEFAULT 'once',
            day_of_week INTEGER,
            start_time TEXT,
            end_time TEXT,
            action TEXT,
            audio_id INTEGER,
            forward_to TEXT,
            template_item_id INTEGER REFERENCES holiday_template_items(id),
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT,
            FOREIGN KEY (schedule_id) REFERENCES schedules(id),
            FOREIGN KEY (audio_id) REFERENCES audio_files(id)
        )
    """)

    # Check if old table has template_item_id (added by migration 006)
    old_columns = [row[1] for row in conn.execute("PRAGMA table_info(schedule_holidays_old)").fetchall()]
    if 'template_item_id' in old_columns:
        conn.execute("""
            INSERT INTO schedule_holidays
                (id, schedule_id, name, date, is_recurring, recurrence, day_of_week,
                 start_time, end_time, action, audio_id, forward_to, template_item_id, created_at, created_by)
            SELECT id, schedule_id, name, date, is_recurring, recurrence, day_of_week,
                   start_time, end_time, action, audio_id, forward_to, template_item_id, created_at, created_by
            FROM schedule_holidays_old
        """)
    else:
        conn.execute("""
            INSERT INTO schedule_holidays
                (id, schedule_id, name, date, is_recurring, recurrence, day_of_week,
                 start_time, end_time, action, audio_id, forward_to, created_at, created_by)
            SELECT id, schedule_id, name, date, is_recurring, recurrence, day_of_week,
                   start_time, end_time, action, audio_id, forward_to, created_at, created_by
            FROM schedule_holidays_old
        """)

    conn.execute("DROP TABLE schedule_holidays_old")


def down(conn):
    # Set any NULL dates to empty string so we can restore NOT NULL
    conn.execute("UPDATE schedule_holidays SET date = '' WHERE date IS NULL")

    conn.execute("ALTER TABLE schedule_holidays RENAME TO schedule_holidays_old")

    conn.execute("""
        CREATE TABLE schedule_holidays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            schedule_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            is_recurring INTEGER DEFAULT 0,
            recurrence TEXT DEFAULT 'once',
            day_of_week INTEGER,
            start_time TEXT,
            end_time TEXT,
            action TEXT,
            audio_id INTEGER,
            forward_to TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT,
            FOREIGN KEY (schedule_id) REFERENCES schedules(id),
            FOREIGN KEY (audio_id) REFERENCES audio_files(id)
        )
    """)

    conn.execute("""
        INSERT INTO schedule_holidays
            (id, schedule_id, name, date, is_recurring, recurrence, day_of_week,
             start_time, end_time, action, audio_id, forward_to, created_at, created_by)
        SELECT id, schedule_id, name, date, is_recurring, recurrence, day_of_week,
               start_time, end_time, action, audio_id, forward_to, created_at, created_by
        FROM schedule_holidays_old
    """)

    conn.execute("DROP TABLE schedule_holidays_old")
