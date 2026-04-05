"""Check SIP domain config from Twilio API."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import requests
from rinq.database.master import get_master_db

t = dict(get_master_db().get_tenant('derek'))
auth = (t['twilio_account_sid'], t['twilio_auth_token'])
base = f"https://api.twilio.com/2010-04-01/Accounts/{t['twilio_account_sid']}"

print("=== Domain config ===")
r = requests.get(f"{base}/SIP/Domains/SDb6dfe60973d7e30510a373283ef8111a.json", auth=auth)
print(json.dumps(r.json(), indent=2))

print("\n=== IP Access Control Lists ===")
r = requests.get(f"{base}/SIP/Domains/SDb6dfe60973d7e30510a373283ef8111a/IpAccessControlListMappings.json", auth=auth)
print(json.dumps(r.json(), indent=2))

print("\n=== Recent alerts (SIP errors) ===")
r = requests.get(f"{base}/Notifications.json?PageSize=5&MessageText=sip", auth=auth)
for n in r.json().get('notifications', []):
    print(f"  {n.get('date_created')} - {n.get('message_text', '')[:120]}")
if not r.json().get('notifications'):
    print("  None found")
