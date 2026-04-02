"""
Gmail service for sending call recordings to Google Group.

Uses Gmail API with service account credentials to send emails
with audio attachments to the call-recordings group.
"""

import base64
import logging
import os
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from rinq.config import config

logger = logging.getLogger(__name__)


class GmailService:
    """Service for sending emails via Gmail API."""

    SCOPES = [
        'https://www.googleapis.com/auth/gmail.send',
    ]

    def __init__(self):
        self.service = None
        self._initialize()

    def _initialize(self):
        """Initialize Gmail API credentials and service."""
        try:
            if not os.path.exists(config.google_credentials_file):
                logger.warning(
                    f"Gmail credentials not found at {config.google_credentials_file}"
                )
                return

            # Create credentials with domain-wide delegation
            credentials = service_account.Credentials.from_service_account_file(
                config.google_credentials_file,
                scopes=self.SCOPES
            )

            # Delegate credentials to admin user (required for Gmail API)
            if config.google_admin_email:
                credentials = credentials.with_subject(config.google_admin_email)

            # Build the Gmail service
            self.service = build('gmail', 'v1', credentials=credentials)
            logger.info("Gmail service initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing Gmail service: {e}")
            self.service = None

    def send_recording(self, recording_data: dict, audio_content: bytes,
                       audio_filename: str) -> dict:
        """Send a call recording to the Google Group.

        Args:
            recording_data: Dict with call metadata:
                - call_sid: Twilio call SID
                - from_number: Caller's phone number
                - to_number: Called phone number
                - duration_seconds: Recording duration
                - call_type: 'inbound', 'outbound', or 'internal'
                - staff_email: Staff member on the call
                - staff_name: Staff member's display name (optional)
            audio_content: Raw bytes of the audio file (MP3)
            audio_filename: Filename for the attachment

        Returns:
            Dict with 'success' and 'message_id' or 'error'
        """
        if not self.service:
            return {'success': False, 'error': 'Gmail service not initialized'}

        try:
            # Build email subject
            call_type = recording_data.get('call_type', 'call')
            from_number = recording_data.get('from_number', 'Unknown')
            to_number = recording_data.get('to_number', 'Unknown')
            duration = recording_data.get('duration_seconds', 0)
            staff_name = recording_data.get('staff_name', recording_data.get('staff_email', 'Staff'))

            # Format duration as M:SS
            minutes = duration // 60
            seconds = duration % 60
            duration_str = f"{minutes}:{seconds:02d}"

            if call_type == 'inbound':
                subject = f"📞 Inbound Call Recording - {from_number} → {staff_name} ({duration_str})"
            elif call_type == 'outbound':
                subject = f"📤 Outbound Call Recording - {staff_name} → {to_number} ({duration_str})"
            else:
                subject = f"📞 Call Recording - {from_number} ↔ {to_number} ({duration_str})"

            # Build email body with metadata
            body_lines = [
                f"Call Recording",
                f"",
                f"Type: {call_type.title()}",
                f"From: {from_number}",
                f"To: {to_number}",
                f"Duration: {duration_str}",
                f"Staff: {staff_name}",
                f"",
                f"Call SID: {recording_data.get('call_sid', 'N/A')}",
                f"Recording SID: {recording_data.get('recording_sid', 'N/A')}",
            ]
            body = "\n".join(body_lines)

            # Create MIME message
            message = MIMEMultipart()
            message['to'] = config.recordings_group_email
            message['from'] = config.google_admin_email
            message['subject'] = subject

            # Add text body
            message.attach(MIMEText(body, 'plain'))

            # Add audio attachment
            audio_part = MIMEAudio(audio_content, _subtype='mpeg')
            audio_part.add_header(
                'Content-Disposition',
                'attachment',
                filename=audio_filename
            )
            message.attach(audio_part)

            # Encode and send
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            result = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()

            message_id = result.get('id')
            logger.info(
                f"Recording sent to {config.recordings_group_email}, "
                f"message_id={message_id}"
            )

            return {
                'success': True,
                'message_id': message_id,
                'thread_id': result.get('threadId'),
            }

        except HttpError as e:
            logger.error(f"Gmail API error sending recording: {e}")
            return {'success': False, 'error': f'Gmail API error: {e}'}
        except Exception as e:
            logger.exception(f"Error sending recording to Gmail: {e}")
            return {'success': False, 'error': str(e)}

    def get_message_url(self, message_id: str) -> str:
        """Get a URL to view the message in Google Groups.

        Note: This is an approximation - the actual URL depends on
        how the group is configured.
        """
        # Google Groups URL format
        group_name = config.recordings_group_email.split('@')[0]
        return f"https://groups.google.com/a/watsonblinds.com.au/g/{group_name}"


# Singleton instance
gmail_service = GmailService()
