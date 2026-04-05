"""Check tenant records for missing Twilio config values.

Usage: venv/bin/python rinq/scripts/check_tenant_config.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from rinq.database.master import get_master_db

REQUIRED_FIELDS = [
    'twilio_account_sid',
    'twilio_auth_token',
    'twilio_api_key',
    'twilio_api_secret',
    'twilio_twiml_app_sid',
    'twilio_default_caller_id',
    'twilio_sip_credential_list_sid',
    'twilio_sip_domain',
]

master_db = get_master_db()
tenants = master_db.get_tenants()

for tenant in tenants:
    t = dict(tenant)
    print(f"\n=== {t['id']} ({t['name']}) ===")
    missing = []
    for key in REQUIRED_FIELDS:
        val = t.get(key)
        status = val[:12] + '...' if val and len(val) > 12 else val or 'MISSING'
        print(f"  {key}: {status}")
        if not val:
            missing.append(key)
    if missing:
        print(f"  ** {len(missing)} MISSING — this tenant may have broken features **")
    else:
        print(f"  All good")
