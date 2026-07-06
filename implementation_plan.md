🚀 Uygulama Planı (Implementation Plan): Mikro İhracat ve E-Ticaret İçin RAG Tabanlı Akıllı Asistan
📑 İçindekiler
1.Proje Özeti ve Hedefleri

2.Sistem Mimarisi ve Kullanılacak Teknolojiler

3.Klasör Yapısı ve Çalışma Ortamı

4.Aşama 1: Temel Kurulum, Güvenlik ve Çevre Değişkenleri

5.Aşama 2: Dikey Dilimleme ve Güvenli Bağlantı Testi

6.Aşama 3: Veri Hazırlığı, Bölme ve Vektör Soyutlama Katmanı

7.Aşama 4: Üretim Seviyesi RAG Mimarisinin ve Oturum Hafızasının Geliştirilmesi

8.Aşama 5: Frontend Arayüz ve Oturum Entegrasyonu

9.Aşama 6: İleri Seviye İyileştirmeler (Prod-Ready Güvenlik)

10.Geliştirme Metodolojisi, İş Takibi ve Kalite Standartları

1. Proje Özeti ve Hedefleri
Bu projenin temel amacı, e-ticaret platformlarındaki müşteri etkileşimlerini otomatize eden, halüsinasyon görmeyen ve sadece mağazaya ait spesifik verilerle (ürün özellikleri, kargo süreci, beden tabloları vb.) doğru cevaplar üretebilen akıllı bir asistan geliştirmektir.

Modeli sıfırdan eğitmek yerine, sektör standardı olan RAG (Retrieval-Augmented Generation) mimarisi kullanılacaktır. OpenAI modelleri, tasarlanan soyutlanmış veri katmanları ve kalıcı oturum hafızalarıyla desteklenerek kurumsal seviyede akıllandırılacaktır.

2. Sistem Mimarisi ve Kullanılacak Teknolojiler
Proje, kod tabanlarının birbirinden izole yönetildiği, bağımsız ölçeklenebilir modern bir Monorepo yapısı üzerine inşa edilmiştir.

**Backend**
Dil: Python 3.11+
Web Framework: FastAPI (Asenkron mimari, yüksek performanslı API hatları)
Sunucu: Uvicorn (ASGI web sunucusu)
Yapay Zeka / LLM: OpenAI API (GPT-4o)
RAG Orkestrasyonu: LangChain (Yalnızca döküman işleme ve zincirleme mimarisi için gevşek bağlı kullanım)
Vektör Veritabanı: ChromaDB (Bulut servislerine kolayca taşınabilir soyutlama katmanı ile)
Oturum / Hafıza Yönetimi: SQLite (Kullanıcı bazlı session_id takibi ve kalıcı mesaj geçmişi için)

**Frontend**
Framework: Next.js (App Router, TypeScript)
Stil ve Tasarım: Tailwind CSS
Veri Çekme: Modern fetch API (Asenkron durum yönetimi)

3. Klasör Yapısı ve Çalışma Ortamı
Proje, güvenlik duvarlarının ve çevre değişkenlerinin hassas bir şekilde ayrıştırıldığı kararlı bir monorepo hiyerarşisine sahiptir.

Plaintext
PROJE_ANA_DİZİNİ/
│
├── backend/
│   ├── venv/                # İzole Python sanal ortamı
│   ├── main.py              # FastAPI giriş noktası ve rota tanımları
│   ├── database.py          # SQLite oturum ve hafıza veritabanı bağlantısı
│   ├── requirements.txt     # Python bağımlılık listesi
│   ├── .env                 # Gizli API anahtarları (Yerel ortam)
│   ├── .env.example         # Çevre değişkenleri şablonu (GitHub için)
│   └── .gitignore           # Sanal ortam, şifre ve cache dosyalarını gizleyen kurallar
│
├── frontend/
│   ├── src/app/             # Next.js arayüz bileşenleri ve sayfaları
│   ├── package.json         # Node.js bağımlılıkları
│   └── (Next.js sistem dosyaları)
│
└── implementation_plan.md   # Proje yol haritası ve mimari döküman
4. Aşama 1: Temel Kurulum, Güvenlik ve Çevre Değişkenleri
Bu aşama, uygulamanın iskeletini kurmayı ve kritik güvenlik katmanlarını devreye almayı hedefler.

Sanal Ortam Kurulumu: Backend klasöründe venv kurularak Python kütüphaneleri küresel sistemden tamamen izole edilir.

Güvenlik Duvarı Konfigürasyonu: Backend içerisine .gitignore eklenerek venv, __pycache__ ve .env dosyalarının GitHub reposuna sızması kesin olarak engellenir.

Çevre Değişkenleri (.env) Yönetimi: OpenAI API anahtarı ve sistem şifreleri için .env dosyası oluşturulur. Takım çalışması ve canlı ortam dağıtımları için hassas bilgi içermeyen .env.example şablonu hazırlanıp repoya eklenir.

Frontend Kurulumu: Next.js, create-next-app komutu ile TypeScript ve Tailwind destekli olarak ana dizinde ayağa kaldırılır.

İlk Kararlı Commit: Yapı sorunsuzca chore: setup pristine backend and frontend monorepo with strict env security mesajıyla GitHub'a gönderilir.

5. Aşama 2: Dikey Dilimleme ve Güvenli Bağlantı Testi
Sisteme yapay zeka entegre edilmeden önce, iki katmanın canlı ortamda hatasız haberleştiği doğrulanmalıdır.

İlk API Endpoint'i: main.py içerisinde sistem sağlığını test eden (Health Check) ve JSON yanıtı döndüren kararlı bir GET metodu yazılır.

CORS Güvenlik Duvarı Yapılandırması: Next.js (port 3000) ve FastAPI (port 8000) farklı kökenlerde çalıştığı için tarayıcı engellemelerini önlemek adına FastAPI tarafında CORSMiddleware yapılandırılır. İzin verilen kökenler (Origins) listesi .env üzerinden dinamik olarak yönetilir.

Next.js Fetch İsteği: Frontend'deki ana sayfadan (page.tsx) asenkron olarak FastAPI sunucusuna güvenli bir fetch isteği atılır ve dönen veri ekranda listelenerek veri hattı (data pipeline) doğrulanır.

6. Aşama 3: Veri Hazırlığı, Bölme ve Vektör Soyutlama Katmanı
E-ticaret asistanının mağaza verilerini tanıma, işleme ve bulut sistemlerine hazır hale getirme aşamasıdır.

Yapılandırılmış Veri Toplama: Mağazaya ait ürün özellikleri, kargo politikaları ve sıkça sorulan sorular net bir CSV dosyası haline getirilir.

Metin Bölümleme (Text Splitting): LangChain'in RecursiveCharacterTextSplitter bileşeni kullanılarak veriler anlamsal bütünlüğü korunacak şekilde mantıksal küçük parçalara (chunk) ayrıştırılır.

Vektör Soyutlama Katmanı (Abstraction Layer): Kod doğrudan ChromaDB kütüphanesine bağımlı yazılmaz. Gelecekte Pinecone veya Supabase (pgvector) gibi bulut tabanlı bir sisteme sıfır kod değişimiyle geçebilmek için bir arayüz (Interface) tasarlanır. Bölünen metinler OpenAI Embedding modelleri ile matematiksel vektörlere dönüştürülerek yerelde ChromaDB üzerinde saklanır.

7. Aşama 4: Üretim Seviyesi RAG Mimarisinin ve Oturum Hafızasının Geliştirilmesi
Sistemin yapay zeka beyninin kurgulandığı, RAM kaybı risklerinin önlendiği ve maliyet optimizasyonunun yapıldığı en kritik aşamadır.

Anlamsal Arama (Semantic Search): Kullanıcıdan gelen soru, vektör soyutlama katmanı aracılığıyla veritabanında sorgulanır ve en yüksek benzerliğe sahip ilk 3 veri parçası çekilir.

Kalıcı Hafıza ve Kayan Pencere (Sliding Window Memory): Mesaj geçmişi sunucu RAM'inde tutulmaz (RAM sıfırlanma riski engellenir). SQLite üzerinde kullanıcıya özel session_id bazlı bir tablo kurulur. Maliyetleri (Token) kontrol altında tutmak ve LLM bağlam sınırını aşmamak için, geçmiş mesajlar "Kayan Pencere" mantığıyla okunur; modele geçmişin tamamı değil, sadece en güncel 5 mesajlaşma gönderilir.

Prompt Mühendisliği (System Prompt): Bulunan veri, kayan pencere kuralıyla filtrelenmiş geçmiş ve güncel soru birleştirilerek OpenAI API'ye şu talimatla gönderilir: "Sen kurumsal bir e-ticaret asistanısın. Müşterinin sorusunu sağlanan mağaza verisi sınırları dışına çıkmadan kesinlikle halüsinasyon görmeden yanıtla.".

8. Aşama 5: Frontend Arayüz ve Oturum Entegrasyonu
Kullanıcı deneyiminin kararlı durum yönetimleri ile (State Management) tamamlandığı aşamadır.

Sohbet Arayüzü Tasarımı: Next.js ve Tailwind CSS kullanılarak modern, responsive, kurumsal kimliğe uygun bir sohbet arayüzü (Chat UI) geliştirilir.

Oturum Yönetimi ve API Entegrasyonu: Tarayıcı tarafında kullanıcı için benzersiz bir session_id üretilir. Kullanıcının yazdığı sorular Frontend'den Backend'e bu session_id bilgisiyle birlikte POST metodu üzerinden iletilir. Backend'den dönen asenkron RAG yanıtları Next.js durum yönetiminde (useState) işlenerek ekrana basılır.

9. Aşama 6: İleri Seviye İyileştirmeler (Prod-Ready Güvenlik ve Optimizasyon)
Temel sistem kusursuz çalıştıktan sonra devreye alınacak kurumsal koruma ve bakım katmanlarıdır.

Girdi Güvenliği (Guardrails): Sisteme yönelik "Prompt Injection" (Sistemi manipüle etme amaçlı girdi) saldırılarını engellemek ve botun mağaza dışı konularla (Örn: "Bana kod yaz") meşgul edilmesini önlemek amacıyla girdi filtreleme katmanı eklenmesi.

Veritabanı Temizliği (Database Cleanup): SQLite veritabanının diskte şişmesini engellemek amacıyla, e-ticaret senaryosunda artık bağlamı kalmayan "30 günden eski" oturum (session) verilerini otomatik/manuel silecek bir bakım fonksiyonu eklenmesi.

Agentic RAG (Canlı Veri Entegrasyonu): Asistanın statik CSV verileriyle sınırlı kalmaması adına, anlık stok takibi ve dinamik fiyat kontrolleri için canlı e-ticaret API'lerine güvenli sorgular atabileceği işlevsel fonksiyonların sisteme bağlanması.

10. Geliştirme Metodolojisi, İş Takibi ve Kalite Standartları
Bu proje tamamen endüstriyel Agile (Çevik) prensiplere ve Git Workflow standartlarına uygun olarak yürütülecektir.

Kanban Panosu: GitHub Projects üzerinde "To Do", "In Progress", "Review" ve "Done" sütunları kurgulanacaktır. Geliştirilecek her madde birer "Issue" olarak açılıp bu panoda anlık takip edilecektir.

Dallanma Stratejisi (Feature Branching): Ana üretim hattını (main) korumak adına tüm geliştirmeler izole dallarda yapılacaktır (Örn: feat/secure-env-setup, feat/session-database-memory).

Anlamlı Commit Standartları (Conventional Commits): Yapılan her geliştirme türüne göre etiketlenecektir; feat: (yeni özellik), chore: (altyapı/kurulum), fix: (hata çözümü), docs: (dokümantasyon).

Pull Request (PR) ve Kod İncelemesi: Geliştirilen dallar doğrudan main ile birleştirilmeyecektir. İş tamamlandığında bir PR açılacak, ilgili Issue sistem tarafından otomatik kapatılması için bağlanacak (Örn: closes #1) ve kod mimari kontrolden geçtikten sonra ana sisteme dahil edilecektir.