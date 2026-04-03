"""Add Twilio address SID to tenants."""


def up(conn):
    conn.execute("ALTER TABLE tenants ADD COLUMN twilio_address_sid TEXT")


def down(conn):
    pass
