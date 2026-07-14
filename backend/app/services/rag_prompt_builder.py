def build_rag_prompt(user_message: str, context: str) -> str:
    cleaned_message = user_message.strip()
    cleaned_context = context.strip()

    if not cleaned_context:
        return (
            "Sen Smart E-Commerce Assistant için çalışan bir e-ticaret asistanısın.\n\n"
            "Kullanıcının sorusu için mağaza veri setinde ilgili bir bağlam bulunamadı.\n"
            "Kullanıcıya bu konuda mevcut ürün verilerinde yeterli bilgi bulunmadığını söyle.\n"
            "Tahmin yapma, ürün uydurma ve mağaza verisi dışında bilgi verme.\n\n"
            f"Kullanıcı sorusu:\n{cleaned_message}"
        )

    return (
        "Sen Smart E-Commerce Assistant için çalışan bir e-ticaret asistanısın.\n\n"
        "Görevin, yalnızca aşağıda verilen mağaza bağlamını kullanarak kullanıcıya cevap vermektir.\n\n"
        "Kurallar:\n"
        "- Cevabı sadece verilen mağaza bağlamına dayanarak üret.\n"
        "- Bağlamda olmayan ürün, fiyat, stok veya teknik özellik uydurma.\n"
        "- Uygun ürünleri kısa, anlaşılır ve karşılaştırmalı şekilde öner.\n"
        "- Ürün önerirken ürün adı, fiyat, stok, puan ve öne çıkan özellikleri belirt.\n"
        "- Bağlam yetersizse bunu açıkça söyle.\n"
        "- Cevabı Türkçe ver.\n\n"
        "Mağaza bağlamı:\n"
        f"{cleaned_context}\n\n"
        "Kullanıcı sorusu:\n"
        f"{cleaned_message}\n\n"
        "Cevap:"
    )