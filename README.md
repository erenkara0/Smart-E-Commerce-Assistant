# Smart E-Commerce Assistant

Smart E-Commerce Assistant, mikro ihracat ve e-ticaret süreçleri için geliştirilen RAG tabanlı akıllı asistan projesidir. Sistem, mağazaya ait yapılandırılmış verileri kullanarak kullanıcı sorularına güvenilir, bağlama dayalı ve kontrollü cevaplar üretmeyi amaçlar.

## Proje Amacı

Bu projenin temel amacı, e-ticaret mağazalarında müşteri destek süreçlerini daha verimli hale getirebilecek bir yapay zeka asistanı geliştirmektir.

Asistan, yalnızca modelin genel bilgisine dayanmak yerine mağazaya ait ürün, stok, kargo, iade ve mikro ihracat verilerini kullanarak cevap üretir. Bu yaklaşım sayesinde sistemin veri dışına çıkması, yanlış bilgi üretmesi ve kullanıcıya bağlamdan kopuk cevaplar vermesi azaltılmaya çalışılır.

## Temel Özellikler

- RAG tabanlı soru-cevap mimarisi
- Mağaza verilerine dayalı cevap üretimi
- FastAPI tabanlı backend yapısı
- Next.js tabanlı frontend arayüzü
- Scalar ile interaktif API dokümantasyonu
- Ürün veri modeli ve örnek ürün veri seti
- Ürün listeleme endpoint’i
- Ürün verilerini RAG için metin dokümanlarına dönüştürme
- Bellek içi temel vector store servis altyapısı
- Temel ürün dokümanı arama endpoint’i
- Güvenli ortam değişkeni yönetimi
- Planlanan ChromaDB, LangChain, OpenAI ve LangSmith entegrasyonları

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

### Planlanan RAG ve Gözlemlenebilirlik Araçları

- LangChain
- OpenAI API
- ChromaDB
- SQLite
- LangSmith

### DevOps ve Ortam Yönetimi

- Git / GitHub
- GitHub Projects Kanban
- Docker
- Docker Compose
- Environment variables

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
│   │   │   ├── product_document_builder.py
│   │   │   ├── product_loader.py
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
│   └── design/
│
├── .env.example
├── .gitignore
├── implementation_plan.md
└── README.md