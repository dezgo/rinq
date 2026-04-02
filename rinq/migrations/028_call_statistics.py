"""
Migration 028: Add tables for call statistics aggregation.

Creates two tables for reporting:
1. daily_call_stats - Daily aggregates by queue and agent
2. hourly_call_stats - Hourly distribution for trend analysis

These tables preserve queue statistics that would otherwise be lost
when queued_calls records are cleaned up after 24 hours.
"""


def up(conn):
    """Create call statistics tables."""

    # Daily call statistics - aggregated per day, per queue, per agent
    conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_call_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            -- Date for this aggregate (YYYY-MM-DD format)
            stat_date TEXT NOT NULL,

            -- Optional filters (NULL means "all")
            queue_id INTEGER,
            queue_name TEXT,
            agent_email TEXT,

            -- Call volume metrics
            total_calls INTEGER DEFAULT 0,
            answered_calls INTEGER DEFAULT 0,
            abandoned_calls INTEGER DEFAULT 0,
            timeout_calls INTEGER DEFAULT 0,
            transferred_calls INTEGER DEFAULT 0,

            -- Duration metrics (in seconds)
            total_duration_seconds INTEGER DEFAULT 0,
            total_wait_seconds INTEGER DEFAULT 0,

            -- Wait time breakdown (for answered calls)
            answered_within_15s INTEGER DEFAULT 0,
            answered_within_30s INTEGER DEFAULT 0,
            answered_within_60s INTEGER DEFAULT 0,
            answered_within_90s INTEGER DEFAULT 0,
            answered_over_90s INTEGER DEFAULT 0,

            -- Wait time for abandoned calls
            abandoned_total_wait_seconds INTEGER DEFAULT 0,

            -- Peak wait times
            max_wait_seconds INTEGER DEFAULT 0,
            max_answered_wait_seconds INTEGER DEFAULT 0,
            max_abandoned_wait_seconds INTEGER DEFAULT 0,

            -- Inbound/outbound breakdown (from recording_log)
            inbound_calls INTEGER DEFAULT 0,
            outbound_calls INTEGER DEFAULT 0,

            -- Timestamps
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

            -- Unique constraint: one row per date/queue/agent combination
            UNIQUE(stat_date, queue_id, agent_email)
        )
    """)

    # Hourly call statistics - for time-of-day distribution charts
    conn.execute("""
        CREATE TABLE IF NOT EXISTS hourly_call_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            -- Date and hour for this aggregate
            stat_date TEXT NOT NULL,  -- YYYY-MM-DD
            stat_hour INTEGER NOT NULL,  -- 0-23

            -- Optional filters
            queue_id INTEGER,
            queue_name TEXT,

            -- Call counts by outcome
            total_calls INTEGER DEFAULT 0,
            answered_calls INTEGER DEFAULT 0,
            abandoned_calls INTEGER DEFAULT 0,
            timeout_calls INTEGER DEFAULT 0,

            -- Timestamps
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

            -- Unique constraint: one row per date/hour/queue
            UNIQUE(stat_date, stat_hour, queue_id)
        )
    """)

    # Indexes for efficient querying
    conn.execute("CREATE INDEX IF NOT EXISTS idx_daily_stats_date ON daily_call_stats(stat_date)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_daily_stats_agent ON daily_call_stats(agent_email, stat_date)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_daily_stats_queue ON daily_call_stats(queue_id, stat_date)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_hourly_stats_date ON hourly_call_stats(stat_date)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_hourly_stats_queue ON hourly_call_stats(queue_id, stat_date)")


def down(conn):
    """Drop call statistics tables."""
    conn.execute("DROP TABLE IF EXISTS hourly_call_stats")
    conn.execute("DROP TABLE IF EXISTS daily_call_stats")
