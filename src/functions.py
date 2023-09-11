from typing import Any, List, Optional

import openai
from pydantic import Field  # pylint: disable=no-name-in-module

from .schema import OpenAIFunction


async def chat_completion(text: str, context: Optional[str] = None):
    if context is not None:
        messages = [
            {"role": "user", "content": text},
            {"role": "system", "content": context},
        ]
    else:
        messages = [{"role": "user", "content": text}]
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo-16k-0613", messages=messages
    )
    return response["choices"][0]["message"]["content"]