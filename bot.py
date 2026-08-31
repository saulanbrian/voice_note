import asyncio
import logging
import tempfile

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

from config import TELEGRAM_BOT_TOKEN
from errors import SummarizationError, TranscriptionError
from stt import transcribe
from summarizer import summarize

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

semaphore = asyncio.Semaphore(3)


async def process_voice(
    update: Update, context: ContextTypes.DEFAULT_TYPE, status_msg
) -> None:
    message = update.message
    if not message:
        return

    async def edit_message(text: str) -> None:
        await status_msg.edit_text(text)

    async with semaphore:
        try:
            voice = message.voice or message.audio
            if not voice:
                return

            await edit_message("Processing voice message...")
            file = await context.bot.get_file(voice.file_id)

            with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
                tmp_path = await file.download_to_drive(tmp.name)

            await edit_message("Transcribing...")
            transcript = await transcribe(tmp_path)
            await message.reply_text(
                f"**Transcript:**\n\n{transcript}", parse_mode="Markdown"
            )

            await edit_message("Summarizing...")
            summary = await summarize(transcript)
            await message.reply_text(
                f"**Summary:**\n\n{summary}", parse_mode="Markdown"
            )

            await edit_message("Done!")

        except TranscriptionError as e:
            logger.error("Transcription failed: %s", e)
            await edit_message(f"Transcription failed: {e}")
        except SummarizationError as e:
            logger.error("Summarization failed: %s", e)
            await edit_message(f"Summarization failed: {e}")
        except Exception as e:
            logger.exception("Unexpected error processing voice message")
            await edit_message("Something went wrong. Please try again.")


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if not message:
        return
    status_msg = await message.reply_text("Queued for processing...")
    context.application.create_task(
        process_voice(update, context, status_msg), update=update
    )


def main() -> None:
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_voice))
    logger.info("Bot started polling")
    app.run_polling()


if __name__ == "__main__":
    main()
