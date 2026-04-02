# Polycom VVX 300 — Twilio SIP Registration Setup

Configuration guide for Polycom VVX 300 desk phones connecting to Twilio SIP.
Access the phone's web UI at its IP address (check phone screen: Settings > Status > Network > TCP/IP Parameters).

## Settings > SIP

### Local Settings

| Setting | Value |
|---------|-------|
| Local SIP Port | `0` (auto) |
| Calls Per Line Key | `24` |

### Outbound Proxy

| Setting | Value |
|---------|-------|
| Address | `watsonblinds.sip.sydney.twilio.com` |
| Port | `5060` |
| Transport | `DNSnaptr` |

### Server 1

| Setting | Value |
|---------|-------|
| Special Interop | `Standard` |
| Address | `watsonblinds.sip.twilio.com` |
| Port | `5060` |
| Transport | `DNSnaptr` |
| Expires (s) | `600` (Twilio minimum — do NOT set lower) |
| Subscription Expires (s) | `600` |
| Register | `Yes` |

## Settings > Lines > Line 1

### Identification

| Setting | Value |
|---------|-------|
| Display Name | User's extension number (e.g. `6809`) |
| Address | Twilio SIP username (e.g. `phillip_fenech`) |
| Type | `Private` |
| Number of Line Keys | `1` |
| Calls Per Line | `24` |
| Enable SRTP | `Yes` |
| Offer SRTP | `No` |
| Require SRTP | `No` |
| Server Auto Discovery | `Enable` |

### Authentication

| Setting | Value |
|---------|-------|
| Use Login Credentials | `Disable` |
| Domain | `watsonblinds.sip.twilio.com` (NO port suffix!) |
| User ID | Twilio SIP username (e.g. `phillip_fenech`) |
| Password | SIP password from Tina's users table |

### Outbound Proxy

Leave blank — inherits from SIP-level outbound proxy.

| Setting | Value |
|---------|-------|
| Address | *(blank)* |
| Port | `0` |
| Transport | `DNSnaptr` |

### Server 1

| Setting | Value |
|---------|-------|
| Address | `watsonblinds.sip.sydney.twilio.com` |
| Port | `5060` |
| Transport | `UDPOnly` |
| Expires (s) | `600` |
| Subscription Expires (s) | `600` |

## Common Gotchas

1. **Do NOT append `:5060` to the Authentication Domain** — this breaks inbound call routing (Twilio can't match credentials). Outbound still works, making it hard to diagnose.

2. **Expires must be >= 600** — Twilio rejects registrations with shorter intervals (`423 Interval too brief`).

3. **Use the Sydney edge** (`sip.sydney.twilio.com`) for the outbound proxy and line server address. Without it, traffic routes through Ashburn, VA (higher latency for AU).

4. **SIP credentials** come from Tina's `users` table — the `username` and `password` fields. These are managed via Tina's web UI (SIP Users page).

## Troubleshooting

- **Outbound works, inbound doesn't**: Check the Authentication Domain for typos/port suffixes. Check Twilio call logs for error 32011 (timeout reaching private IP = NAT/registration issue).
- **Registration failing**: Verify Expires >= 600, check credentials match Tina's users table exactly.
- **Check registration status**: Phone screen > Settings > Status > Lines > Line 1 should show "Registered".
- **Twilio SIP domain check**: Hit Tina's API to verify credential list is linked for both calls and registrations.
