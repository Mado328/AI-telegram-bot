from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionUserMessageParam, ChatCompletionAssistantMessageParam
from config import AI_TOKEN

from openai import OpenAI
import base64


client = AsyncOpenAI(api_key=f'{AI_TOKEN}',
                base_url="https://openrouter.ai/api/v1")

# генерация ответа ИИ
async def ai_generate(text: str, role: str):
    response = await client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=[
            ChatCompletionAssistantMessageParam(role="assistant", content=role),
            ChatCompletionUserMessageParam(role="user", content=text)
        ]

    )
    return response.choices[0].message.content