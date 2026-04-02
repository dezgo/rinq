"""
Multi-tenant support for Tina/Rinq.

When RINQ_MULTI_TENANT=true, each tenant gets their own database
and Twilio config. Tenants are resolved from session (web) or
from the called phone number (Twilio webhooks).

When multi-tenant is off (default), Tina runs in single-tenant mode
using the existing database and config.
"""
