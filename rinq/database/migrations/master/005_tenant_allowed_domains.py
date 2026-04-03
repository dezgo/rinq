"""Add allowed_domains to tenants for auto-provisioning users."""


def up(conn):
    conn.execute("ALTER TABLE tenants ADD COLUMN allowed_domains TEXT")


def down(conn):
    pass
