# 🚀 Uygulama Planı (Implementation Plan): Mikro İhracat ve E-Ticaret İçin RAG Tabanlı Akıllı Asistan

## 📑 İçindekiler
1. Proje Özeti ve Hedefleri
2. Sistem Mimarisi ve Kullanılacak Teknolojiler
3. Klasör Yapısı ve Çalışma Ortamı
4. Aşama 1: Temel Kurulum, Güvenlik ve Çevre Değişkenleri
5. Aşama 2: Dikey Dilimleme, API Dokümantasyonu (Scalar) ve Güvenli Bağlantı Testi
6. Aşama 3: Veri Hazırlığı, Bölme ve Vektör Soyutlama Katmanı
7. Aşama 4: Üretim Seviyesi RAG Mimarisinin, Oturum Hafızasının ve Gözlemlenebilirliğin (LangSmith) Geliştirilmesi
8. Aşama 5: Frontend Arayüz ve Oturum Entegrasyonu
9. Aşama 6: İleri Seviye İyileştirmeler, Güvenlik ve Konteynerleştirme (Docker)
10. Geliştirme Metodolojisi, İş Takibi ve Kalite Standartları

---

### 1. Proje Özeti ve Hedefleri
Bu projenin temel amacı, e-ticaret platformlarındaki müşteri etkileşimlerini otomatize eden, halüsinasyon görmeyen ve sadece mağazaya ait spesifik verilerle doğru cevaplar üretebilen akıllı bir asistan geliştirmektir. 
Modeli sıfırdan eğitmek yerine, sektör standardı olan RAG (Retrieval-Augmented Generation) mimarisi kullanılacaktır. OpenAI modelleri, tasarlanan veri katmanları ve kalıcı oturum hafızalarıyla desteklenerek kurumsal seviyede akıllandırılacaktır.

### 2. Sistem Mimarisi ve Kullanılacak Teknolojiler
Proje, kod tabanlarının birbirinden izole yönetildiği modern bir Monorepo yapısı üzerine inşa edilmiştir.

**Backend**
* **Dil:** Python 3.11+
* **Web Framework:** FastAPI
* **API Dokümantasyon & İstemci:** Scalar (Gömülü Postman alternatifi, modern interaktif arayüz)
* **Yapay Zeka / LLM:** OpenAI API (GPT-4o)
* **RAG Orkestrasyonu:** LangChain
* **LLM Gözlemlenebilirlik (Observability):** LangSmith (LangChain ile yerleşik ve tam uyumlu takip paneli)
* **Vektör Veritabanı:** ChromaDB
* **Oturum Yönetimi:** SQLite

**Frontend**
* **Framework:** Next.js (App Router, TypeScript)
* **Stil:** Tailwind CSS

**DevOps & Dağıtım**
* **Konteynerleştirme:** Docker & Docker Compose (Tüm geliştirme ve canlı ortamı izole etmek için)

### 3. Klasör Yapısı ve Çalışma Ortamı
Proje, güvenlik duvarlarının ve çevre değişkenlerinin hassas bir şekilde ayrıştırıldığı kararlı bir monorepo hiyerarşisine sahiptir.

PROJE_ANA_DİZİNİ/
│
├── backend/
│   ├── venv/                # İzole Python sanal ortamı (Yerel geliştirme için)
│   ├── Dockerfile           # Backend uygulamasını konteynerleştiren imaj dosyası
│   ├── main.py              # FastAPI giriş noktası ve Scalar API arayüzü
│   ├── .env                 # API ve LangSmith takip anahtarları
│   └── requirements.txt     
│
├── frontend/
│   ├── Dockerfile           # Frontend uygulamasını konteynerleştiren imaj dosyası
│   ├── src/app/             
│   └── package.json         
│
├── docker-compose.yml       # Tek komutla tüm sistemi (Front+Back) ayağa kaldıran orkestrasyon dosyası
└── implementation_plan.md

4. Aşama 1: Temel Kurulum, Güvenlik ve Çevre Değişkenleri
Sanal Ortam Kurulumu: Backend klasöründe venv kurularak yerel geliştirme için izolasyon sağlanır.

Güvenlik: .gitignore dosyası ile hassas verilerin GitHub'a sızması engellenir.

Frontend Kurulumu: Next.js ve Tailwind CSS ayağa kaldırılır.

5. Aşama 2: Dikey Dilimleme, API Dokümantasyonu (Scalar) ve Güvenli Bağlantı Testi
Yapay zeka entegre edilmeden önce temel veri hattı kurulur.

Scalar Entegrasyonu: FastAPI'nin eski nesil varsayılan Swagger arayüzü devre dışı bırakılır. Yerine karanlık mod destekli, gömülü bir API Client içeren (Postman ihtiyacını ortadan kaldıran) Scalar arayüzü entegre edilir.

Bağlantı Testi: Next.js (Frontend) üzerinden FastAPI'ye atılan güvenli CORS izinli fetch istekleri doğrudan Scalar üzerinden veya tarayıcıdan test edilir.

6. Aşama 3: Veri Hazırlığı, Bölme ve Vektör Soyutlama Katmanı
Veri Toplama: Mağaza verileri (CSV) yapılandırılır.

Text Splitting: Veriler LangChain ile küçük parçalara (chunk) bölünür.

Vektörleştirme: Parçalar OpenAI Embedding ile ChromaDB üzerinde vektör formatında saklanır.

7. Aşama 4: Üretim Seviyesi RAG Mimarisinin, Oturum Hafızasının ve Gözlemlenebilirliğin (LangSmith) Geliştirilmesi
Anlamsal Arama (Semantic Search): Soru veritabanında aranır ve en benzer parçalar çekilir.

Kayan Pencere (Sliding Window Memory): SQLite ile bağlam geçmişi son 5 mesajla sınırlandırılır.

Prompt Mühendisliği: Mağaza verisi dışına çıkmama talimatları verilir.

LLM Gözlemlenebilirliği (LangSmith): LangChain zincirine yerleşik LangSmith entegrasyonu dahil edilir. Sistem çalıştırıldığı anda harcanan token sayısı (maliyet), geri çağrılan döküman kalite skoru ve yanıt süresi (latency) LangSmith web arayüzünden canlı olarak izlenir.

8. Aşama 5: Frontend Arayüz ve Oturum Entegrasyonu
Modern sohbet (Chat) arayüzü tasarlanır ve session_id bazlı durum yönetimleri (state management) ile veriler ekrana asenkron olarak basılır.

9. Aşama 6: İleri Seviye İyileştirmeler, Güvenlik ve Konteynerleştirme (Docker)
Girdi Güvenliği (Guardrails): Prompt Injection saldırılarını önleme.

Veritabanı Temizliği: Eski oturumların periyodik olarak temizlenmesi.

Konteynerleştirme (Docker-Compose): Geliştirme ortamındaki tüm bağımlılıkları sabitlemek için sistem izole Docker imajları ve docker-compose ile paketlenir.

10. Geliştirme Metodolojisi, İş Takibi ve Kalite Standartları
Tüm süreç GitHub Projects üzerinden (Kanban) ve PR (Pull Request) incelemeleriyle yürütülür.