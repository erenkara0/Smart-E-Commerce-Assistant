def build_no_context_answer() -> str:
    return (
        "Bu soruyla ilgili mağaza veri setinde yeterli ürün bilgisi bulunamadı. "
        "Lütfen ürün adı, kategori, marka veya teknik özellik belirterek tekrar deneyin."
    )


def build_openai_config_error_answer() -> str:
    return (
        "RAG cevabı üretilemedi çünkü OpenAI API key yapılandırması eksik. "
        "Lütfen yerel .env dosyasında OPENAI_API_KEY değerinin tanımlı olduğunu kontrol edin."
    )


def build_rag_service_error_answer() -> str:
    return (
        "RAG cevabı üretilirken geçici bir servis hatası oluştu. "
        "Lütfen daha sonra tekrar deneyin."
    )


def build_empty_model_answer() -> str:
    return (
        "Modelden geçerli bir cevap alınamadı. "
        "Lütfen sorunuzu daha açık bir şekilde tekrar yazın."
    )