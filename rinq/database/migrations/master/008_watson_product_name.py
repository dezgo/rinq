"""Set Watson tenant product_name to Tina."""


def up(conn):
    conn.execute("UPDATE tenants SET product_name = 'Tina' WHERE id = 'watson'")


def down(conn):
    conn.execute("UPDATE tenants SET product_name = NULL WHERE id = 'watson'")
