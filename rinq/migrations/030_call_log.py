"""
Migration 030: Add call_log table for comprehensive call tracking.

This table tracks ALL calls - inbound, outbound, direct-answered, queued,
voicemail, missed, etc. It provides a complete picture of call activity
for reporting purposes.

The existing queued_calls table is kept for queue-specific features
(dashboard showing who's waiting in queue). The call_log table is the
source of truth for all call statistics and reporting.
"""


def up(conn):
    """Create call_log table."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS call_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            -- Twilio identifiers
            call_sid TEXT UNIQUE NOT NULL,
            parent_call_sid TEXT,  -- For child legs (transfers, etc.)

            -- Call direction and type
            direction TEXT NOT NULL,  -- 'inbound' or 'outbound'
            call_type TEXT,  -- 'direct', 'queue', 'transfer', 'voicemail', 'forwarded'

            -- Numbers involved
            from_number TEXT NOT NULL,
            to_number TEXT NOT NULL,

            -- For inbound: which phone number was called
            -- For outbound: which phone number was used as caller ID
            phone_number_id TEXT,  -- FK to phone_numbers.sid

            -- Queue info (if call went through a queue)
            queue_id INTEGER,
            queue_name TEXT,

            -- Call flow that handled this call (for inbound)
            call_flow_id INTEGER,

            -- Call status
            -- inbound: ringing, answered, queued, voicemail, abandoned, missed, busy, failed
            -- outbound: ringing, answered, busy, no-answer, failed
            status TEXT NOT NULL DEFAULT 'ringing',

            -- Who answered/made the call
            agent_email TEXT,  -- Staff email

            -- Timing
            started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            answered_at TEXT,
            ended_at TEXT,

            -- Duration metrics (in seconds)
            ring_seconds INTEGER,  -- How long before answered (or hung up)
            talk_seconds INTEGER,  -- Actual conversation time
            total_seconds INTEGER,  -- Total call duration

            -- Customer info (enriched from Clara/Otto for inbound calls)
            customer_id INTEGER,
            customer_name TEXT,
            customer_email TEXT,

            -- Was this call recorded?
            is_recorded INTEGER DEFAULT 0,
            recording_sid TEXT,

            -- Additional context
            notes TEXT,

            -- Audit fields
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (queue_id) REFERENCES queues(id),
            FOREIGN KEY (call_flow_id) REFERENCES call_flows(id)
        )
    """)

    # Indexes for efficient querying
    conn.execute("CREATE INDEX IF NOT EXISTS idx_call_log_direction ON call_log(direction)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_call_log_status ON call_log(status)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_call_log_started ON call_log(started_at)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_call_log_agent ON call_log(agent_email)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_call_log_queue ON call_log(queue_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_call_log_from ON call_log(from_number)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_call_log_to ON call_log(to_number)")


def down(conn):
    """Drop call_log table."""
    conn.execute("DROP TABLE IF EXISTS call_log")
