# Refactor Plan

Accumulated tech debt from 2026-04-06 testing session. Every fix risked breaking something else due to tight coupling and scattered state. The auto-hangup feature alone caused 3 bugs because it interacted with conference setup, warm transfers, and 3-way calls in ways that weren't obvious.

**Rule: Plan this as a dedicated refactor. Don't mix with feature work.**

## Frontend (phone.html)

1. ~~**Group call state into one object**~~ ✅ Done — `resetCallState()` resets all 19 per-call variables in one shot. Individual vars kept to avoid 200+ renames; the key benefit (no missed resets) is delivered.

2. ~~**Eliminate global flags**~~ ✅ Done — `window._sawMultipleParticipants` now reset inside `resetCallState()`.

3. **Break up phone.html** — transfer logic, call state polling, queue dashboard, contacts all interleaved. Could use `{% include %}` partials. Lower priority now that state management is cleaner.

## Backend (routes.py)

4. ~~**Break up routes.py**~~ ✅ Done — from 7700+ down to 5876 lines. Extracted:
   - `api/twiml.py` — TwiML helpers (audio URL, say/play, closed messages)
   - `api/identity.py` — email/browser/SIP identity conversion
   - `api/schedule.py` — business hours checking, next-open-time
   - `api/call_state.py` — participant resolution, call state polling (270 lines)
   - `api/transfer_routes.py` — all transfer endpoints (~700 lines)
   - `api/recording_routes.py` — all recording endpoints (~410 lines)

5. ~~**Consolidate duplicate call routing paths**~~ ✅ Done — `_build_voicemail_twiml` and `queue_rejected_voicemail` now delegate to `_go_to_voicemail`. `queue_no_answer` inline voicemail replaced with `_build_voicemail_twiml` call. All open-hours voicemail flows through one path. Closed-hours voicemail kept separate (genuinely different prompt logic).

6. ~~**Extract phone number helpers**~~ ✅ Done — `services/phone.py` with `ensure_plus`, `to_e164`, `to_local`, `normalize_au_mobile`, `is_valid_au_mobile`, `format_for_speech`. All inline duplication replaced.

7. ~~**Proper call_state.py module**~~ ✅ Done — `api/call_state.py` with `get_call_state()`, `resolve_participant()`, `build_user_map()`, `get_conference_participants()`. Shared between call state polling and conference participant endpoints.

8. ~~**Call panel name resolution**~~ ✅ Done — `resolve_participant()` extracted as standalone function with explicit parameters (6-strategy resolution chain). No more nested closure scope.

9. ~~**Bare except clauses**~~ ✅ Done — all 16 `except Exception: pass` clauses in routes.py now log at debug/warning level.

10. ~~**`session:` prefix leaking**~~ ✅ Done — added `get_api_caller_email()` for clean email. Transfer endpoints store clean email. Fixed double-prefix bug in callback logging.

---

## Next: Call Participants Table (replaces call_state.py internals)

### Problem

The call panel reverse-engineers participant state from scattered DB entries and Twilio API calls every 3 seconds. Every fix (dedup, fallback lookups, conference name parsing) is a patch over the same fundamental issue: **nobody records who's in a call**.

This causes:
- Agent 2 (transfer target) never sees the call panel
- Duplicate participants after transfers
- Wrong names after blind transfers
- Slow polling (multiple Twilio API round-trips per poll)

### Solution

A `call_participants` table that's the source of truth:

```sql
CREATE TABLE call_participants (
    id INTEGER PRIMARY KEY,
    conference_name TEXT NOT NULL,
    call_sid TEXT NOT NULL,
    role TEXT NOT NULL,           -- 'agent', 'customer', 'transfer_target'
    name TEXT,
    phone_number TEXT,
    email TEXT,
    joined_at TEXT NOT NULL,
    left_at TEXT,
    UNIQUE(conference_name, call_sid)
);
CREATE INDEX idx_call_participants_conf ON call_participants(conference_name);
CREATE INDEX idx_call_participants_sid ON call_participants(call_sid);
```

Updated explicitly at every lifecycle event instead of discovered after the fact.

### Entry Points That Need Writes

| Event | Route/Function | Write |
|-------|---------------|-------|
| Agent answers queue call | `queue_agent_answer`, `conference_join` | Insert agent + customer |
| Outbound call connects | `voice_outbound`, `outbound_customer_join` | Insert agent + customer |
| Extension call connects | `_handle_internal_extension_call` | Insert both agents |
| Transfer target joins | `transfer_consult_join`, `transfer_target_join` | Insert target |
| Transfer completes | `warm_transfer_complete` | Update roles (target→agent, original agent leaves) |
| Transfer fails | `transfer_consult_status` | Remove target |
| Agent answers inbound | `inbound_ring_status` | Insert agent + customer |
| Participant hangs up | `call_status_callback` | Set left_at |
| Conference ends | cleanup | Mark all remaining as left |

### Migration Path

1. Create table (migration)
2. Add DB methods: `add_participant()`, `remove_participant()`, `get_participants()`
3. Add writes to each entry point listed above
4. Replace `get_call_state()` internals with a simple DB read
5. Remove old code: `resolve_participant()`, `_find_agent_in_conference()`, `_deduplicate_participants()`, `_get_customer_from_call_log()`, `build_user_map()`
6. Call state endpoint becomes fast (no Twilio API calls) — can poll more frequently

### Benefits

- **Correct**: participants tracked from creation, not discovered later
- **Fast**: single SQLite query instead of multiple Twilio API calls per poll
- **Simple**: `get_call_state()` becomes ~20 lines instead of ~300
- **Agent 2 works**: transfer target is explicitly added when they join
- **No dedup needed**: each participant added once, removed once
