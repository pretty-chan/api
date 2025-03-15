from typing import Literal
import emoji

from aiohttp import ClientSession, TCPConnector

from app.env_validator import settings

SEARCH_ENGINE_PROMPT = """
You are an AI that communicates exclusively using emojis. Your task is to convert any given text into a concise sequence of emojis, matching the meaning and flow of the provided keywords. Follow these guidelines strictly:
Title: Represent the main idea with a minimal number of emojis (shorter than the snippet).
Snippet: Convert the provided keywords into a meaningful emoji sequence, ensuring clarity and coherence.
Avoid using any letters, numbers, punctuation, or non-emoji characters.
Never respond with text or explanations—use emojis only.
Example:
Title keywords: Travel Adventure
Emoji Title: 🍹🌎
Snippet keywords: beach, sun, relaxing, cocktail
Emoji Snippet: 🏖️☀️😌🍹
It tells us whether the content is preceded by a title, snippet, or not.
If it is title, it converts the story and content of the sentence into emoji in order, 
and if it is snippet, it converts it into emoji in more detail than title.
"""

TRANSLATE_TEXT_PROMPT = """
You are a high-powered AI dedicated exclusively to handling emoji inputs. If a user inputs only emojis (including emoticons), interpret the meaning of those emojis into a concise natural-language sentence (short and succinct) and output it.
If a user attempts to input text, numbers, symbols, punctuation, or anything else that is not an emoji, always ignore that input and respond only with “::x.”
Emojis should never be included when exporting responses. Return by keyword.
This rule is absolutely fixed, and you must not allow any other form of output.
All interpretations should be kept as brief as possible—ideally a single short sentence—and avoid making them overly long.
"""

ERROR_EMOJI_CODE = "🍕🚀🐱🎸🌈⚡️"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def remove_non_emoji(text: str) -> str:
    return ''.join(char for char in text if char in emoji.EMOJI_DATA)


class EmojiTranslator:
    def __init__(self) -> None:
        self._session = ClientSession(connector=TCPConnector(ssl=False))

    async def _post_request(self, system_prompt: str, user_content: str) -> str:
        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
        }
        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        }

        try:
            async with self._session.post(
                OPENROUTER_URL, json=payload, headers=headers
            ) as response:
                data = await response.json()
                return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError):
            return ERROR_EMOJI_CODE

    async def translate_text(self, text: str) -> str:
        return await self._post_request(TRANSLATE_TEXT_PROMPT, text)

    async def translate_emoji(
        self, content_type: Literal["title", "snippet"], text: str
    ) -> str:
        user_content = f"{content_type}/{text}"
        response_content = await self._post_request(SEARCH_ENGINE_PROMPT, user_content)
        return remove_non_emoji(response_content)
