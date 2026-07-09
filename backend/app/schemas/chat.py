from pydantic import BaseModel, Field, field_validator

# API’ye boş veya aşırı uzun mesaj gelmesini engelle
class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User message sent to the assistant.",
        examples=["Laptop önerisi yapabilir misin?"],
    )

# mesajdaki boşlukları temizle
    @field_validator("message")
    @classmethod
    def message_must_not_be_blank(cls, value: str) -> str:
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("Message cannot be empty.")

        return cleaned_value

# chat endpoint’inin vereceği cevabın formatını belirle
class ChatResponseData(BaseModel):
    answer: str = Field(
        ...,
        description="Assistant answer generated for the user message.",
        examples=["Elbette, sana yardımcı olabilirim."],
    )

# chat endpoint’inin tam cevabını temsil eder
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