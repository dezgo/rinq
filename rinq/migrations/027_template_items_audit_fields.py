"""
Migration 027: Add audit fields to holiday_template_items

The holiday_template_items table was created in migration 006 without
updated_at and updated_by columns. Adding them now for consistency
with the standard audit field pattern.
"""


def up(conn):
    conn.execute("""
        ALTER TABLE holiday_template_items
        ADD COLUMN updated_at TEXT
    """)

    conn.execute("""
        ALTER TABLE holiday_template_items
        ADD COLUMN updated_by TEXT
    """)

    conn.commit()


def down(conn):
    # SQLite doesn't easily support DROP COLUMN
    pass
