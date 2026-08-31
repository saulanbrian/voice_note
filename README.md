# Telegram Voice-to-Text Bot

A Telegram bot that handles voice recordings, converts them to text using Deepgram's Nova-3 speech-to-text, and generates summaries using Ollama Cloud.

## Features

- Voice message transcription (Deepgram Nova-3)
- Transcript summarization (Ollama Cloud)
- Async processing with concurrency limit (3 concurrent)
- Built-in error handling and retry logic

## Prerequisites

- Python 3.10+
- A Telegram bot token (via [@BotFather](https://t.me/BotFather))
- A Deepgram API key (free $200 credit, no card required)
- An Ollama Cloud API key (free tier)

## Installation

```bash
git clone <repo-url>
cd tgbot
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
DEEPGRAM_API_KEY=your_deepgram_api_key
OLLAMA_API_KEY=your_ollama_api_key
OLLAMA_MODEL=gpt-oss:20b
```

## Usage

```bash
python bot.py
```

Send a voice message to your bot on Telegram. It will:

1. Queue the message
2. Transcribe the audio via Deepgram
3. Reply with the transcript
4. Summarize the transcript via Ollama Cloud
5. Reply with the summary

## Architecture

```
Voice message received
  → Download .ogg file
  → Queue for processing (Semaphore limits to 3 concurrent)
  → Background task (create_task):
      1. Transcribe via Deepgram Nova-3
      2. Send transcript
      3. Summarize via Ollama Cloud
      4. Send summary
```

## Project Structure

```
tgbot/
├── bot.py              # Entry point, handlers, polling
├── config.py           # Environment variable loading
├── stt.py              # Deepgram speech-to-text
├── summarizer.py       # Ollama Cloud summarization
├── errors.py           # Custom exceptions
├── requirements.txt    # Dependencies
├── .env.example        # Environment template
└── .gitignore
```

## Cost

| Provider | Service | Free Tier |
|----------|---------|-----------|
| Deepgram | Speech-to-Text (Nova-3) | $200 credit (~45,000 minutes) |
| Ollama Cloud | Summarization (gpt-oss:20b) | Free tier, light usage |

## License

MIT
