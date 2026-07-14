from openai import OpenAI, OpenAIError

from app.core.config import settings


def create_openai_client() -> OpenAI:
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is not configured.")

    return OpenAI(api_key=settings.openai_api_key)


def generate_chat_completion(prompt: str) -> str:
    client = create_openai_client()

    try:
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful e-commerce assistant. "
                        "Answer only based on the provided store context."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
    except OpenAIError as exc:
        raise RuntimeError("OpenAI request failed.") from exc

    content = response.choices[0].message.content

    if not content:
        return "Cevap üretilemedi."

    return content