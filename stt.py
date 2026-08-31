import asyncio
import logging
import os
from pathlib import Path

from deepgram import AsyncDeepgramClient

from config import DEEPGRAM_API_KEY
from errors import TranscriptionError

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB

client = AsyncDeepgramClient(api_key=DEEPGRAM_API_KEY)


def _read_file(file_path: Path) -> bytes:
    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE:
        raise TranscriptionError(
            f"File too large: {file_size / 1024 / 1024:.1f} MB ",
            f"(max {MAX_FILE_SIZE / 1024 / 1024:.0f} MB)",
        )
    with open(file_path, "rb") as f:
        return f.read()


async def transcribe(file_path: Path) -> str:
    file_bytes = await asyncio.to_thread(_read_file, file_path)
    try:
        response = await client.listen.v1.media.transcribe_file(
            request=file_bytes,
            model="nova-3",
            smart_format=True,
        )
        transcript = response.results.channels[0].alternatives[0].transcript  # pyright: ignore
        if not transcript or not isinstance(transcript, str):
            raise TranscriptionError("No transcript returned")
        return transcript
    except TranscriptionError:
        raise
    except Exception as e:
        logger.error("Deepgram transcription failed: %s", e)
        raise TranscriptionError(f"Transcription failed: {e}") from e
