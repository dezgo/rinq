"""OpenAI Whisper transcription service.

Config via env var:
    OPENAI_API_KEY=sk-xxx

Used for voicemail transcription as a higher-quality alternative to
Twilio's built-in transcribeCallback (which mangles accents, names, and
numbers). Falls back to Twilio transcription if not configured.
"""

import logging
import os
from typing import Optional

import requests

logger = logging.getLogger(__name__)


class WhisperService:
    """Audio transcription using OpenAI's Whisper API."""

    API_URL = 'https://api.openai.com/v1/audio/transcriptions'
    MODEL = 'whisper-1'

    def __init__(self):
        self.api_key = os.environ.get('OPENAI_API_KEY', '')

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)

    def transcribe(self, audio_bytes: bytes, filename: str = 'audio.mp3') -> Optional[str]:
        """Transcribe audio bytes via Whisper. Returns text on success, None on failure."""
        if not self.is_configured:
            return None
        try:
            response = requests.post(
                self.API_URL,
                headers={'Authorization': f'Bearer {self.api_key}'},
                files={'file': (filename, audio_bytes, 'audio/mpeg')},
                data={'model': self.MODEL},
                timeout=60,
            )
            response.raise_for_status()
            return response.json().get('text', '').strip() or None
        except Exception as e:
            logger.warning(f"Whisper transcription failed: {e}")
            return None


_whisper_service: Optional[WhisperService] = None


def get_whisper_service() -> WhisperService:
    """Get or create the WhisperService singleton."""
    global _whisper_service
    if _whisper_service is None:
        _whisper_service = WhisperService()
    return _whisper_service
