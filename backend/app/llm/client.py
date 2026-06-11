import json
import logging
from typing import Type, TypeVar
from openai import AsyncOpenAI
from pydantic import BaseModel
from app.config import get_settings

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class LLMClient:
    def __init__(self):
        settings = get_settings()
        self._client = AsyncOpenAI(
            api_key=settings.dashscope_api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        self._model = settings.llm_model

    async def chat(self, system: str, user: str, temperature: float = 0.7, max_tokens: int = 2000) -> str:
        resp = await self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content or ""

    async def structured(self, system: str, user: str, schema: Type[T], temperature: float = 0.4, max_tokens: int = 3000) -> T:
        """Call the LLM and parse the response into schema. Retries once on parse failure."""
        schema_json = json.dumps(schema.model_json_schema(), indent=2)
        system_with_schema = (
            f"{system}\n\n"
            f"You MUST respond with a single valid JSON object that matches this schema exactly:\n"
            f"{schema_json}\n"
            f"Do not include any text outside the JSON object. Do not use markdown code blocks."
        )

        for attempt in range(2):
            raw = await self.chat(system_with_schema, user, temperature, max_tokens=max_tokens)
            try:
                # Strip markdown code blocks if model wraps response
                text = raw.strip()
                if text.startswith("```"):
                    text = text.split("```")[1]
                    if text.startswith("json"):
                        text = text[4:]
                return schema.model_validate_json(text.strip())
            except Exception as e:
                if attempt == 0:
                    logger.warning("JSON parse failed on attempt 1, retrying: %s", e)
                    user = f"{user}\n\nIMPORTANT: Your previous response could not be parsed as JSON. Return ONLY a valid JSON object."
                else:
                    logger.error("JSON parse failed after retry: %s\nRaw: %s", e, raw[:500])
                    raise ValueError(f"LLM returned invalid JSON after 2 attempts: {e}") from e

        raise RuntimeError("unreachable")


_client: LLMClient | None = None


def get_llm_client() -> LLMClient:
    global _client
    if _client is None:
        _client = LLMClient()
    return _client
