"""
Add holiday templates for managing public holidays across multiple schedules.

This migration adds:
- holiday_templates: Named templates (e.g., "Australian National 2026", "ACT Public Holidays")
- holiday_template_items: Holidays within each template
- template_item_id on schedule_holidays: Track which holidays came from templates

Workflow:
1. Create template with holidays (e.g., "Australian National" with Christmas, Boxing Day, etc.)
2. Apply template to schedules - copies holidays in
3. Sync later to verify/update all schedules have the right holidays
4. Ad-hoc holidays (staff away, etc.) are added directly without template link
"""

from datetime import datetime


def up(conn):
    # Holiday templates - named collections of holidays
    conn.execute("""
        CREATE TABLE IF NOT EXISTS holiday_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_by TEXT
        )
    """)

    # Items within each template
    conn.execute("""
        CREATE TABLE IF NOT EXISTS holiday_template_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            template_id INTEGER NOT NULL,
            name TEXT NOT NULL,           -- "Christmas Day", "Boxing Day"
            date TEXT NOT NULL,           -- "12-25" for recurring, "2026-12-25" for specific
            is_recurring INTEGER DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT,
            FOREIGN KEY (template_id) REFERENCES holiday_templates(id) ON DELETE CASCADE
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_template_items_template ON holiday_template_items(template_id)")

    # Add template_item_id to schedule_holidays to track origin
    # NULL = ad-hoc holiday, non-NULL = came from template (can be synced)
    conn.execute("""
        ALTER TABLE schedule_holidays
        ADD COLUMN template_item_id INTEGER REFERENCES holiday_template_items(id)
    """)

    conn.commit()


def down(conn):
    # Remove template_item_id from schedule_holidays (SQLite limitation - can't drop columns easily)
    # So we'll leave it but it won't be used

    conn.execute("DROP TABLE IF EXISTS holiday_template_items")
    conn.execute("DROP TABLE IF EXISTS holiday_templates")
    conn.commit()
