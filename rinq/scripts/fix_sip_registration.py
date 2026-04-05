"""Enable SIP registration on derek's domain."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from rinq.database.master import get_master_db
from twilio.rest import Client

t = dict(get_master_db().get_tenant('derek'))
client = Client(t['twilio_account_sid'], t['twilio_auth_token'])

domain = client.sip.domains('SDb6dfe60973d7e30510a373283ef8111a').update(
    sip_registration=True
)
print(f'Enabled SIP registration on {domain.domain_name}')
