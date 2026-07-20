# Smart E-Commerce Assistant

Smart E-Commerce Assistant, mikro ihracat ve e-ticaret süreçleri için geliştirilen RAG tabanlı akıllı asistan projesidir. Sistem, mağazaya ait yapılandırılmış verileri kullanarak kullanıcı sorularına güvenilir, bağlama dayalı ve kontrollü cevaplar üretmeyi amaçlar.

## Proje Amacı

Bu projenin temel amacı, e-ticaret mağazalarında müşteri destek süreçlerini daha verimli hale getirebilecek bir yapay zeka asistanı geliştirmektir.

Asistan, yalnızca modelin genel bilgisine dayanmak yerine mağazaya ait ürün, stok, kargo, iade ve mikro ihracat verilerini kullanarak cevap üretir. Bu yaklaşım sayesinde sistemin veri dışına çıkması, yanlış bilgi üretmesi ve kullanıcıya bağlamdan kopuk cevaplar vermesi azaltılmaya çalışılır.

## Temel Özellikler

- RAG tabanlı soru-cevap mimarisi
- Mağaza verilerine dayalı cevap üretimi
- FastAPI tabanlı backend yapısı
- Next.js tabanlı frontend proje altyapısı
- Scalar ile interaktif API dokümantasyonu
- Ürün veri modeli ve örnek ürün veri seti
- Ürün listeleme endpoint’i
- Ürün verilerini RAG için metin dokümanlarına dönüştürme
- Bellek içi temel vector store servis altyapısı
- Temel ürün dokümanı arama endpoint’i
- Güvenli ortam değişkeni yönetimi
- OpenAI API ile mağaza bağlamına dayalı RAG cevap üretimi
- SQLite tabanlı kalıcı oturum hafızası
- `session_id` ile bağlama duyarlı devam soruları
- OpenAI hata yönetimi ve kullanıcı dostu fallback cevapları
- LangSmith ile OpenAI çağrılarının trace, token kullanımı ve gecikme takibi

## Kullanılan Teknolojiler

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn
- Scalar API Reference

### Frontend

- Next.js
- TypeScript
- Tailwind CSS

### RAG, Hafıza ve Gözlemlenebilirlik Araçları

- OpenAI API
- SQLite
- LangSmith
- In-memory vector store

Planlanan sonraki entegrasyonlar:

- LangChain
- ChromaDB

### DevOps ve Ortam Yönetimi

- Git / GitHub
- GitHub Projects Kanban
- GitHub Issues
- Pull Request akışı
- Environment variables

Planlanan DevOps araçları:

- Docker
- Docker Compose

## Proje Yapısı

Proje monorepo yapısında geliştirilir.

```text
Smart-E-Commerce-Assistant/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── chat.py
│   │   │       ├── health.py
│   │   │       ├── products.py
│   │   │       └── root.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── exception_handlers.py
│   │   ├── data/
│   │   │   └── products.json
│   │   ├── schemas/
│   │   │   ├── chat.py
│   │   │   ├── product.py
│   │   │   └── response.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── conversation_context_builder.py
│   │   │   ├── openai_client.py
│   │   │   ├── product_document_builder.py
│   │   │   ├── product_loader.py
│   │   │   ├── rag_fallbacks.py
│   │   │   ├── rag_prompt_builder.py
│   │   │   ├── retrieval_context_builder.py
│   │   │   ├── session_memory_service.py
│   │   │   └── vector_store_service.py
│   │   ├── __init__.py
│   │   └── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   └── app/
│   ├── package.json
│   ├── package-lock.json
│   ├── next.config.ts
│   ├── postcss.config.mjs
│   ├── eslint.config.mjs
│   └── tsconfig.json
│
├── docs/
│   ├── brand/
│   ├── design/
│   └── testing/
│       └── m4-rag-session-validation.md
│
├── .env.example
├── .gitignore
├── implementation_plan.md
└── README.md
```

## Backend’i Çalıştırma

Backend bağımlılıklarını yüklemek ve uygulamayı başlatmak için:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend çalıştıktan sonra aşağıdaki adresler kullanılabilir:

- Scalar API dokümantasyonu: `http://127.0.0.1:8000/scalar`
- Health endpoint’i: `http://127.0.0.1:8000/health`

## Ortam Değişkenleri

Proje kökündeki `.env.example` dosyasını temel alarak yerel bir `.env` dosyası oluşturun.

Temel ortam değişkenleri:

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

LANGSMITH_TRACING=false
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=smart-e-commerce-assistant
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
```

Gerçek API anahtarları `.env.example` dosyasına veya Git repository’sine eklenmemelidir.

LangSmith takibi kullanılacaksa yerel `.env` dosyasındaki değer şu şekilde etkinleştirilmelidir:

```env
LANGSMITH_TRACING=true
```

## Temel API Endpoint’leri

- `GET /`
- `GET /health`
- `GET /products`
- `GET /products/search`
- `POST /chat`

## Chat Oturum Yönetimi

İlk chat isteğinde `session_id` gönderilmediğinde backend otomatik olarak yeni bir oturum kimliği oluşturur.

Örnek ilk istek:

```json
{
  "message": "ASUS bilgisayar önerir misin?"
}
```

Backend cevabında oluşturulan `session_id` döndürülür. Aynı sohbet içindeki devam mesajlarında bu değer tekrar gönderilmelidir.

Örnek devam isteği:

```json
{
  "message": "Bunun fiyatı nedir?",
  "session_id": "İLK_CEVAPTAN_GELEN_SESSION_ID"
}
```

Aynı `session_id` kullanıldığında sistem önceki konuşma geçmişini dikkate alır. Oturum mesajları SQLite veritabanında saklandığı için backend yeniden başlatıldığında da konuşma geçmişi korunur.

## LangSmith Gözlemlenebilirlik

LangSmith tracing etkinleştirildiğinde OpenAI çağrıları `smart-e-commerce-assistant` projesi altında izlenebilir.

LangSmith üzerinden aşağıdaki bilgiler kontrol edilebilir:

- OpenAI istek ve cevapları
- Model çalışma süresi
- Token kullanımı
- Hata ve çağrı durumu

Gerçek `LANGSMITH_API_KEY` değeri yalnızca yerel `.env` dosyasında saklanmalıdır.

## M4 Doğrulama Notları

RAG cevap üretimi, SQLite oturum hafızası ve LangSmith gözlemlenebilirlik testleri için:

[M4 RAG ve Oturum Hafızası Doğrulama Notları](docs/testing/m4-rag-session-validation.md)
