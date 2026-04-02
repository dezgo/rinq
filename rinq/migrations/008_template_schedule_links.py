"""
Migration 008: Add template-schedule links

Allows templates to be associated with specific schedules so that:
- Sync preview only shows linked schedules
- Sync only applies to linked schedules
- Each region's template only syncs to relevant schedules
"""


def up(conn):
    """Create template_schedule_links table."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS template_schedule_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            template_id INTEGER NOT NULL,
            schedule_id INTEGER NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT,
            FOREIGN KEY (template_id) REFERENCES holiday_templates(id) ON DELETE CASCADE,
            FOREIGN KEY (schedule_id) REFERENCES schedules(id) ON DELETE CASCADE,
            UNIQUE(template_id, schedule_id)
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_template_schedule_links_template
        ON template_schedule_links(template_id)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_template_schedule_links_schedule
        ON template_schedule_links(schedule_id)
    """)


def down(conn):
    """Drop template_schedule_links table."""
    conn.execute("DROP TABLE IF EXISTS template_schedule_links")
