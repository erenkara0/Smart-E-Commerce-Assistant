# Smart E-Commerce Assistant

Smart E-Commerce Assistant, mikro ihracat ve e-ticaret süreçleri için geliştirilen RAG tabanlı akıllı asistan projesidir. Sistem, mağazaya ait yapılandırılmış verileri kullanarak kullanıcı sorularına güvenilir, bağlama dayalı ve kontrollü cevaplar üretmeyi amaçlar.

## Proje Amacı

Bu projenin temel amacı, e-ticaret mağazalarında müşteri destek süreçlerini daha verimli hale getirebilecek bir yapay zeka asistanı geliştirmektir. Asistan, modelin genel bilgisine doğrudan dayanmak yerine mağazaya ait ürün, stok, kargo, iade ve mikro ihracat verilerini kullanarak cevap üretir.

Bu yaklaşım ile sistemin veri dışına çıkması, yanlış bilgi üretmesi ve kullanıcıya bağlamdan kopuk cevaplar vermesi azaltılmaya çalışılır.

## Temel Özellikler

* RAG tabanlı soru-cevap mimarisi
* Mağaza verilerine dayalı cevap üretimi
* FastAPI tabanlı backend yapısı
* Next.js tabanlı frontend arayüzü
* ChromaDB ile vektör veri saklama
* SQLite ile oturum hafızası
* LangSmith ile LLM gözlemlenebilirliği
* Scalar ile interaktif API dokümantasyonu
* Docker ve docker-compose ile ortam standardizasyonu
* Güvenli ortam değişkeni yönetimi

## Kullanılan Teknolojiler

### Backend

* Python
* FastAPI
* LangChain
* OpenAI API
* ChromaDB
* SQLite
* LangSmith
* Scalar API Reference

### Frontend

* Next.js
* TypeScript
* Tailwind CSS

### DevOps ve Ortam Yönetimi

* Git / GitHub
* GitHub Projects Kanban
* Docker
* Docker Compose
* Environment variables

## Proje Yapısı

Proje monorepo yapısında geliştirilir.

```text
Smart-E-Commerce-Assistant/
├── backend/
│   ├── app/
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
│   └── brand/
│
├── .env.example
├── .gitignore
├── implementation_plan.md
└── README.md
```

## Ortam Değişkenleri

Projede gizli anahtarlar ve ortam ayarları `.env` dosyası üzerinden yönetilir. Gerçek `.env` dosyası Git takibine alınmaz.

Gerekli değişkenlerin şablonu kök dizindeki `.env.example` dosyasında tanımlanmıştır.

`.env.example` dosyası; backend, frontend, OpenAI, LangSmith, ChromaDB, SQLite, RAG ayarları ve Scalar API dokümantasyonu için gerekli yapılandırma alanlarını içerir.

## Geliştirme Fazları

Proje geliştirme süreci fazlara ayrılmıştır:

| Faz | Kapsam                                                                |
| --- | --------------------------------------------------------------------- |
| M0  | Proje kimliği, teknik planlama, tasarım sistemi ve mockuplar          |
| M1  | Monorepo kurulumu, backend/frontend ortamı ve güvenlik yapılandırması |
| M2  | FastAPI, Scalar API arayüzü ve frontend-backend bağlantısı            |
| M3  | Veri hazırlığı, text splitting, embedding ve ChromaDB yapısı          |
| M4  | RAG mimarisi, oturum hafızası ve LangSmith gözlemlenebilirliği        |
| M5  | Frontend chat arayüzü ve session entegrasyonu                         |
| M6  | Guardrails, güvenlik iyileştirmeleri ve Docker yapılandırması         |
| M7  | Test, dokümantasyon ve final sunum hazırlığı                          |

## Güvenlik Notları

* Gerçek API anahtarları repository içine eklenmez.
* `.env` dosyası Git takibine alınmaz.
* `.env.example` yalnızca şablon olarak kullanılır.
* Python sanal ortamı, Next.js build çıktıları ve bağımlılık klasörleri GitHub’a gönderilmez.
* Prompt injection ve veri dışı cevap üretme riskleri guardrail kurallarıyla sınırlandırılacaktır.

## Proje Durumu

Proje geliştirme süreci GitHub Projects Kanban panosu üzerinden takip edilmektedir. Görevler milestone yapısına göre fazlara ayrılır ve her geliştirme adımı issue/branch/pull request akışıyla yönetilir.
