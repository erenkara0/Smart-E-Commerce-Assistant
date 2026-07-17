def build_no_context_answer() -> str:
    return (
        "Bu soruyla ilgili mağaza veri setinde yeterli ürün bilgisi bulunamadı. "
        "Lütfen ürün adı, kategori, marka veya teknik özellik belirterek tekrar deneyin."
    )


def build_empty_model_answer() -> str:
    return (
        "Modelden geçerli bir cevap alınamadı. "
        "Lütfen sorunuzu daha açık bir şekilde tekrar yazın."
    )


def build_openai_error_fallback(error_code: str) -> tuple[str, str]:
    fallbacks: dict[str, tuple[str, str]] = {
        "missing_api_key": (
            "OpenAI service is not configured",
            "Yanıt servisi şu anda yapılandırma nedeniyle kullanılamıyor.",
        ),
        "authentication_error": (
            "OpenAI authentication failed",
            "Yanıt servisine şu anda erişilemiyor. Lütfen daha sonra tekrar deneyin.",
        ),
        "permission_denied": (
            "OpenAI request permission denied",
            "Yanıt servisi bu isteği şu anda işleyemiyor.",
        ),
        "rate_limit": (
            "OpenAI rate limit exceeded",
            "Yanıt servisi şu anda yoğun. Lütfen kısa bir süre sonra tekrar deneyin.",
        ),
        "timeout": (
            "OpenAI request timed out",
            "Yanıt oluşturma işlemi zaman aşımına uğradı. Lütfen tekrar deneyin.",
        ),
        "connection_error": (
            "OpenAI connection failed",
            "Yanıt servisine bağlantı kurulamadı. Lütfen daha sonra tekrar deneyin.",
        ),
        "bad_request": (
            "OpenAI request was rejected",
            "İstek yanıt servisi tarafından işlenemedi. Lütfen sorunuzu değiştirerek tekrar deneyin.",
        ),
        "server_error": (
            "OpenAI server error",
            "Yanıt servisinde geçici bir sorun oluştu. Lütfen daha sonra tekrar deneyin.",
        ),
        "api_status_error": (
            "OpenAI API status error",
            "Yanıt servisi isteği tamamlayamadı. Lütfen daha sonra tekrar deneyin.",
        ),
        "unknown_openai_error": (
            "Unexpected OpenAI error",
            "Yanıt oluşturulurken beklenmeyen bir sorun oluştu. Lütfen tekrar deneyin.",
        ),
    }

    return fallbacks.get(
        error_code,
        (
            "RAG response generation failed",
            "Yanıt oluşturulurken bir sorun oluştu. Lütfen daha sonra tekrar deneyin.",
        ),
    )