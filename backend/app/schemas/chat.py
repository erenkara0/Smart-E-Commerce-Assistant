from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User message sent to the assistant.",
        examples=["Laptop önerisi yapabilir misin?"],
    )
    session_id: str | None = Field(
        default=None,
        max_length=100,
        description=(
            "Existing chat session identifier. "
            "A new session identifier is generated when omitted."
        ),
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )

    @field_validator("message")
    @classmethod
    def message_must_not_be_blank(cls, value: str) -> str:
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("Message cannot be empty.")

        return cleaned_value

    @field_validator("session_id", mode="before")
    @classmethod
    def normalize_session_id(cls, value: str | None) -> str | None:
        if value is None:
            return None

        cleaned_value = value.strip()

        if not cleaned_value:
            return None

        return cleaned_value


class ChatResponseData(BaseModel):
    session_id: str = Field(
        ...,
        description="Identifier of the active chat session.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    answer: str = Field(
        ...,
        description="Assistant answer generated for the user message.",
        examples=["Elbette, sana yardımcı olabilirim."],
    )


class ChatResponse(BaseModel):
    success: bool = Field(
        ...,
        description="Indicates whether the request was processed successfully.",
    )
    message: str = Field(
        ...,
        description="Short response message.",
    )
    data: ChatResponseData = Field(
        ...,
        description="Chat response payload.",
    )