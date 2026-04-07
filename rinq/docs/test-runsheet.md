# Tina Phone System — Test Runsheet

Run through these scenarios after any changes to call handling, hold, or transfer code. Each section tests a different call path.

## 1. Outbound Call (browser to external)

From the Tina phone page, dial an external number (e.g. your mobile).

| # | Test | Expected |
|---|------|----------|
| 1.1 | Dial number, let it ring | Hear ringback tone, then customer answers |
| 1.2 | Dial number, customer doesn't answer | "No answer" status after ~30s |
| 1.3 | Dial number, customer is busy | "Busy" status shown |
| 1.4 | Connected call — hold | Customer hears hold music, button shows "Resume" |
| 1.5 | Connected call — resume | Both parties reconnected, conversation resumes |
| 1.6 | Connected call — agent hangs up | Customer's call ends cleanly |
| 1.7 | Connected call — customer hangs up | Agent sees call ended, status returns to Ready |
| 1.8 | Connected call — blind transfer | Call transfers to target |
| 1.9 | Connected call — warm transfer | Consult, then complete or cancel |
| 1.10 | Connected call — recording | Start/stop recording works |

## 2. Queue Call (customer calls in, waits in queue, agent answers from panel)

Have someone (or your mobile) call a Tina number that routes to a queue.

| # | Test | Expected |
|---|------|----------|
| 2.1 | Call comes in, appears in queue panel | Caller shown with name/number |
| 2.2 | Click Answer on queue panel | Connected to caller |
| 2.3 | Connected — hold | Caller hears hold music |
| 2.4 | Connected — resume | Conversation resumes |
| 2.5 | Connected — hold, then resume, repeat | Works multiple times |
| 2.6 | Connected — agent hangs up | Caller disconnected |
| 2.7 | Connected — caller hangs up | Agent sees call ended |
| 2.8 | Connected — blind transfer | Call transfers |
| 2.9 | Connected — warm transfer (complete) | Caller connected to target |
| 2.10 | Connected — warm transfer (cancel) | Agent reconnected to caller |
| 2.11 | Connected — 3-way call | All three parties connected, modal auto-closes |
| 2.12 | No agents available (all DND) | Caller sent to voicemail immediately |

## 3. Direct Inbound (call flow with dial action)

Call a Tina number whose call flow uses "Dial" action (simultaneous ring to agents).

| # | Test | Expected |
|---|------|----------|
| 3.1 | Call comes in, agent's browser rings | Agent sees incoming call notification |
| 3.2 | Agent answers | Connected to caller |
| 3.3 | Connected — hold | Caller hears hold music |
| 3.4 | Connected — resume | Conversation resumes |
| 3.5 | Connected — agent hangs up | Caller disconnected |
| 3.6 | Connected — caller hangs up | Agent sees call ended |
| 3.7 | Nobody answers | Caller routed to voicemail/AI receptionist |
| 3.8 | Connected — transfer | Works same as queue calls |

## 4. Direct Assignment (phone number assigned to specific agents)

Call a Tina number that has direct phone assignments (no call flow).

| # | Test | Expected |
|---|------|----------|
| 4.1 | Call comes in, assigned agent's browser rings | Agent sees incoming call |
| 4.2 | Agent answers | Connected |
| 4.3 | Connected — hold/resume | Works |
| 4.4 | Connected — hangup from either side | Clean disconnect |

## 5. Internal Extension Call (browser to browser)

From the Tina phone page, dial a 4-digit extension.

| # | Test | Expected |
|---|------|----------|
| 5.1 | Dial extension, recipient answers | Connected |
| 5.2 | Dial extension, recipient doesn't answer | "Not answered" message |
| 5.3 | Dial extension, recipient has DND on | "Currently unavailable" message |
| 5.4 | Connected — hold/resume | Works |
| 5.5 | Connected — hangup from either side | Clean disconnect |

## 6. Transfer Scenarios (from any connected call)

| # | Test | Expected |
|---|------|----------|
| 6.1 | Blind transfer to external number | Caller connected to target |
| 6.2 | Blind transfer to internal extension | Caller connected to extension |
| 6.3 | Warm transfer — complete | Caller connected to target, agent disconnected |
| 6.4 | Warm transfer — cancel | Agent reconnected to caller |
| 6.5 | 3-way — all connected | Modal auto-closes, all three talking |
| 6.6 | 3-way — agent drops out | Other two continue |
| 6.7 | Transfer a call that was already transferred | Works (second transfer) |

## 7. SIP / Desk Phone

| # | Test | Expected |
|---|------|----------|
| 7.1 | Queue call comes in, SIP device rings | Desk phone rings within a few seconds |
| 7.2 | SIP device rings, caller hangs up before answer | Desk phone stops ringing |
| 7.3 | Direct inbound, caller hangs up before answer | SIP and browser both stop ringing |
| 7.4 | Answer on SIP, verify call connects | Can talk to caller |
| 7.5 | Make outgoing call from SIP device | Call connects normally |

## 8. Multi-Tenant / Contacts

| # | Test | Expected |
|---|------|----------|
| 8.1 | Contacts tab shows staff list (no Peter) | Falls back to local staff extensions |
| 8.2 | Transfer modal shows all staff with extensions | Not filtered by is_active |
| 8.3 | Contacts/transfer targets on different tenant | Shows that tenant's staff, not watson's |

## 9. Queue Display

| # | Test | Expected |
|---|------|----------|
| 9.1 | Caller hangs up, queue panel updates | Caller removed within one poll cycle |
| 9.2 | Same number calls twice (redial) | Only shown once (most recent) |
| 9.3 | Stale caller in queue (webhook missed) | Auto-cleaned on next poll |
| 9.4 | Agent in multiple queues sees callers from all | Callers shown, no duplicates |

## 10. Edge Cases

| # | Test | Expected |
|---|------|----------|
| 10.1 | Hold → transfer while on hold | Transfer works from hold state |
| 10.2 | Multiple hold/resume cycles | No degradation, works each time |
| 10.3 | Two agents on calls simultaneously | Each call independent |
| 10.4 | Call during DND | Rejected silently |
| 10.5 | Refresh browser during call | Call state recovers (or ends cleanly) |
| 10.6 | Answer queue call — no hold music gap | Agent hears "Connecting" then caller, not hold music |
| 10.7 | SIP credentials synced after fresh setup | Users table populated with staff_email links |

## Quick Smoke Test (minimum viable check)

If short on time, test these 7 scenarios:

1. **Outbound**: Dial your mobile → talk → hold → resume → hang up
2. **Queue**: Call in → answer from panel → hold → resume → hang up
3. **Inbound dial**: Call a direct-dial number → answer → hold → resume → hang up
4. **Transfer**: On any call → warm transfer → complete
5. **No answer**: Call in when all agents DND → goes to voicemail
6. **SIP ring**: Call in → verify desk phone rings → caller hangs up → phone stops ringing
7. **Queue cleanup**: Stale callers in queue panel → verify they disappear
