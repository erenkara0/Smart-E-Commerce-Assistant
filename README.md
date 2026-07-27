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
│   │   ├── app/
│   │   │   ├── api/
│   │   │   │   └── chat/
│   │   │   │       └── route.ts
│   │   │   ├── globals.css
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components/
│   │   │   └── chat/
│   │   │       ├── chat-header.tsx
│   │   │       ├── chat-input.tsx
│   │   │       ├── chat-interface.tsx
│   │   │       ├── chat-message-list.tsx
│   │   │       └── chat-welcome.tsx
│   │   ├── hooks/
│   │   │   └── use-chat.ts
│   │   ├── lib/
│   │   │   └── api.ts
│   │   └── types/
│   │       └── chat.ts
│   ├── .env.example
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

Backend ve Docker Compose yapılandırması için proje kökündeki örnek dosyayı kopyalayın:

```powershell
Copy-Item .env.example .env
```

Yerel frontend yapılandırması için:

```powershell
Copy-Item frontend/.env.example frontend/.env.local
```

Backend tarafından kullanılan temel değişkenler:

```env
APP_ENV=development

CORS_ALLOWED_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
CORS_ALLOW_CREDENTIALS=false

OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
OPENAI_TIMEOUT_SECONDS=30
OPENAI_MAX_RETRIES=2

RETRIEVAL_TOP_K=2
RAG_MAX_CONTEXT_CHARS=4000
VECTOR_STORE_PROVIDER=in_memory

SQLITE_DB_PATH=./backend/storage/app.db
SESSION_MEMORY_LIMIT=5

LANGSMITH_TRACING=false
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=smart-e-commerce-assistant
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
```

Frontend’in backend servisine bağlanmak için kullandığı değişken:

```env
BACKEND_API_BASE_URL=http://127.0.0.1:8000
```

Docker Compose çalıştırıldığında frontend için backend adresi otomatik olarak `http://backend:8000` şeklinde ayarlanır.

Gerçek API anahtarları `.env.example`, `frontend/.env.example` veya Git repository’sine eklenmemelidir.

LangSmith takibi kullanılacaksa yerel `.env` dosyasında aşağıdaki değişkenler ayarlanmalıdır:

```env
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_api_key
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

## M5 Frontend Sohbet Arayüzü

MikroAsistan frontend uygulaması, Next.js API proxy üzerinden FastAPI backend servisine bağlanan duyarlı bir sohbet deneyimi sunar.

### Tamamlanan Özellikler

- Mobil, tablet ve masaüstü için duyarlı sohbet arayüzü
- Önerilen soru butonları
- Kullanıcı ve asistan mesaj balonları
- `/api/chat` üzerinden backend entegrasyonu
- `session_id` kullanılarak konuşma devamlılığı
- Yüklenme ve backend hata durumları
- Yeni mesajlar için otomatik kaydırma
- Mesajları ve oturumu sıfırlayan yeni sohbet özelliği
- Enter ile mesaj gönderme
- Shift + Enter ile yeni satır oluşturma
- İçeriğe göre otomatik büyüyen mesaj kutusu
- Uzun mesajların ve bağlantıların satır içine sığdırılması
- Yeniden kullanılabilir React bileşenleri ve ortak TypeScript tipleri
- Sohbet state ve API işlemlerinin özel hook üzerinden yönetilmesi

### Frontend Doğrulama

M5 sohbet arayüzü aşağıdaki komutlarla doğrulandı:

```bash
npm run lint
npm run build
```
Tüm testler başarıyla tamamlandı. Ayrıntılı manuel test sonuçları aşağıdaki dosyada kayıt altına alındı:
```bash
/m5-chat-interface-validation.md
```

## Docker ile Çalıştırma

MikroAsistan frontend ve backend servisleri Docker Compose kullanılarak birlikte çalıştırılabilir.

### Gereksinimler

- Docker Desktop
- Docker Compose
- Proje kökünde yapılandırılmış bir `.env` dosyası

Gerçek API anahtarları ve diğer gizli bilgiler Docker imajlarına eklenmez. Bu değerler çalışma sırasında `.env` dosyasından alınır.

### Uygulamayı Başlatma

Proje kökünde aşağıdaki komutu çalıştırın:

```bash
docker compose up --build
```

Bu komut:

- FastAPI backend imajını oluşturur.
- Next.js frontend imajını oluşturur.
- Backend sağlık kontrolünü çalıştırır.
- Backend sağlıklı duruma geldikten sonra frontend servisini başlatır.
- İki servisi aynı Docker ağı üzerinden birbirine bağlar.

Uygulama başladıktan sonra aşağıdaki adreslerden erişilebilir:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- Backend sağlık kontrolü: `http://localhost:8000/health`
- Scalar API dokümantasyonu: `http://localhost:8000/scalar`

### Servis Durumlarını Kontrol Etme

```bash
docker compose ps
```

Backend servisinin durumunda `healthy` ifadesi görünmelidir.

### Logları Görüntüleme

Tüm servislerin loglarını görüntülemek için:

```bash
docker compose logs -f
```

Yalnızca belirli bir servisin loglarını görüntülemek için:

```bash
docker compose logs -f backend
docker compose logs -f frontend
```

### Uygulamayı Durdurma

```bash
docker compose down
```

Bu komut container ve ağ yapılarını kaldırır. SQLite verilerinin saklandığı Docker volume korunur.

Containerlarla birlikte kayıtlı volume verilerini de silmek için:

```bash
docker compose down -v
```

> `-v` seçeneği SQLite verilerini kalıcı olarak silebileceği için dikkatli kullanılmalıdır.

## Backend Testlerini Çalıştırma

Backend test bağımlılıklarını yüklemek için:

```bash
cd backend
python -m pip install -r requirements-dev.txt
```

Testleri çalıştırmak için:

```bash
python -m pytest
```

Testler geçici ve izole bir SQLite veritabanı kullanır; geliştirme veritabanındaki veriler değiştirilmez.

### Test Kapsamı

Mevcut backend test paketi aşağıdaki senaryoları doğrular:

- Root ve health endpoint yanıtları
- Ürün listesinin ve zorunlu ürün alanlarının doğrulanması
- Geçerli chat isteğinin başarılı yanıt üretmesi
- Boş mesaj ve eksik istek gövdesi için doğrulama hataları
- Otomatik session ID oluşturulması
- Mevcut session ID'nin yeniden kullanılması
- Takip mesajlarında konuşma geçmişinin korunması
- Ürün bağlamı bulunamadığında fallback yanıtı
- OpenAI rate limit, timeout ve bağlantı hatası fallback yanıtları
- Modelin boş cevap vermesi durumundaki fallback yanıtı

Testlerde harici OpenAI istekleri `monkeypatch` kullanılarak mock'lanır. Bu nedenle test paketi gerçek bir OpenAI API anahtarı gerektirmez ve dış servise istek göndermez.

Tam test paketi başarıyla çalıştığında mevcut sonuç:

```text
15 passed
```

## Demo Akışı

1. Uygulama Docker Compose ile başlatılır:

```powershell
docker compose up --build -d
```

2. Backend sağlık durumu kontrol edilir:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

3. Tarayıcıdan frontend açılır:

```text
http://localhost:3000
```

4. Kullanıcı aşağıdaki örnek mesajı gönderir:

```text
Oyun için uygun bir laptop önerir misin?
```

5. Asistanın mağaza veri setine bağlı ürün önerisi, fiyat, stok ve özellik bilgileri sunduğu doğrulanır.

6. Aynı sohbet içinde takip sorusu gönderilerek konuşma geçmişi test edilir:

```text
Önerdiğin ürünün stok ve fiyat bilgisi nedir?
```

7. **Yeni Sohbet** butonuyla önceki mesajların temizlendiği ve yeni bir oturum oluşturulduğu doğrulanır.

8. Demo tamamlandıktan sonra servisler durdurulur:

```powershell
docker compose down
```

## Son Doğrulama Sonuçları

- Backend test paketi: `15 passed`
- Frontend production build: başarılı
- Docker Compose backend servisi: `healthy`
- Docker Compose frontend servisi: çalışıyor
- Backend health endpoint’i: başarılı
- Frontend HTTP yanıtı: `200`
- Chat mesajlaşma akışı: başarılı
- Konuşma geçmişi: başarılı
- Yeni sohbet akışı: başarılı