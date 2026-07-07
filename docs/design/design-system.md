# MikroAsistan — Tasarım Sistemi

Kaynak: `implementation_plan.md` — Frontend Arayüz ve Oturum Entegrasyonu, RAG Mimarisi, LangSmith Gözlemlenebilirliği ve Scalar API Dokümantasyonu bölümleri. Renk paleti ayrı belgede tanımlanır: `docs/brand/palette.md`.

Bu belge, **Mikro İhracat ve E-Ticaret İçin RAG Tabanlı Akıllı Asistan** projesinde kullanılacak tipografi, spacing, köşe yarıçapı, gölge, bileşen davranışları ve genel arayüz kurallarını tanımlar.

Tasarım sistemi; web arayüzü, sohbet ekranı, gözlemlenebilirlik paneli, API dokümantasyon arayüzü ve sunum/mockup tasarımlarında ortak görsel dili korumak için kullanılır.

Tüm tasarım değerleri merkezi token yapısı üzerinden yönetilmelidir. Bileşenlerde sabit, rastgele veya hardcoded değerler kullanılmamalıdır. Görsel dilde değişiklik gerektiğinde önce tasarım sistemi ve ilgili token tanımları güncellenmelidir.

---

## 1. Tasarım İlkeleri

MikroAsistan arayüzü aşağıdaki temel ilkeler üzerine kuruludur:

| İlke             | Açıklama                                                                                                |
| ---------------- | ------------------------------------------------------------------------------------------------------- |
| Güvenilirlik     | Sistem, mağaza verilerine dayalı cevap ürettiğini kullanıcıya açıkça hissettirmelidir.                  |
| Sadelik          | Kullanıcı, asistanla hızlı ve dikkat dağılmadan iletişim kurabilmelidir.                                |
| Teknik Şeffaflık | RAG süreci, kaynaklar, token kullanımı ve latency gibi bilgiler geliştirici panelinde net görünmelidir. |
| Tutarlılık       | Chat, dashboard, API arayüzü ve mockuplar aynı renk, tipografi ve spacing sistemini kullanmalıdır.      |
| Erişilebilirlik  | Metin kontrastı, buton boyutları ve durum renkleri okunabilir ve anlaşılır olmalıdır.                   |

---

## 2. Tipografi

### 2.1 Font Aileleri

| Kullanım                      | Font                            | Token                         |
| ----------------------------- | ------------------------------- | ----------------------------- |
| Ana font                      | Inter                           | `typography.fontFamily.base`  |
| Teknik veri / JSON / endpoint | JetBrains Mono veya Roboto Mono | `typography.fontFamily.mono`  |
| Marka wordmark                | Inter / modern sans-serif       | `typography.fontFamily.brand` |

Inter, başlıklar ve gövde metni dahil tüm arayüz metinlerinde ana font olarak kullanılır.

Endpoint, JSON örnekleri, session ID, token değerleri, dosya adları, latency değerleri ve teknik metriklerde monospace font tercih edilir. Bu sayede teknik değerler daha okunabilir ve hizalı görünür.

Marka wordmark’ı sade, modern ve okunabilir bir sans-serif karaktere sahip olmalıdır. Aşırı dekoratif font kullanılmaz.

---

### 2.2 Font Ağırlıkları

| Ağırlık  | Değer | Token                            | Kullanım                          |
| -------- | ----: | -------------------------------- | --------------------------------- |
| Regular  |   400 | `typography.fontWeight.regular`  | Gövde metni, açıklamalar          |
| Medium   |   500 | `typography.fontWeight.medium`   | Menü öğeleri, butonlar, etiketler |
| Semibold |   600 | `typography.fontWeight.semibold` | Kart başlıkları, panel başlıkları |
| Bold     |   700 | `typography.fontWeight.bold`     | Ana başlıklar, marka vurgusu      |

Başlıklarda 600 veya 700 ağırlık kullanılmalıdır. Gövde metinlerinde 400 veya 500 yeterlidir. Gereksiz kalın yazı kullanımından kaçınılmalıdır.

---

### 2.3 Font Boyut Ölçeği

Ölçek: 12 / 14 / 16 / 18 / 20 / 24 / 32 px

| Token                     | px | Tipik Kullanım                                   |
| ------------------------- | -: | ------------------------------------------------ |
| `typography.fontSize.xs`  | 12 | Yardımcı metin, zaman bilgisi, chip, küçük rozet |
| `typography.fontSize.sm`  | 14 | Menü öğeleri, form etiketi, ikincil metin        |
| `typography.fontSize.md`  | 16 | Gövde metni, chat mesajları                      |
| `typography.fontSize.lg`  | 18 | Kart başlıkları, önemli açıklamalar              |
| `typography.fontSize.xl`  | 20 | Panel başlığı, modal başlığı                     |
| `typography.fontSize.2xl` | 24 | Sayfa başlığı                                    |
| `typography.fontSize.3xl` | 32 | Sunum/mockup başlığı, hero başlık                |

Chat mesajları için temel font boyutu 16 px olmalıdır. Dashboard kartlarında metrik değerleri 24–32 px aralığında kullanılabilir.

---

### 2.4 Satır Yüksekliği

| Token                           | Değer | Kullanım                    |
| ------------------------------- | ----: | --------------------------- |
| `typography.lineHeight.tight`   |   1.2 | Büyük başlıklar             |
| `typography.lineHeight.normal`  |   1.5 | Gövde metni, chat mesajları |
| `typography.lineHeight.relaxed` |   1.7 | Uzun açıklama metinleri     |

Chat cevaplarında okunabilirlik için `normal` satır yüksekliği kullanılmalıdır. Uzun RAG açıklamaları sıkışık gösterilmemelidir.

---

## 3. Spacing

Spacing skalası: 4 / 8 / 12 / 16 / 24 / 32 / 48 px

Tüm padding, margin ve gap değerleri bu skalaya oturmalıdır. Ara değerler kullanılmamalıdır.

| Token         | px | Tipik Kullanım                                 |
| ------------- | -: | ---------------------------------------------- |
| `spacing.xs`  |  4 | İkon-metin arası, küçük rozet iç boşluğu       |
| `spacing.sm`  |  8 | Küçük bileşen iç boşluğu                       |
| `spacing.md`  | 12 | Chat mesaj iç padding’i, form elemanları arası |
| `spacing.lg`  | 16 | Kart iç padding’i, sidebar menü öğeleri        |
| `spacing.xl`  | 24 | Kartlar arası boşluk, ana bölüm ayrımı         |
| `spacing.2xl` | 32 | Sayfa kenar boşluğu, büyük panel boşluğu       |
| `spacing.3xl` | 48 | Hero alanı, sunum/mockup bölüm ayrımı          |

---

## 4. Köşe Yarıçapı

MikroAsistan arayüzünde yuvarlatılmış köşeler, modern ve kullanıcı dostu görünüm için kullanılır. Ancak aşırı yuvarlak, oyuncak hissi veren formlardan kaçınılmalıdır.

| Token         |  px | Kullanım                                 |
| ------------- | --: | ---------------------------------------- |
| `radius.xs`   |   4 | Küçük chip, teknik rozet                 |
| `radius.sm`   |   6 | Input, küçük buton                       |
| `radius.md`   |   8 | Standart buton, tablo satırı, küçük kart |
| `radius.lg`   |  12 | Chat mesaj balonu, dashboard kartı       |
| `radius.xl`   |  16 | Modal, büyük panel                       |
| `radius.2xl`  |  24 | App icon, büyük mockup kartları          |
| `radius.full` | 999 | Avatar, status dot, pill badge           |

### Kullanım Kuralları

Kartlar ve dashboard panelleri için varsayılan köşe yarıçapı 12 px olmalıdır.

Chat mesaj balonlarında 12–16 px arası köşe yarıçapı kullanılabilir.

App icon ve büyük marka sunum kartlarında 24 px köşe yarıçapı tercih edilir.

Status pill ve badge bileşenlerinde tam yuvarlak yapı kullanılabilir.

---

## 5. Gölge Sistemi

MikroAsistan arayüzünde derinlik, öncelikle border ve hafif gölge ile verilmelidir. Ağır, koyu ve çok katmanlı gölgeler kullanılmamalıdır.

| Token        | Değer                | Kullanım                              |
| ------------ | -------------------- | ------------------------------------- |
| `shadows.xs` | Hafif kenar vurgusu  | Input, küçük chip                     |
| `shadows.sm` | Hafif kart gölgesi   | Kart, kaynak kutusu, küçük modal      |
| `shadows.md` | Orta seviye gölge    | Dashboard paneli, dropdown            |
| `shadows.lg` | Sunum/mockup gölgesi | Büyük cihaz mockup’ı, app icon sunumu |

### Kullanım Kuralları

Standart arayüz kartlarında `shadows.sm` yeterlidir.

Dashboard ve gözlemlenebilirlik panellerinde gölge çok hafif tutulmalıdır.

Mockup görsellerinde cihaz ve app icon sunumlarında daha belirgin ama yumuşak gölge kullanılabilir.

---

## 6. Border ve Yüzey Kuralları

| Kullanım          | Renk / Token         | Açıklama                   |
| ----------------- | -------------------- | -------------------------- |
| Standart kenarlık | `colors.border`      | Kart, input, tablo sınırı  |
| Hafif yüzey       | `colors.surface`     | Kart ve panel zeminleri    |
| Sayfa zemini      | `colors.background`  | Genel uygulama arka planı  |
| Vurgulu yüzey     | `colors.surfaceSoft` | Kaynak kutusu, bilgi alanı |

Kartlar genellikle beyaz yüzey üzerinde, açık gri border ve hafif gölge ile ayrılmalıdır.

Bir ekranda çok fazla çizgi ve border kullanılmamalı; bileşenler spacing ve yüzey farkıyla ayrıştırılmalıdır.

---

## 7. Layout Sistemi

### 7.1 Web Uygulama Yerleşimi

Web arayüzünde temel yapı üç ana alandan oluşur:

| Alan        | Açıklama                                                       |
| ----------- | -------------------------------------------------------------- |
| Sol Sidebar | Navigasyon, oturumlar, dokümanlar, ayarlar                     |
| Ana İçerik  | Chat ekranı, dashboard veya API içeriği                        |
| Sağ Panel   | Kaynaklar, oturum bilgisi, retrieved context, metrik detayları |

### 7.2 Sayfa Genişliği

| Kullanım                        |        Değer |
| ------------------------------- | -----------: |
| Minimum desteklenen genişlik    |      1280 px |
| İdeal masaüstü mockup genişliği |      1440 px |
| Ana içerik maksimum genişliği   | 1200–1320 px |
| Sidebar genişliği               |   240–280 px |
| Sağ panel genişliği             |   320–380 px |

### 7.3 Responsive Davranış

Mobil ve dar ekranlarda:

* Sidebar gizlenebilir veya drawer yapısına dönüşebilir.
* Sağ panel, ana içeriğin altına taşınabilir.
* Chat ekranı tam genişlik kullanılmalıdır.
* Kaynaklar ayrı bir sekme veya açılır panel içinde gösterilebilir.
* Alt navigasyon mobilde kullanılabilir.

---

## 8. Chat Arayüzü Kuralları

MikroAsistan’ın ana kullanıcı deneyimi sohbet ekranıdır. Bu nedenle chat arayüzü net, güvenilir ve sade olmalıdır.

### 8.1 Mesaj Tipleri

| Mesaj Tipi             | Görünüm                 | Kullanım                            |
| ---------------------- | ----------------------- | ----------------------------------- |
| Kullanıcı mesajı       | Primary mavi balon      | Kullanıcının sorduğu soru           |
| Asistan cevabı         | Beyaz kart / açık yüzey | Mağaza verisine dayalı cevap        |
| Sistem mesajı          | Açık mavi bilgi alanı   | Oturum, bağlantı veya işlem bilgisi |
| Hata mesajı            | Açık kırmızı yüzey      | API, bağlantı veya güvenlik hatası  |
| Veri bulunamadı mesajı | Açık amber yüzey        | Kaynakta bilgi bulunamadığında      |

### 8.2 Kullanıcı Mesajı

Kullanıcı mesajları sağ hizalı ve primary mavi renkte olmalıdır.

Metin beyaz olmalı, kontrast korunmalıdır.

Mesaj balonu içerisinde zaman bilgisi küçük boyutta gösterilebilir.

### 8.3 Asistan Cevabı

Asistan cevapları sol hizalı, beyaz yüzeyli kart olarak gösterilmelidir.

Cevap altında küçük bir doğrulama satırı bulunmalıdır:

“Yanıt mağaza verilerine göre üretildi.”

Bu satırda success rengi ve küçük onay ikonu kullanılabilir.

### 8.4 Kaynak Gösterimi

RAG cevabında kullanılan kaynaklar ayrı bir kaynak kartında gösterilmelidir.

Kaynak kartında şu bilgiler bulunabilir:

| Alan           | Açıklama                            |
| -------------- | ----------------------------------- |
| Dosya adı      | Örn. `returns_policy.csv`           |
| Kaynak başlığı | Örn. “İade ve Değişim Politikaları” |
| Alaka skoru    | Örn. `%92`                          |
| Kaynak türü    | CSV, PDF, doküman, ürün verisi      |

Kaynak gösterimi kullanıcıyı boğmayacak şekilde sade tutulmalıdır. Teknik detaylar geliştirici panelinde daha ayrıntılı gösterilebilir.

---

## 9. Buton Kuralları

### 9.1 Buton Tipleri

| Tip              | Kullanım                          |
| ---------------- | --------------------------------- |
| Primary Button   | Ana işlem: gönder, yükle, başlat  |
| Secondary Button | İkincil işlem: filtrele, düzenle  |
| Ghost Button     | Hafif aksiyon: kopyala, görüntüle |
| Danger Button    | Silme, engelleme, kritik işlem    |

### 9.2 Primary Button

Primary buton yalnızca ekrandaki ana aksiyon için kullanılmalıdır.

Örnek kullanımlar:

* “Gönder”
* “Yeni Sohbet”
* “Doküman Yükle”
* “İsteği Çalıştır”

Bir ekranda çok fazla primary buton kullanılmamalıdır.

### 9.3 Buton Boyutları

| Boyut  | Yükseklik | Kullanım                                |
| ------ | --------: | --------------------------------------- |
| Small  |     32 px | Tablo aksiyonları, küçük kart içi buton |
| Medium |     40 px | Standart buton                          |
| Large  |     48 px | Ana aksiyon, mobil buton                |

Mobilde dokunulabilir alan en az 44 px olmalıdır.

---

## 10. Input ve Form Kuralları

Input alanları sade, okunabilir ve yeterli yüksekliğe sahip olmalıdır.

| Eleman          | Kural                                       |
| --------------- | ------------------------------------------- |
| Text input      | 40–48 px yükseklik                          |
| Chat input      | Minimum 48 px, geniş metinlerde büyüyebilir |
| Placeholder     | Text secondary rengi                        |
| Focus durumu    | Primary mavi border veya hafif mavi glow    |
| Error durumu    | Danger border ve açıklama metni             |
| Disabled durumu | Düşük kontrastlı yüzey ve pasif metin       |

Chat input alanında placeholder olarak “Sorunuzu yazın...” kullanılabilir.

---

## 11. Badge, Chip ve Status Kuralları

### 11.1 Genel Status Renkleri

| Durum   | Renk    | Kullanım                        |
| ------- | ------- | ------------------------------- |
| Success | Yeşil   | Başarılı işlem, sağlıklı sistem |
| Warning | Amber   | Düşük güven, eksik bağlam       |
| Danger  | Kırmızı | Hata, engellenen istek          |
| Info    | Mavi    | Bilgilendirme, aktif işlem      |
| Neutral | Gri     | Pasif veya tamamlanmış durum    |

### 11.2 RAG Durum Chipleri

| Durum                  | Renk         | Kullanım                      |
| ---------------------- | ------------ | ----------------------------- |
| `QUESTION_RECEIVED`    | Mavi         | Soru alındı                   |
| `RETRIEVING`           | Cyan         | Vektör araması yapılıyor      |
| `CONTEXT_FOUND`        | Yeşil        | İlgili bağlam bulundu         |
| `LOW_CONFIDENCE`       | Amber        | Bağlam zayıf                  |
| `NO_CONTEXT`           | Amber koyu   | Uygun veri bulunamadı         |
| `ANSWER_GENERATED`     | Mavi         | Yanıt üretildi                |
| `BLOCKED_BY_GUARDRAIL` | Kırmızı      | Güvenlik kuralı devreye girdi |
| `SYSTEM_ERROR`         | Kırmızı koyu | Sistem hatası                 |

Durum renkleri dekoratif amaçla kullanılmamalıdır. Her renk gerçek bir sistem durumunu temsil etmelidir.

---

## 12. Dashboard ve Gözlemlenebilirlik Kuralları

Gözlemlenebilirlik paneli; LangSmith veya benzeri gözlem araçlarından gelen metriklerin kullanıcıya anlaşılır şekilde gösterildiği alandır.

### 12.1 KPI Kartları

KPI kartları üst bölümde yatay olarak sıralanmalıdır.

Önerilen KPI’lar:

| Metrik                  | Açıklama                                          |
| ----------------------- | ------------------------------------------------- |
| Toplam İstek            | Belirli zaman aralığındaki toplam API/chat isteği |
| Ortalama Latency        | Ortalama yanıt süresi                             |
| Token Kullanımı         | Toplam prompt + completion token                  |
| Tahmini Maliyet         | Token kullanımına göre yaklaşık maliyet           |
| Retrieval Başarı Oranı  | Kaynak bulma başarısı                             |
| Guardrail Engellemeleri | Güvenlik nedeniyle engellenen istekler            |

### 12.2 Grafik Kullanımı

| Grafik Türü  | Kullanım                          |
| ------------ | --------------------------------- |
| Line Chart   | Günlük istek ve token trendleri   |
| Bar Chart    | Latency dağılımı                  |
| Donut Chart  | Retrieved doküman kalitesi        |
| Table        | Canlı izler, session detayları    |
| Progress Bar | Kaynak kullanım ve alaka oranları |

Grafiklerde renk sayısı sınırlı tutulmalı, anlamlı durum renkleri kullanılmalıdır.

### 12.3 Uyarı Paneli

Uyarılar, kullanıcıyı yormayacak şekilde sağ panelde veya ayrı kartta gösterilmelidir.

Örnek uyarılar:

* Latency eşiği aşıldı
* Düşük güvenli yanıt üretildi
* Retrieval başarı oranı düştü
* Token maliyeti arttı
* Guardrail engellemesi gerçekleşti

---

## 13. Scalar API Arayüzü Kuralları

Scalar API arayüzü, geliştirici deneyimini temsil eder. Görsel dil, ana uygulamayla tutarlı olmalıdır.

### 13.1 API Sayfası Yapısı

| Alan                     | Açıklama                                      |
| ------------------------ | --------------------------------------------- |
| Sol Endpoint Menüsü      | API grupları ve endpoint listesi              |
| Orta Dokümantasyon Alanı | Endpoint açıklaması, şema, örnekler           |
| Sağ API İstemcisi        | Request body, authorization, response preview |

### 13.2 HTTP Method Renkleri

| Method      | Renk    | Kullanım                        |
| ----------- | ------- | ------------------------------- |
| GET         | Yeşil   | Veri okuma                      |
| POST        | Mavi    | Veri oluşturma / işlem başlatma |
| PUT / PATCH | Amber   | Güncelleme                      |
| DELETE      | Kırmızı | Silme                           |

### 13.3 Teknik Metinler

Endpoint, JSON, token ve session ID gibi değerler monospace fontla gösterilmelidir.

Teknik panellerde koyu kod alanı kullanılabilir, ancak sayfanın genel arayüzü açık tema ile uyumlu kalmalıdır.

---

## 14. Modal ve Dialog Kuralları

Modal pencereler yalnızca kullanıcının dikkatini gerektiren işlemlerde kullanılmalıdır.

Örnek kullanımlar:

* Doküman yükleme
* Oturum silme onayı
* API anahtarı uyarısı
* Guardrail detayları
* Kaynak doküman önizleme

Modal yapısı:

| Bölüm      | Açıklama                             |
| ---------- | ------------------------------------ |
| Başlık     | Net ve kısa                          |
| Açıklama   | Kullanıcının ne yapacağını açıklar   |
| İçerik     | Form, uyarı veya detay alanı         |
| Aksiyonlar | Sağ altta primary/secondary butonlar |

Kritik işlemlerde primary buton yerine danger buton kullanılmalıdır.

---

## 15. Logo ve Icon Kullanım Kuralları

MikroAsistan logosu; sohbet balonu, e-ticaret paketi ve veri bağlantı noktaları fikrini temsil eder.

### 15.1 Logo Kullanımı

| Kullanım   | Kural                                          |
| ---------- | ---------------------------------------------- |
| Açık zemin | Lacivert + mavi + cyan logo kullanılabilir     |
| Koyu zemin | Beyaz veya açık mavi varyasyon kullanılmalıdır |
| Navbar     | Yatay logo kullanılır                          |
| App icon   | Sadece ikon versiyonu kullanılır               |
| Favicon    | Sadeleştirilmiş ikon kullanılmalıdır           |

Logo etrafında yeterli boşluk bırakılmalıdır. Logo sıkıştırılmamalı, döndürülmemeli veya farklı renklere rastgele boyanmamalıdır.

### 15.2 App Icon

App icon 1:1 oranında hazırlanmalıdır.

Önerilen yapı:

| Özellik       | Değer                                   |
| ------------- | --------------------------------------- |
| Oran          | 1:1                                     |
| Köşe yarıçapı | 22–24 px                                |
| Arka plan     | Beyaz veya çok açık gri                 |
| Ana sembol    | Chat bubble + paket + veri bağlantıları |
| Stil          | Minimal, flat, modern                   |

---

## 16. Mobil Arayüz Kuralları

Mobil mockup ve olası mobil arayüzlerde sade yapı korunmalıdır.

### 16.1 Mobil Chat Yapısı

| Alan            | Kural                                 |
| --------------- | ------------------------------------- |
| Üst bar         | Logo, başlık, durum                   |
| Chat alanı      | Tam genişliğe yakın, rahat okunabilir |
| Mesaj balonları | Kısa satır uzunluğu                   |
| Alt input       | Sabit alt alanda                      |
| Alt navigasyon  | Sohbet, Kaynaklar, Geçmiş, Ayarlar    |

Mobilde sağ panel kullanılmaz. Kaynaklar ayrı sekme veya açılır alt panel olarak gösterilmelidir.

---

## 17. Erişilebilirlik Kuralları

Tasarım sistemi, erişilebilirlik kurallarını gözetmelidir.

| Kural            | Açıklama                                                             |
| ---------------- | -------------------------------------------------------------------- |
| Kontrast         | Metinler zemin üzerinde yeterli kontrasta sahip olmalıdır            |
| Renk bağımlılığı | Durumlar yalnızca renkle değil, metin veya ikonla da belirtilmelidir |
| Buton alanı      | Mobil dokunma alanları en az 44 px olmalıdır                         |
| Font boyutu      | Gövde metni 16 px altında olmamalıdır                                |
| Hata mesajı      | Kullanıcıya net ve açıklayıcı bilgi vermelidir                       |
| Focus durumu     | Klavye ile gezinmede görünür olmalıdır                               |

---

## 18. Boş Durumlar

Kullanıcı bir ekrana ilk kez girdiğinde veya veri bulunmadığında boş durum ekranları kullanılmalıdır.

### Örnek Boş Durumlar

| Ekran            | Mesaj                                      |
| ---------------- | ------------------------------------------ |
| Sohbet yok       | “Henüz bir sohbet başlatılmadı.”           |
| Kaynak yok       | “Bu yanıt için kaynak bulunamadı.”         |
| Doküman yok      | “Henüz mağaza verisi yüklenmedi.”          |
| İz kaydı yok     | “Bu zaman aralığında iz kaydı bulunamadı.” |
| Arama sonucu yok | “Aramanızla eşleşen sonuç bulunamadı.”     |

Boş durumlarda kullanıcıya bir sonraki adım gösterilmelidir.

Örnek:

“Yeni sohbet başlat”
“Doküman yükle”
“Filtreleri temizle”

---

## 19. Hata Durumları

Hata durumları sade, açıklayıcı ve yönlendirici olmalıdır.

| Hata Tipi            | Gösterim                        |
| -------------------- | ------------------------------- |
| API hatası           | Kırmızı uyarı kartı             |
| Bağlantı hatası      | Yeniden dene aksiyonu           |
| Yetkilendirme hatası | Giriş veya token kontrol mesajı |
| Veri bulunamadı      | Amber bilgi alanı               |
| Guardrail engeli     | Kırmızı/güvenlik temalı uyarı   |

Hata mesajları kullanıcıyı suçlayıcı olmamalıdır. Teknik detaylar son kullanıcıya gereksiz yere gösterilmemelidir.

---

## 20. Token Kullanım İlkesi

Tasarım sistemi aşağıdaki token grupları üzerinden yönetilir:

| Token Grubu  | İçerik                                              |
| ------------ | --------------------------------------------------- |
| `colors`     | Renk paleti                                         |
| `typography` | Font ailesi, boyut, ağırlık, satır yüksekliği       |
| `spacing`    | Margin, padding, gap değerleri                      |
| `radius`     | Köşe yarıçapları                                    |
| `shadows`    | Gölge seviyeleri                                    |
| `layout`     | Sidebar, panel, container ölçüleri                  |
| `components` | Button, input, card, badge gibi bileşen kuralları   |
| `chat`       | Chat mesaj balonu, kaynak kartı ve sistem mesajları |
| `dashboard`  | KPI, grafik ve gözlemlenebilirlik paneli kuralları  |

Tasarım değeri tek bir yerde tanımlanmalıdır. Web arayüzü, mockuplar ve ileride oluşturulabilecek mobil arayüzler aynı tasarım kararlarını takip etmelidir.

---

## 21. Tailwind Kullanım İlkesi

Frontend tarafında Tailwind CSS kullanılacağı için renk, spacing, radius ve font değerleri Tailwind tema yapılandırmasıyla uyumlu olmalıdır.

Kurallar:

* Rastgele HEX değerleri bileşen içinde kullanılmamalıdır.
* Aynı renk için farklı isimlendirme yapılmamalıdır.
* Tasarım sistemi dışında yeni renk eklenmemelidir.
* Spacing değerleri belirlenen skalaya bağlı kalmalıdır.
* Buton, kart, input ve badge gibi tekrar eden bileşenler ortak tasarım kurallarına göre hazırlanmalıdır.

---

## 22. Bileşen Öncelikleri

Projede ilk tasarlanacak temel bileşenler şunlardır:

| Öncelik | Bileşen                         |
| ------- | ------------------------------- |
| 1       | Button                          |
| 2       | Input / Chat Input              |
| 3       | Card                            |
| 4       | Badge / Status Chip             |
| 5       | Sidebar                         |
| 6       | Chat Message Bubble             |
| 7       | Source / Retrieved Context Card |
| 8       | KPI Card                        |
| 9       | Table                           |
| 10      | Modal                           |

Bu bileşenler tamamlandıktan sonra sayfa tasarımları daha tutarlı şekilde oluşturulabilir.

---

## 23. Sayfa Bazlı Tasarım Kuralları

### 23.1 Web Chat Sayfası

Kullanım amacı: Son kullanıcının MikroAsistan ile konuşması.

Zorunlu alanlar:

* Sol sidebar
* Chat header
* Session ID bilgisi
* Kullanıcı mesajları
* Asistan cevapları
* Retrieved context / kaynak kartları
* Chat input
* Güvenli bağlantı veya veri dayanaklı cevap bildirimi

### 23.2 Gözlemlenebilirlik Sayfası

Kullanım amacı: Token, latency, retrieval ve guardrail metriklerini izlemek.

Zorunlu alanlar:

* KPI kartları
* Günlük trend grafiği
* Latency dağılımı
* Retrieved doküman kalitesi
* Canlı izler
* Uyarılar
* En çok kullanılan kaynaklar

### 23.3 Scalar API Sayfası

Kullanım amacı: Backend endpointlerini dokümante etmek ve test etmek.

Zorunlu alanlar:

* Endpoint menüsü
* Seçili endpoint açıklaması
* Request body şeması
* Örnek istek
* API istemcisi
* Response preview
* Son istekler

---

## 24. Genel Görsel Dil

MikroAsistan görsel dili şu özellikleri taşımalıdır:

* Açık, ferah ve sade arayüz
* Lacivert ile güven hissi
* Mavi ile teknoloji ve ana aksiyon vurgusu
* Cyan ile veri bağlantısı ve yapay zeka hissi
* Yuvarlatılmış kartlar
* Hafif gölgeler
* Okunabilir metin hiyerarşisi
* Teknik ama kullanıcı dostu görünüm

Arayüz; aşırı renkli, karmaşık, neon, oyuncak gibi veya fazla dekoratif görünmemelidir. Projenin hem akademik/staj sunumuna hem de gerçek ürün demosuna uygun profesyonel bir çizgide kalması hedeflenir.

---

## 25. Kısa Tasarım Gerekçesi

MikroAsistan tasarım sistemi, güvenilirlik, veri şeffaflığı ve modern yapay zeka deneyimi üzerine kuruludur. Chat arayüzünde kullanıcıya sade ve anlaşılır bir deneyim sunulurken, dashboard ve API arayüzlerinde teknik detaylar düzenli ve takip edilebilir şekilde gösterilir.

Lacivert tonları sistemin güvenilir ve kontrollü yapısını, mavi tonları teknolojik altyapıyı, cyan vurgu rengi ise RAG mimarisindeki veri bağlantılarını temsil eder. Yuvarlatılmış kartlar ve hafif gölgeler, arayüzü modern ve kullanıcı dostu hale getirir.

Bu tasarım sistemi, projenin yalnızca teknik olarak değil, görsel ve kullanıcı deneyimi açısından da planlı, tutarlı ve sunuma hazır olduğunu gösterir.
