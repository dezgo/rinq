# Refactor Plan

Accumulated tech debt from 2026-04-06 testing session. Every fix risked breaking something else due to tight coupling and scattered state. The auto-hangup feature alone caused 3 bugs because it interacted with conference setup, warm transfers, and 3-way calls in ways that weren't obvious.

**Rule: Plan this as a dedicated refactor. Don't mix with feature work.**

## Frontend (phone.html)

1. ~~**Group call state into one object**~~ ✅ Done — `resetCallState()` resets all 19 per-call variables in one shot. Individual vars kept for now to avoid 200+ renames; the key benefit (no missed resets) is delivered.

2. ~~**Eliminate global flags**~~ ✅ Done — `window._sawMultipleParticipants` now reset inside `resetCallState()`.

3. **Break up phone.html** — transfer logic, call state polling, conference management all interleaved. Split into separate JS modules. *(Still TODO — lower priority now that state management is cleaner)*

## Backend (routes.py)

4. ~~**Break up routes.py (7000+ lines)**~~ ✅ Started — extracted `api/twiml.py` (TwiML helpers), `api/identity.py` (email/SIP identity), `api/schedule.py` (business hours). ~400 lines moved. More to extract: SIP helpers, call routing, conference management.

5. **Consolidate duplicate call routing paths** — DND/voicemail has two parallel code paths (`<Dial>` and `<Enqueue>`) plus `_handle_closed_call()` inline voicemail. Should route through `_go_to_voicemail` consistently. *(Deferred — high risk to voicemail path)*

6. ~~**Extract phone number helpers**~~ ✅ Done — `services/phone.py` with `ensure_plus`, `to_e164`, `to_local`, `normalize_au_mobile`, `is_valid_au_mobile`, `format_for_speech`. All inline duplication replaced.

7. **Proper call_state.py module** — `_get_call_state_inner` tries to reverse-engineer participant info from Twilio API calls across 4 call types (queue, outbound, extension, transfer). Should track participants from the start when calls are created, not discover them later.

8. **Call panel name resolution** — `resolve_participant` has 6 fallback steps with silent exception handling. Needs a single reliable path that works for all call types.

9. ~~**Bare except clauses**~~ ✅ Done — all 16 `except Exception: pass` clauses in routes.py now log at debug/warning level.

10. ~~**`session:` prefix leaking**~~ ✅ Done — added `get_api_caller_email()` for clean email. Transfer endpoints now store clean email. Fixed double-prefix bug in callback logging.
