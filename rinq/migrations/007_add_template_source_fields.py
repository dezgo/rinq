"""
Migration 007: Add source URL and data-as-at fields to holiday templates.

Allows tracking where holiday data came from and when it was last verified.
"""


def up(conn):
    """Add source_url and data_as_at columns to holiday_templates."""
    # Add source URL field
    conn.execute("""
        ALTER TABLE holiday_templates
        ADD COLUMN source_url TEXT
    """)

    # Add data as at date field
    conn.execute("""
        ALTER TABLE holiday_templates
        ADD COLUMN data_as_at TEXT
    """)


def down(conn):
    """Remove source fields (SQLite doesn't support DROP COLUMN easily)."""
    pass
