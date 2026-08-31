import logging

from ollama import AsyncClient

from config import OLLAMA_API_KEY, OLLAMA_MODEL
from errors import SummarizationError

logger = logging.getLogger(__name__)

client = AsyncClient(
    host="https://ollama.com",
    headers={"Authorization": f"Bearer {OLLAMA_API_KEY}"},
)

SYSTEM_PROMPT = (
    "You are a helpful assistant that summarizes transcripts. "
    "Provide a concise summary of the following transcript. "
    "Keep it clear and structured."
)


async def summarize(text: str) -> str:
    try:
        response = await client.chat(  # pyright: ignore
            OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            stream=False,
        )
        content = response["message"]["content"]
        if not isinstance(content, str):
            raise SummarizationError("No content returned from the model")
        return content
    except SummarizationError:
        raise
    except Exception as e:
        logger.error("Ollama summarization failed: %s", e)
        raise SummarizationError(f"Summarization failed: {e}") from e
