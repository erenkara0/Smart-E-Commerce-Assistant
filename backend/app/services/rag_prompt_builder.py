def build_rag_prompt(
    user_message: str,
    context: str,
    conversation_history: str = "",
) -> str:
    cleaned_message = user_message.strip()
    cleaned_context = context.strip()
    cleaned_history = conversation_history.strip()

    history_section = (
        f"Önceki konuşma:\n{cleaned_history}\n\n"
        if cleaned_history
        else ""
    )

    if not cleaned_context:
        return (
            "Sen Smart E-Commerce Assistant için çalışan bir e-ticaret asistanısın.\n\n"
            f"{history_section}"
            "Kullanıcının sorusu için mağaza veri setinde ilgili bir bağlam bulunamadı.\n"
            "Kullanıcıya mevcut ürün verilerinde yeterli bilgi bulunmadığını söyle.\n"
            "Tahmin yapma, ürün uydurma ve mağaza verisi dışında bilgi verme.\n\n"
            f"Güncel kullanıcı sorusu:\n{cleaned_message}"
        )

    return (
        "Sen Smart E-Commerce Assistant için çalışan bir e-ticaret asistanısın.\n\n"
        "Görevin, yalnızca verilen mağaza bağlamını ve konuşma geçmişini "
        "kullanarak kullanıcıya cevap vermektir.\n\n"
        "Kurallar:\n"
        "- Cevabı yalnızca mağaza bağlamındaki bilgilere dayanarak üret.\n"
        "- Önceki konuşmadaki 'bu', 'bunun', 'bunlardan' gibi ifadeleri dikkate al.\n"
        "- Bağlamda olmayan ürün, fiyat, stok veya teknik özellik uydurma.\n"
        "- Kullanıcının güncel sorusuna doğrudan ve anlaşılır cevap ver.\n"
        "- Bağlam yetersizse bunu açıkça söyle.\n"
        "- Cevabı Türkçe ver.\n\n"
        f"{history_section}"
        "Mağaza bağlamı:\n"
        f"{cleaned_context}\n\n"
        "Güncel kullanıcı sorusu:\n"
        f"{cleaned_message}\n\n"
        "Cevap:"
    )