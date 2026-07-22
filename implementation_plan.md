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

---

## 4. M0: Proje Kimliği ve Teknik Planlama

Bu aşamada projenin genel amacı, teknik kapsamı ve tasarım yaklaşımı belirlendi.

Tamamlanan işler:

- Proje amacı tanımlandı.
- Kullanılacak teknolojiler belirlendi.
- Monorepo yaklaşımı seçildi.
- Tasarım sistemi için temel renk, font ve arayüz kararları hazırlandı.
- Proje fazları milestone yapısına bölündü.
- GitHub Projects üzerinde iş takibi planlandı.

**M0 durumu:** Tamamlandı.

---

## 5. M1: Temel Kurulum ve Güvenlik

Bu aşamada backend ve frontend için temel geliştirme ortamı hazırlandı.

Tamamlanan işler:

- Backend için FastAPI proje iskeleti oluşturuldu.
- Frontend için Next.js projesi hazırlandı.
- Kök dizinde ortak `.gitignore` dosyası oluşturuldu.
- `.env.example` dosyası hazırlandı.
- Gerçek `.env` dosyasının Git takibine alınması engellendi.
- Backend ve frontend bağımlılıkları ayrı ayrı yönetildi.
- Proje klasör yapısı düzenlendi.

Bu aşamada güvenli ve sürdürülebilir bir geliştirme ortamının temeli oluşturuldu.

**M1 durumu:** Tamamlandı.

---

## 6. M2: FastAPI, Scalar API ve İlk Dikey Dilim

Bu aşamada backend tarafında temel API yapısı oluşturuldu.

Tamamlanan işler:

- FastAPI uygulaması yapılandırıldı.
- Scalar API Reference entegre edildi.
- `GET /` root endpoint’i oluşturuldu.
- `GET /health` endpoint’i eklendi.
- Genel API response formatı belirlendi.
- Chat request ve response şemaları oluşturuldu.
- `POST /chat` endpoint’i ile ilk dikey API akışı hazırlandı.
- Hata cevapları için exception handler yapısı eklendi.

Bu aşamanın amacı, yapay zeka entegrasyonundan önce temel API akışının çalıştığını doğrulamaktır.

**M2 durumu:** Tamamlandı.

---

## 7. M3: Veri Hazırlığı ve Vektör Arama Altyapısı

Bu aşamada RAG sisteminde kullanılacak ürün verisinin hazırlanması ve arama altyapısının temelinin oluşturulması hedeflendi.

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

- Ürün metinleri için embedding vektörlerinin üretilmesi
- ChromaDB üzerinde vektör olarak saklanması
- Kullanıcı sorgularına göre semantic search yapılması

**M3 durumu:** Tamamlandı.

---

## 8. M4: RAG Mimarisi, Oturum Hafızası ve LangSmith

Bu aşamada temel ürün arama altyapısı, mağaza verilerine dayalı cevap üreten ve konuşma geçmişini koruyan bir RAG akışına dönüştürüldü.

Tamamlanan işler:

- OpenAI API entegrasyonu yapıldı.
- İlgili ürün dokümanlarını bulan retrieval context yapısı chat akışına bağlandı.
- Bulunan mağaza bağlamını kontrollü şekilde modele ileten RAG prompt yapısı oluşturuldu.
- Modelin mağaza bağlamı dışında ürün, fiyat, stok veya teknik özellik uydurma riskini azaltmayı amaçlayan prompt kuralları eklendi.
- OpenAI authentication, rate limit, timeout, bağlantı ve servis hataları için kontrollü hata yönetimi eklendi.
- Hata ve boş model cevabı durumları için kullanıcı dostu fallback mesajları oluşturuldu.
- SQLite tabanlı kalıcı oturum hafızası eklendi.
- Yeni konuşmalar için otomatik `session_id` üretimi sağlandı.
- Aynı `session_id` altında kullanıcı ve asistan mesajlarının saklanması sağlandı.
- Son mesajları dikkate alan sınırlı konuşma geçmişi RAG prompt’una eklendi.
- Önceki kullanıcı mesajları retrieval sorgusuna dahil edilerek “bunun fiyatı nedir?” gibi devam soruları desteklendi.
- Backend yeniden başlatıldığında konuşma geçmişinin SQLite üzerinden korunması sağlandı.
- LangSmith ile OpenAI çağrılarının trace, token kullanımı ve gecikme süresi takibi eklendi.
- RAG, oturum hafızası ve LangSmith doğrulama adımları
  [M4 doğrulama notlarında](docs/testing/m4-rag-session-validation.md)
  dokümante edildi.

Teknik yaklaşım:

- Mevcut M4 kapsamında özel servislerden oluşan doğrudan OpenAI tabanlı RAG akışı kullanıldı.
- Vector store sağlayıcısı olarak mevcut in-memory yapı korundu.
- LangChain ve ChromaDB entegrasyonları sonraki geliştirme aşamalarına bırakıldı.

**M4 durumu:** Tamamlandı.

---

## 9. ## M5 — Frontend Sohbet Arayüzü

**Durum:** Tamamlandı

### Tamamlanan Çalışmalar

- Next.js ile responsive sohbet arayüzü oluşturuldu.
- Frontend ile FastAPI backend arasında Next.js API proxy bağlantısı kuruldu.
- Kullanıcı ve asistan mesaj balonları eklendi.
- Önerilen soru butonları oluşturuldu.
- `session_id` ile konuşma devamlılığı sağlandı.
- Yüklenme ve backend bağlantı hata durumları eklendi.
- Yeni sohbet özelliği ile mesaj ve oturum sıfırlama işlemi gerçekleştirildi.
- Yeni mesajlar için otomatik kaydırma eklendi.
- Enter ile gönderme ve Shift + Enter ile yeni satır davranışları eklendi.
- Mesaj kutusunun içeriğe göre otomatik büyümesi sağlandı.
- Uzun mesaj ve bağlantıların taşması engellendi.
- Mobil, tablet ve masaüstü responsive düzenlemeleri tamamlandı.
- Sohbet arayüzü yeniden kullanılabilir React bileşenlerine ayrıldı.
- Sohbet state ve API işlemleri `useChat` custom hook içinde toplandı.
- Ortak TypeScript tipleri ayrı bir dosyada tanımlandı.
- Lint, production build ve manuel uçtan uca testler başarıyla tamamlandı.

### Doğrulama

Manuel test sonuçları aşağıdaki dosyada kayıt altına alındı:

`docs/m5-chat-interface-validation.md`

---

## 10. M6: Güvenlik, Docker ve İyileştirmeler

Bu aşamada sistem daha güvenli, taşınabilir ve çalıştırılabilir hale getirilecektir.

Planlanan işler:

- Prompt injection risklerine karşı temel guardrail kuralları eklenir.
- Mevcut sistem talimatları prompt injection, veri dışına çıkma ve kötü niyetli yönlendirme senaryolarına karşı güçlendirilir.
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
- README proje final durumuyla uyumlu hâle getirilir.
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