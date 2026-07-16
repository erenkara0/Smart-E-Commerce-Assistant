from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    OpenAI,
    OpenAIError,
    PermissionDeniedError,
    RateLimitError,
)

from app.core.config import settings


class OpenAIServiceError(RuntimeError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def create_openai_client() -> OpenAI:
    if not settings.openai_api_key:
        raise OpenAIServiceError(
            code="missing_api_key",
            message="OPENAI_API_KEY is not configured.",
        )

    return OpenAI(
        api_key=settings.openai_api_key,
        timeout=settings.openai_timeout_seconds,
        max_retries=settings.openai_max_retries,
    )


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
    except AuthenticationError as exc:
        raise OpenAIServiceError(
            code="authentication_error",
            message="OpenAI authentication failed.",
        ) from exc
    except PermissionDeniedError as exc:
        raise OpenAIServiceError(
            code="permission_denied",
            message="OpenAI request permission was denied.",
        ) from exc
    except RateLimitError as exc:
        raise OpenAIServiceError(
            code="rate_limit",
            message="OpenAI rate limit was exceeded.",
        ) from exc
    except APITimeoutError as exc:
        raise OpenAIServiceError(
            code="timeout",
            message="OpenAI request timed out.",
        ) from exc
    except APIConnectionError as exc:
        raise OpenAIServiceError(
            code="connection_error",
            message="OpenAI service could not be reached.",
        ) from exc
    except BadRequestError as exc:
        raise OpenAIServiceError(
            code="bad_request",
            message="OpenAI rejected the request.",
        ) from exc
    except InternalServerError as exc:
        raise OpenAIServiceError(
            code="server_error",
            message="OpenAI service returned a server error.",
        ) from exc
    except APIStatusError as exc:
        raise OpenAIServiceError(
            code="api_status_error",
            message=f"OpenAI request failed with status {exc.status_code}.",
        ) from exc
    except OpenAIError as exc:
        raise OpenAIServiceError(
            code="unknown_openai_error",
            message="An unexpected OpenAI error occurred.",
        ) from exc

    if not response.choices:
        return ""

    content = response.choices[0].message.content

    if not content:
        return ""

    return content.strip()