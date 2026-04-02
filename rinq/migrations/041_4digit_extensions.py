"""Migrate 3-digit extensions to 4-digit.

Prefixes existing 3-digit extensions (100-999) with '1' so they become
4-digit (1100-1999). Extensions already 4+ digits are left unchanged.
"""


def up(conn):
    # Prefix all 3-digit extensions with '1'
    conn.execute("""
        UPDATE staff_extensions
        SET extension = '1' || extension
        WHERE LENGTH(extension) = 3
    """)


def down(conn):
    # Strip the leading '1' from extensions that were migrated
    conn.execute("""
        UPDATE staff_extensions
        SET extension = SUBSTR(extension, 2)
        WHERE LENGTH(extension) = 4
          AND extension LIKE '1%'
          AND CAST(SUBSTR(extension, 2) AS INTEGER) BETWEEN 100 AND 999
    """)
