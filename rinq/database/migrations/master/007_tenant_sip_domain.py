"""Add SIP domain name to tenant record so we don't need to call Twilio API to display it."""


def up(conn):
    conn.execute("ALTER TABLE tenants ADD COLUMN twilio_sip_domain TEXT")


def down(conn):
    pass
