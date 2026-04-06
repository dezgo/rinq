# Refactor Plan

Accumulated tech debt from 2026-04-06 testing session. Every fix risked breaking something else due to tight coupling and scattered state. The auto-hangup feature alone caused 3 bugs because it interacted with conference setup, warm transfers, and 3-way calls in ways that weren't obvious.

**Rule: Plan this as a dedicated refactor. Don't mix with feature work.**

## Frontend (phone.html)

1. **Group call state into one object** — seven+ variables reset individually in endCall(). Should be `callState = {call, queueCallerSid, outboundCallSid, ...}` reset with one assignment. Would prevent bugs from missed resets.

2. **Eliminate global flags** — `window._sawMultipleParticipants` is fragile across refreshes. Should be part of the grouped call state.

3. **Break up phone.html** — transfer logic, call state polling, conference management all interleaved. Split into separate JS modules.

## Backend (routes.py)

4. **Break up routes.py (7000+ lines)** — deeply coupled transfer/hold/conference logic. Split into focused modules: `conference.py`, `transfer.py`, `call_state.py`, etc.

5. **Consolidate duplicate call routing paths** — DND/voicemail has two parallel code paths (`<Dial>` and `<Enqueue>`) that need identical fixes applied separately. Should be one path through `_go_to_voicemail`.

6. **Extract phone number helpers** — plus-prefix normalization duplicated at lines 3668/3822, phone formatting scattered throughout. Should be one `normalize_phone()` utility.

7. **Proper call_state.py module** — `_get_call_state_inner` tries to reverse-engineer participant info from Twilio API calls across 4 call types (queue, outbound, extension, transfer). Should track participants from the start when calls are created, not discover them later.

8. **Call panel name resolution** — `resolve_participant` has 6 fallback steps with silent exception handling. Needs a single reliable path that works for all call types.

9. **Bare except clauses** — dozens of `except Exception: pass/continue` hiding real errors. Each should at minimum log a warning.

10. **`session:` prefix leaking** — `get_api_caller()` returns `session:email` which leaked into client identities and transfer state. Should strip prefix at the source or use a clean email getter.
