"""
Migration 016: Add queued_calls table for tracking callers in queue with enriched data.

This table stores caller information enriched from Clara (customer data) and
Otto (order data) to help agents prioritize and identify callers.
"""


def up(conn):
    """Create queued_calls table."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS queued_calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            -- Twilio identifiers
            call_sid TEXT UNIQUE NOT NULL,
            queue_id INTEGER NOT NULL,
            queue_name TEXT,

            -- Call details
            caller_number TEXT NOT NULL,
            called_number TEXT NOT NULL,

            -- Enriched from Clara
            customer_id INTEGER,
            customer_name TEXT,
            customer_email TEXT,

            -- Enriched from Otto (JSON for flexibility)
            -- Contains: active_orders, next_installation, order_summary
            order_data TEXT,

            -- Priority: high, medium, normal, unknown
            priority TEXT DEFAULT 'normal',
            priority_reason TEXT,

            -- Status: waiting, answered, abandoned, timeout
            status TEXT DEFAULT 'waiting',

            -- Timestamps
            enqueued_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            answered_at TEXT,
            answered_by TEXT,  -- Agent email who answered
            ended_at TEXT,

            -- Wait time in seconds (calculated when answered/ended)
            wait_seconds INTEGER,

            FOREIGN KEY (queue_id) REFERENCES queues(id)
        )
    """)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_queued_calls_status ON queued_calls(status)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_queued_calls_queue ON queued_calls(queue_id, status)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_queued_calls_caller ON queued_calls(caller_number)")


def down(conn):
    """Drop queued_calls table."""
    conn.execute("DROP TABLE IF EXISTS queued_calls")
