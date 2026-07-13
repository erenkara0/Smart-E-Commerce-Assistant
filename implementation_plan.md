# 🚀 Implementation Plan: Mikro İhracat ve E-Ticaret İçin RAG Tabanlı Akıllı Asistan

## 📑 İçindekiler

1. Proje Özeti ve Hedefleri  
2. Sistem Mimarisi ve Kullanılacak Teknolojiler  
3. Klasör Yapısı ve Çalışma Ortamı  
4. M0: Proje Kimliği ve Teknik Planlama  
5. M1: Temel Kurulum ve Güvenlik  
6. M2: FastAPI, Scalar API ve İlk Dikey Dilim  
7. M3: Veri Hazırlığı ve Vektör Arama Altyapısı  
8. M4: RAG Mimarisi, Oturum Hafızası ve LangSmith  
9. M5: Frontend Chat Arayüzü  
10. M6: Güvenlik, Docker ve İyileştirmeler  
11. M7: Test, Dokümantasyon ve Final Hazırlığı  
12. Geliştirme Metodolojisi ve Kalite Standartları  

---

## 1. Proje Özeti ve Hedefleri

Bu projenin temel amacı, mikro ihracat ve e-ticaret süreçlerinde kullanılabilecek, mağaza verilerine dayalı cevaplar üreten RAG tabanlı bir akıllı asistan geliştirmektir.

Sistem, yalnızca dil modelinin genel bilgisine dayanmak yerine mağazaya ait ürün, stok, kargo, iade ve mikro ihracat verilerini kullanarak daha güvenilir ve bağlama uygun cevaplar üretmeyi hedefler.

Bu yaklaşım ile sistemin veri dışına çıkması, yanlış bilgi üretmesi ve kullanıcıya bağlamdan kopuk cevaplar vermesi azaltılmaya çalışılır.

---

## 2. Sistem Mimarisi ve Kullanılacak Teknolojiler

Proje, backend ve frontend taraflarının aynı repository içinde yönetildiği modern bir monorepo yapısı üzerine kuruludur.

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
- GitHub Issues
- Pull Request akışı
- Environment variables
- Docker
- Docker Compose

---

## 3. Klasör Yapısı ve Çalışma Ortamı

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
```

---

## 4. M0: Proje Kimliği ve Teknik Planlama

Bu aşamada projenin genel amacı, teknik kapsamı ve tasarım yaklaşımı belirlenir.

Bu kapsamda:

- Proje amacı tanımlanır.
- Kullanılacak teknolojiler belirlenir.
- Monorepo yaklaşımı seçilir.
- Tasarım sistemi için temel renk, font ve arayüz kararları hazırlanır.
- Proje fazları milestone yapısına bölünür.
- GitHub Projects üzerinde iş takibi planlanır.

---

## 5. M1: Temel Kurulum ve Güvenlik

Bu aşamada backend ve frontend için temel geliştirme ortamı hazırlanır.

Yapılacak işler:

- Backend için FastAPI proje iskeleti oluşturulur.
- Frontend için Next.js projesi hazırlanır.
- Kök dizinde ortak `.gitignore` dosyası oluşturulur.
- `.env.example` dosyası hazırlanır.
- Gerçek `.env` dosyasının Git takibine alınması engellenir.
- Backend ve frontend bağımlılıkları ayrı ayrı yönetilir.
- Proje klasör yapısı düzenlenir.

Bu aşamanın amacı, güvenli ve sürdürülebilir bir geliştirme ortamı oluşturmaktır.

---

## 6. M2: FastAPI, Scalar API ve İlk Dikey Dilim

Bu aşamada backend tarafında temel API yapısı oluşturulur.

Yapılan ve planlanan işler:

- FastAPI uygulaması yapılandırılır.
- Scalar API Reference entegre edilir.
- `GET /` root endpoint’i oluşturulur.
- `GET /health` sağlık kontrol endpoint’i eklenir.
- Genel API response formatı belirlenir.
- Chat request ve response şemaları oluşturulur.
- `POST /chat` endpoint’i ile ilk dikey API akışı hazırlanır.
- Hata cevapları için exception handler yapısı eklenir.

Bu aşamanın amacı, yapay zeka entegrasyonundan önce temel API akışının çalıştığını doğrulamaktır.

---

## 7. M3: Veri Hazırlığı ve Vektör Arama Altyapısı

Bu aşamada RAG sisteminde kullanılacak ürün verisinin hazırlanması ve arama altyapısının temelinin oluşturulması hedeflenir.

### Tamamlanan Geliştirmeler

- Ürün veri modeli `Product` şeması ile tanımlandı.
- Örnek ürün veri seti `products.json` dosyasında hazırlandı.
- Ürün verilerini okuyup doğrulayan `product_loader.py` servis yapısı eklendi.
- Ürün listesini API üzerinden döndüren `GET /products` endpoint’i oluşturuldu.
- Ürün kayıtlarını RAG süreçlerinde kullanılabilecek metin dokümanlarına dönüştüren `product_document_builder.py` dosyası eklendi.
- Bellek içi temel vector store servis altyapısı `vector_store_service.py` ile oluşturuldu.
- Temel ürün dokümanı araması için `GET /products/search` endpoint’i eklendi.

### Mevcut Arama Yaklaşımı

Mevcut arama yapısı henüz gerçek embedding veya ChromaDB kullanmamaktadır. Şu an ürün dokümanları bellek içinde tutulur ve basit metin eşleştirme yöntemiyle aranır.

Bu yapı ilerleyen aşamalarda şu geliştirmelere temel oluşturacaktır:

- Ürün metinlerinin embedding formatına dönüştürülmesi
- ChromaDB üzerinde vektör olarak saklanması
- Kullanıcı sorgularına göre semantic search yapılması
- Bulunan bağlamın RAG cevap üretiminde kullanılması

---

## 8. M4: RAG Mimarisi, Oturum Hafızası ve LangSmith

Bu aşamada temel ürün arama altyapısı gerçek RAG mimarisine dönüştürülecektir.

Planlanan işler:

- OpenAI API entegrasyonu yapılır.
- LangChain ile RAG zinciri oluşturulur.
- Kullanıcı sorusu embedding veya retrieval sistemiyle ilgili ürün dokümanları üzerinde aranır.
- Bulunan bağlam LLM’e kontrollü şekilde verilir.
- Modelin yalnızca verilen mağaza verisine göre cevap üretmesi sağlanır.
- SQLite ile oturum hafızası eklenir.
- Son mesajları dikkate alan sınırlı konuşma geçmişi yapısı oluşturulur.
- LangSmith ile çağrı takibi, token kullanımı, gecikme süresi ve hata izleme yapılır.

---

## 9. M5: Frontend Chat Arayüzü

Bu aşamada kullanıcıların asistanla etkileşime geçeceği frontend arayüzü geliştirilecektir.

Planlanan işler:

- Chat sayfası tasarlanır.
- Kullanıcı mesaj girişi eklenir.
- Backend `POST /chat` endpoint’i ile bağlantı kurulur.
- Loading, hata ve başarılı cevap durumları yönetilir.
- Mesaj geçmişi arayüzde gösterilir.
- Session tabanlı konuşma akışı desteklenir.
- Mobil uyumlu temel tasarım düzenlemeleri yapılır.

---

## 10. M6: Güvenlik, Docker ve İyileştirmeler

Bu aşamada sistem daha güvenli, taşınabilir ve çalıştırılabilir hale getirilecektir.

Planlanan işler:

- Prompt injection risklerine karşı temel guardrail kuralları eklenir.
- Modelin mağaza verisi dışına çıkmasını azaltacak sistem talimatları hazırlanır.
- CORS ayarları yapılandırılır.
- Eski veya gereksiz oturum verilerinin temizlenmesi için yapı oluşturulur.
- Backend için Dockerfile hazırlanır.
- Frontend için Dockerfile hazırlanır.
- Docker Compose ile backend ve frontend birlikte çalıştırılır.
- Ortam değişkenleri Docker ortamına uygun hale getirilir.

---

## 11. M7: Test, Dokümantasyon ve Final Hazırlığı

Bu aşamada proje genel olarak test edilir ve sunuma hazır hale getirilir.

Planlanan işler:

- Backend endpointleri manuel ve otomatik testlerle kontrol edilir.
- Ürün listeleme ve ürün arama akışları doğrulanır.
- Chat akışı test edilir.
- README güncellenir.
- API kullanım notları eklenir.
- Kurulum ve çalıştırma adımları netleştirilir.
- Final sunum içeriği hazırlanır.
- Projenin güçlü yönleri ve geliştirmeye açık tarafları belgelenir.

---

## 12. Geliştirme Metodolojisi ve Kalite Standartları

Proje geliştirme süreci GitHub Projects Kanban panosu üzerinden takip edilir.

Her geliştirme adımı için:

- Issue oluşturulur.
- İlgili milestone seçilir.
- Ayrı branch üzerinden geliştirme yapılır.
- Değişiklikler anlamlı commit mesajlarıyla kaydedilir.
- Pull Request açılır.
- PR açıklamasında yapılan işler ve test notları belirtilir.
- İlgili issue’lar PR açıklamasında referanslanır.

Kod kalitesi için temel prensipler:

- Her dosya tek bir sorumluluğa sahip olmalıdır.
- Endpoint dosyaları yalnızca istek alıp cevap döndürmelidir.
- İş mantığı servis katmanında tutulmalıdır.
- Veri modelleri Pydantic şemalarıyla doğrulanmalıdır.
- Gizli bilgiler repository içine eklenmemelidir.
- Geliştirme süreci küçük ama anlamlı PR’lar halinde ilerlemelidir.