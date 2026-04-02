"""
Full call flow schema for proper IVR/PBX functionality.

This migration adds:
- users: Staff members who can make/receive calls
- user_devices: How to reach each user (browser, mobile, SIP)
- audio_files: Greetings, hold music, messages
- schedules: Business hours and holidays
- queues: Ring groups with hold music
- queue_members: Who's in each queue
- call_flows: What happens when a number is called
- callback_requests: Pending customer callbacks

The phone_assignments table is migrated to queue_members via a default queue.
"""

from datetime import datetime


def up(conn):
    # =========================================================================
    # Users - Staff members (may already exist from migration 001)
    # =========================================================================
    # The existing 'users' table is for SIP credentials. We'll keep it but
    # add a proper staff users table. Actually, let's rename concepts:
    # - users table stays as-is (SIP credentials)
    # - We'll use staff_email from phone_assignments as the user identifier
    #   and link to Peter for full staff info when needed

    # =========================================================================
    # Audio Files - Greetings, hold music, messages
    # =========================================================================
    conn.execute("""
        CREATE TABLE IF NOT EXISTS audio_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            file_type TEXT NOT NULL,  -- 'greeting', 'hold_music', 'voicemail_prompt', 'closed_message'
            file_url TEXT,            -- URL to audio file (could be Twilio asset or external)
            file_path TEXT,           -- Local path if stored locally
            duration_seconds INTEGER,
            is_active INTEGER DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_by TEXT
        )
    """)

    # =========================================================================
    # Schedules - Business hours and holidays
    # =========================================================================
    conn.execute("""
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            timezone TEXT DEFAULT 'Australia/Sydney',
            -- Business hours as JSON: {"mon": {"open": "09:00", "close": "17:00"}, ...}
            -- null for a day means closed that day
            business_hours TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_by TEXT
        )
    """)

    # Holiday dates - separate table for flexibility
    conn.execute("""
        CREATE TABLE IF NOT EXISTS schedule_holidays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            schedule_id INTEGER NOT NULL,
            name TEXT NOT NULL,           -- "Christmas Day", "Good Friday"
            date TEXT NOT NULL,           -- "2024-12-25" for specific, or "12-25" for recurring
            is_recurring INTEGER DEFAULT 0,  -- 1 if same date every year
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT,
            FOREIGN KEY (schedule_id) REFERENCES schedules(id)
        )
    """)

    # =========================================================================
    # Queues - Ring groups with hold music
    # =========================================================================
    conn.execute("""
        CREATE TABLE IF NOT EXISTS queues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,

            -- Hold experience
            hold_music_id INTEGER,        -- FK to audio_files
            position_announcement INTEGER DEFAULT 1,  -- Announce queue position
            announcement_interval INTEGER DEFAULT 60, -- Seconds between announcements
            estimated_wait_announcement INTEGER DEFAULT 0,

            -- Ring behavior
            ring_strategy TEXT DEFAULT 'simultaneous',  -- 'simultaneous', 'round_robin', 'least_recent'
            ring_timeout INTEGER DEFAULT 30,            -- Seconds to ring before trying next/giving up
            max_queue_size INTEGER,                     -- null = unlimited
            max_wait_time INTEGER,                      -- Seconds, null = unlimited

            -- Callback option
            offer_callback INTEGER DEFAULT 0,
            callback_threshold INTEGER DEFAULT 60,  -- Offer callback after X seconds wait

            -- No answer action
            no_answer_action TEXT DEFAULT 'voicemail',  -- 'voicemail', 'message', 'overflow_queue'
            no_answer_audio_id INTEGER,    -- FK to audio_files (voicemail greeting or message)
            overflow_queue_id INTEGER,     -- FK to queues (if no_answer_action = 'overflow_queue')

            is_active INTEGER DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_by TEXT,

            FOREIGN KEY (hold_music_id) REFERENCES audio_files(id),
            FOREIGN KEY (no_answer_audio_id) REFERENCES audio_files(id),
            FOREIGN KEY (overflow_queue_id) REFERENCES queues(id)
        )
    """)

    # =========================================================================
    # Queue Members - Who's in each queue
    # =========================================================================
    conn.execute("""
        CREATE TABLE IF NOT EXISTS queue_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            queue_id INTEGER NOT NULL,
            user_email TEXT NOT NULL,     -- Staff email (links to Peter for full info)
            priority INTEGER DEFAULT 0,   -- Higher = rings first in round_robin
            is_active INTEGER DEFAULT 1,  -- Can be temporarily disabled (on break, etc.)

            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_by TEXT,

            FOREIGN KEY (queue_id) REFERENCES queues(id),
            UNIQUE(queue_id, user_email)
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_queue_members_email ON queue_members(user_email)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_queue_members_queue ON queue_members(queue_id)")

    # =========================================================================
    # User Devices - How to reach each user
    # =========================================================================
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user_devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            device_type TEXT NOT NULL,    -- 'browser', 'mobile', 'sip', 'external'
            device_name TEXT,             -- "Derek's Mobile", "Reception Desk Phone"

            -- Config depends on device_type:
            -- browser: null (identity derived from email)
            -- mobile: phone number in E.164
            -- sip: JSON with username, domain, etc.
            -- external: phone number in E.164
            device_config TEXT,

            priority INTEGER DEFAULT 0,   -- Ring order (0 = all ring together)
            ring_delay INTEGER DEFAULT 0, -- Seconds to wait before ringing this device
            is_active INTEGER DEFAULT 1,

            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_by TEXT
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_user_devices_email ON user_devices(user_email)")

    # =========================================================================
    # Call Flows - What happens when a number is called
    # =========================================================================
    conn.execute("""
        CREATE TABLE IF NOT EXISTS call_flows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,

            -- Initial greeting (optional)
            greeting_audio_id INTEGER,    -- FK to audio_files

            -- Schedule check (optional)
            schedule_id INTEGER,          -- FK to schedules

            -- What to do when OPEN
            open_action TEXT DEFAULT 'queue',  -- 'queue', 'forward', 'message'
            open_queue_id INTEGER,        -- FK to queues (if open_action = 'queue')
            open_forward_number TEXT,     -- Phone number (if open_action = 'forward')
            open_audio_id INTEGER,        -- FK to audio_files (if open_action = 'message')

            -- What to do when CLOSED
            closed_action TEXT DEFAULT 'message',  -- 'voicemail', 'message', 'forward'
            closed_audio_id INTEGER,      -- FK to audio_files
            closed_forward_number TEXT,   -- Phone number (if closed_action = 'forward')
            voicemail_email TEXT,         -- Email to send voicemail to

            is_active INTEGER DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_by TEXT,

            FOREIGN KEY (greeting_audio_id) REFERENCES audio_files(id),
            FOREIGN KEY (schedule_id) REFERENCES schedules(id),
            FOREIGN KEY (open_queue_id) REFERENCES queues(id),
            FOREIGN KEY (open_audio_id) REFERENCES audio_files(id),
            FOREIGN KEY (closed_audio_id) REFERENCES audio_files(id)
        )
    """)

    # =========================================================================
    # Link phone numbers to call flows
    # =========================================================================
    # Add call_flow_id column to phone_numbers
    conn.execute("""
        ALTER TABLE phone_numbers
        ADD COLUMN call_flow_id INTEGER REFERENCES call_flows(id)
    """)

    # =========================================================================
    # Callback Requests - Pending customer callbacks
    # =========================================================================
    conn.execute("""
        CREATE TABLE IF NOT EXISTS callback_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            queue_id INTEGER NOT NULL,
            customer_phone TEXT NOT NULL,
            customer_name TEXT,           -- If captured via IVR
            original_call_sid TEXT,       -- Twilio call SID of original call

            status TEXT DEFAULT 'pending',  -- 'pending', 'in_progress', 'completed', 'failed', 'expired'
            priority INTEGER DEFAULT 0,

            requested_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            estimated_callback_time TEXT,

            -- When callback is attempted/completed
            agent_email TEXT,             -- Who took the callback
            attempt_count INTEGER DEFAULT 0,
            last_attempt_at TEXT,
            completed_at TEXT,
            callback_call_sid TEXT,       -- Twilio call SID of callback

            notes TEXT,
            created_by TEXT,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_by TEXT,

            FOREIGN KEY (queue_id) REFERENCES queues(id)
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_callback_requests_status ON callback_requests(status)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_callback_requests_queue ON callback_requests(queue_id)")

    # =========================================================================
    # Migrate phone_assignments to queue_members
    # =========================================================================
    # Check if there's any data to migrate
    cursor = conn.execute("SELECT COUNT(*) FROM phone_assignments")
    assignment_count = cursor.fetchone()[0]

    if assignment_count > 0:
        now = datetime.utcnow().isoformat()

        # Get unique phone numbers that have assignments
        cursor = conn.execute("""
            SELECT DISTINCT pn.sid, pn.phone_number, pn.friendly_name
            FROM phone_assignments pa
            JOIN phone_numbers pn ON pa.phone_number_sid = pn.sid
        """)
        phone_numbers = cursor.fetchall()

        for pn in phone_numbers:
            phone_sid = pn[0]
            phone_number = pn[1]
            friendly_name = pn[2] or phone_number

            # Create a queue for this phone number's assignments
            cursor = conn.execute("""
                INSERT INTO queues (name, description, created_at, created_by)
                VALUES (?, ?, ?, ?)
            """, (f"{friendly_name} Queue", f"Auto-migrated from phone assignments", now, "system:migration"))
            queue_id = cursor.lastrowid

            # Create a simple call flow that uses this queue
            cursor = conn.execute("""
                INSERT INTO call_flows (name, description, open_action, open_queue_id, created_at, created_by)
                VALUES (?, ?, 'queue', ?, ?, ?)
            """, (f"{friendly_name} Flow", f"Auto-migrated from phone assignments", queue_id, now, "system:migration"))
            flow_id = cursor.lastrowid

            # Link phone number to call flow
            conn.execute("""
                UPDATE phone_numbers SET call_flow_id = ? WHERE sid = ?
            """, (flow_id, phone_sid))

            # Migrate assignments to queue members
            cursor = conn.execute("""
                SELECT staff_email, can_receive, created_at, created_by
                FROM phone_assignments
                WHERE phone_number_sid = ? AND can_receive = 1
            """, (phone_sid,))
            assignments = cursor.fetchall()

            for assignment in assignments:
                staff_email = assignment[0]
                created_at = assignment[2]
                created_by = assignment[3]

                conn.execute("""
                    INSERT OR IGNORE INTO queue_members (queue_id, user_email, created_at, created_by, updated_at, updated_by)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (queue_id, staff_email, created_at, created_by, now, "system:migration"))

                # Create browser device for each user (auto-enabled)
                conn.execute("""
                    INSERT OR IGNORE INTO user_devices (user_email, device_type, device_name, created_at, created_by, updated_at, updated_by)
                    VALUES (?, 'browser', 'Browser Softphone', ?, ?, ?, ?)
                """, (staff_email, now, "system:migration", now, "system:migration"))

    conn.commit()


def down(conn):
    # Remove call_flow_id from phone_numbers (SQLite doesn't support DROP COLUMN easily)
    # So we'd need to recreate the table - skipping for simplicity

    conn.execute("DROP TABLE IF EXISTS callback_requests")
    conn.execute("DROP TABLE IF EXISTS call_flows")
    conn.execute("DROP TABLE IF EXISTS user_devices")
    conn.execute("DROP TABLE IF EXISTS queue_members")
    conn.execute("DROP TABLE IF EXISTS queues")
    conn.execute("DROP TABLE IF EXISTS schedule_holidays")
    conn.execute("DROP TABLE IF EXISTS schedules")
    conn.execute("DROP TABLE IF EXISTS audio_files")
    conn.commit()
