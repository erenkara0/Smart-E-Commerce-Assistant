# MikroAsistan — Renk Paleti

Kaynak: `implementation_plan.md` — Proje Özeti, Sistem Mimarisi, Frontend Arayüz ve Gözlemlenebilirlik bölümleri. Bu belge tek doğruluk kaynağı değildir; plandan sapma gerekirse önce proje planı güncellenir.

Bu renk paleti, **Mikro İhracat ve E-Ticaret İçin RAG Tabanlı Akıllı Asistan** projesinin ortak görsel dilini tanımlar. Palet; web arayüzü, sohbet ekranı, yönetim paneli, API dokümantasyonu sunumu ve mockup tasarımlarında tutarlı bir marka kimliği oluşturmak için kullanılır.

Tüm renkler tasarım sistemi üzerinden tüketilmelidir. Bileşenlerde rastgele veya sabit HEX değerleri kullanılmamalı; renkler belirlenen token isimleriyle yönetilmelidir.

---

## Ana Palet

| Rol            | İsim      |       HEX | Token                  | Kullanım                                         |
| -------------- | --------- | --------: | ---------------------- | ------------------------------------------------ |
| Primary        | Blue 600  | `#2563EB` | `colors.primary`       | Ana aksiyonlar, marka vurgusu, aktif durumlar    |
| Primary Dark   | Navy 900  | `#0F172A` | `colors.primaryDark`   | Logo metni, başlıklar, koyu alanlar              |
| Secondary      | Cyan 500  | `#06B6D4` | `colors.secondary`     | Yapay zeka, veri bağlantıları, yardımcı vurgular |
| Secondary Dark | Cyan 700  | `#0E7490` | `colors.secondaryDark` | Hover, ikon detayları, vurgu geçişleri           |
| Background     | Slate 50  | `#F8FAFC` | `colors.background`    | Sayfa arka planı                                 |
| Surface        | White     | `#FFFFFF` | `colors.surface`       | Kartlar, chat kutuları, modal yüzeyleri          |
| Surface Soft   | Blue 50   | `#EFF6FF` | `colors.surfaceSoft`   | Hafif vurgulu bilgi alanları                     |
| Border         | Slate 200 | `#E2E8F0` | `colors.border`        | Kart kenarlıkları, ayırıcı çizgiler              |
| Text Primary   | Slate 900 | `#0F172A` | `colors.textPrimary`   | Ana metin, başlıklar                             |
| Text Secondary | Slate 500 | `#64748B` | `colors.textSecondary` | Açıklama, yardımcı metin                         |
| Success        | Green 600 | `#16A34A` | `colors.success`       | Başarılı işlem, güvenli cevap, aktif bağlantı    |
| Warning        | Amber 500 | `#F59E0B` | `colors.warning`       | Uyarı, eksik veri, dikkat gerektiren durum       |
| Danger         | Red 600   | `#DC2626` | `colors.danger`        | Hata, başarısız işlem, güvenlik riski            |

---

## Marka Renklerinin Anlamı

| Renk            | Anlamı                                               |
| --------------- | ---------------------------------------------------- |
| Lacivert / Navy | Güven, kurumsallık, kontrollü sistem yapısı          |
| Mavi            | Teknoloji, yapay zeka altyapısı, ana marka aksiyonu  |
| Turkuaz / Cyan  | Veri bağlantıları, RAG mimarisi, yenilikçilik        |
| Açık Gri        | Temiz arayüz, okunabilirlik, sade kullanıcı deneyimi |
| Yeşil           | Başarılı işlem ve güvenilir çıktı                    |
| Amber           | Dikkat, eksik bağlam veya bekleyen işlem             |
| Kırmızı         | Hata, reddedilen işlem veya güvenlik uyarısı         |

---

## Kullanım Kuralları

Primary `#2563EB`, yalnızca birincil aksiyonlarda kullanılmalıdır. Örneğin “Soru Gönder”, “Oturum Başlat”, “Veriyi Yükle” gibi ana işlemlerde tercih edilir. Bir ekranda birden fazla birincil aksiyon rengi kullanmaktan kaçınılmalıdır.

Primary Dark `#0F172A`, logo yazısı, ana başlıklar, koyu zeminler ve kurumsal vurgu alanları için kullanılır. Bağımsız bir buton rengi olarak değil, marka otoritesini destekleyen ana koyu ton olarak düşünülmelidir.

Secondary `#06B6D4`, yapay zeka, veri bağlantıları, embedding, retrieval ve LangSmith gözlemlenebilirlik gibi teknik kavramların görsel temsilinde kullanılabilir. Dekoratif amaçla aşırı kullanılmamalıdır.

Background `#F8FAFC`, sayfa genel zemini için kullanılır. Surface `#FFFFFF`, kartlar, chat mesaj kutuları, tablolar ve modal alanlar için kullanılır. Bu iki renk üst üste geldiğinde derinlik, border ve hafif gölge ile verilmelidir.

Text Primary `#0F172A`, başlık ve ana gövde metinlerinde kullanılır. Text Secondary `#64748B`, açıklama, placeholder, meta bilgi ve ikincil metinler için tercih edilir.

Success, Warning ve Danger renkleri yalnızca durum bildirimi amacıyla kullanılmalıdır. Bu renkler dekoratif unsur olarak kullanılmamalı; kullanıcıya anlamlı bir sistem durumu iletmelidir.

---

## Sohbet Arayüzü Renkleri

MikroAsistan’ın ana kullanıcı deneyimi chat arayüzü olduğu için mesaj tipleri ayrı bir renk mantığıyla yönetilir.

| Alan                    |      Renk | Token                         | Kullanım                               |
| ----------------------- | --------: | ----------------------------- | -------------------------------------- |
| Kullanıcı Mesajı        | `#2563EB` | `chatColors.userMessage`      | Kullanıcının gönderdiği mesaj balonu   |
| Asistan Mesajı          | `#FFFFFF` | `chatColors.assistantMessage` | Asistan cevabı                         |
| Asistan Mesaj Kenarlığı | `#E2E8F0` | `chatColors.assistantBorder`  | Asistan mesaj kartı sınırı             |
| Sistem Bilgisi          | `#EFF6FF` | `chatColors.systemInfo`       | Bilgilendirme, yardımcı açıklama       |
| Kaynak / Retrieved Veri | `#ECFEFF` | `chatColors.retrievedContext` | Cevapta kullanılan kaynak veri alanı   |
| Veri Bulunamadı         | `#FEF3C7` | `chatColors.noContext`        | Mağaza verisinde bilgi bulunamadığında |
| Hata Mesajı             | `#FEE2E2` | `chatColors.errorMessage`     | API, bağlantı veya güvenlik hatası     |

---

## RAG Durum Renkleri

RAG sisteminde soru-cevap akışı sırasında oluşan durumlar aşağıdaki renklerle ifade edilir.

| Durum                | Açıklama                             |                 Renk | Token                                  |
| -------------------- | ------------------------------------ | -------------------: | -------------------------------------- |
| QUESTION_RECEIVED    | Kullanıcı sorusu alındı              |       Blue `#2563EB` | `ragStatusColors.QUESTION_RECEIVED`    |
| RETRIEVING           | Vektör veritabanında arama yapılıyor |       Cyan `#06B6D4` | `ragStatusColors.RETRIEVING`           |
| CONTEXT_FOUND        | İlgili mağaza verisi bulundu         |      Green `#16A34A` | `ragStatusColors.CONTEXT_FOUND`        |
| LOW_CONFIDENCE       | Eşleşme zayıf veya bağlam yetersiz   |      Amber `#F59E0B` | `ragStatusColors.LOW_CONFIDENCE`       |
| NO_CONTEXT           | İlgili veri bulunamadı               | Amber Dark `#D97706` | `ragStatusColors.NO_CONTEXT`           |
| ANSWER_GENERATED     | Yanıt başarıyla oluşturuldu          |       Blue `#2563EB` | `ragStatusColors.ANSWER_GENERATED`     |
| BLOCKED_BY_GUARDRAIL | Güvenlik kuralı nedeniyle engellendi |        Red `#DC2626` | `ragStatusColors.BLOCKED_BY_GUARDRAIL` |
| SYSTEM_ERROR         | Sistem veya API hatası               |   Red Dark `#B91C1C` | `ragStatusColors.SYSTEM_ERROR`         |

Not: RAG akışında yeşil renk yalnızca başarılı ve güvenilir bağlam bulunduğunda kullanılmalıdır. Bağlam bulunamadığında sistem cevap uydurmak yerine kullanıcıya bilginin mağaza verilerinde bulunmadığını belirtmelidir.

---

## LangSmith / Gözlemlenebilirlik Renkleri

Token maliyeti, latency ve retrieved doküman takibi gibi gözlemlenebilirlik metrikleri için aşağıdaki renk sistemi kullanılabilir.

| Metrik Durumu              |            Renk | Token                                 | Kullanım                             |
| -------------------------- | --------------: | ------------------------------------- | ------------------------------------ |
| Normal Token Kullanımı     | Green `#16A34A` | `observabilityColors.tokenNormal`     | Beklenen maliyet aralığı             |
| Yüksek Token Kullanımı     | Amber `#F59E0B` | `observabilityColors.tokenHigh`       | Optimize edilmesi gereken prompt     |
| Çok Yüksek Token Kullanımı |   Red `#DC2626` | `observabilityColors.tokenCritical`   | Maliyet riski                        |
| Normal Latency             | Green `#16A34A` | `observabilityColors.latencyNormal`   | Kabul edilebilir yanıt süresi        |
| Yüksek Latency             | Amber `#F59E0B` | `observabilityColors.latencyHigh`     | Performans uyarısı                   |
| Kritik Latency             |   Red `#DC2626` | `observabilityColors.latencyCritical` | Kullanıcı deneyimini bozan gecikme   |
| Güçlü Retrieval            | Green `#16A34A` | `observabilityColors.retrievalStrong` | Yüksek benzerlik ve kaliteli bağlam  |
| Zayıf Retrieval            | Amber `#F59E0B` | `observabilityColors.retrievalWeak`   | Düşük benzerlik veya yetersiz bağlam |
| Başarısız Retrieval        |   Red `#DC2626` | `observabilityColors.retrievalFailed` | İlgili doküman bulunamadı            |

---

## Logo Kullanım Renkleri

MikroAsistan logosu için önerilen ana kullanım aşağıdaki gibidir.

| Logo Bölümü                |               Renk |                   HEX |
| -------------------------- | -----------------: | --------------------: |
| “Mikro” yazısı             |       Primary Dark |             `#0F172A` |
| “Asistan” yazısı           |            Primary |             `#2563EB` |
| Konuşma balonu dış çizgisi |       Primary Dark |             `#0F172A` |
| Kutu / paket ikonu         |            Primary |             `#2563EB` |
| Veri bağlantı noktaları    |          Secondary |             `#06B6D4` |
| Açık zemin                 | Background / White | `#F8FAFC` / `#FFFFFF` |

Logo, açık zeminde lacivert + mavi + turkuaz renkleriyle kullanılmalıdır. Koyu zeminde ise ikon ve yazı okunabilirliği korunacak şekilde beyaz veya açık mavi varyasyon tercih edilmelidir.

---

## Açık Tema Kullanımı

Açık tema, projenin varsayılan arayüz teması olarak düşünülür.

| Alan               |      Renk |
| ------------------ | --------: |
| Sayfa arka planı   | `#F8FAFC` |
| Kart / Chat yüzeyi | `#FFFFFF` |
| Ana başlık         | `#0F172A` |
| Yardımcı metin     | `#64748B` |
| Ana buton          | `#2563EB` |
| Buton hover        | `#1E40AF` |
| Veri / AI vurgusu  | `#06B6D4` |

---

## Koyu Tema Kullanımı

Scalar, geliştirici paneli veya sunum mockuplarında koyu tema kullanılacaksa aşağıdaki renk mantığı tercih edilir.

| Alan                |      Renk |
| ------------------- | --------: |
| Sayfa arka planı    | `#020617` |
| Kart / Panel yüzeyi | `#0F172A` |
| Kenarlık            | `#1E293B` |
| Ana metin           | `#F8FAFC` |
| Yardımcı metin      | `#94A3B8` |
| Ana vurgu           | `#3B82F6` |
| AI / Veri vurgusu   | `#22D3EE` |
| Hata                | `#F87171` |
| Başarı              | `#4ADE80` |

Koyu temada mavi ve turkuaz vurgular daha parlak tonlarla kullanılabilir. Ancak uzun metinlerde yüksek doygunluklu renkler kullanılmamalı, okunabilirlik öncelikli olmalıdır.

---

## Renk Skalası

### Primary Blue

| Seviye |       HEX | Kullanım                |
| ------ | --------: | ----------------------- |
| 50     | `#EFF6FF` | Açık bilgi alanları     |
| 100    | `#DBEAFE` | Hafif vurgulu arka plan |
| 200    | `#BFDBFE` | Pasif buton zemini      |
| 300    | `#93C5FD` | Yardımcı vurgu          |
| 400    | `#60A5FA` | Hover detayları         |
| 500    | `#3B82F6` | İkincil mavi vurgu      |
| 600    | `#2563EB` | Ana marka rengi         |
| 700    | `#1D4ED8` | Hover / pressed         |
| 800    | `#1E40AF` | Koyu vurgu              |
| 900    | `#1E3A8A` | Başlık / güçlü vurgu    |

### Cyan / AI Accent

| Seviye |       HEX | Kullanım                     |
| ------ | --------: | ---------------------------- |
| 50     | `#ECFEFF` | Retrieved context arka planı |
| 100    | `#CFFAFE` | Hafif AI bilgi alanı         |
| 200    | `#A5F3FC` | Yardımcı vurgu               |
| 300    | `#67E8F9` | Grafik / bağlantı çizgisi    |
| 400    | `#22D3EE` | Koyu tema AI vurgusu         |
| 500    | `#06B6D4` | Ana AI / veri bağlantı rengi |
| 600    | `#0891B2` | Hover                        |
| 700    | `#0E7490` | Koyu vurgu                   |
| 800    | `#155E75` | Başlık detayı                |
| 900    | `#164E63` | Koyu zemin destek rengi      |

### Neutral Slate

| Seviye |       HEX | Kullanım                   |
| ------ | --------: | -------------------------- |
| 50     | `#F8FAFC` | Sayfa arka planı           |
| 100    | `#F1F5F9` | Hafif yüzey                |
| 200    | `#E2E8F0` | Border                     |
| 300    | `#CBD5E1` | Pasif kenarlık             |
| 400    | `#94A3B8` | Placeholder                |
| 500    | `#64748B` | İkincil metin              |
| 600    | `#475569` | Yardımcı başlık            |
| 700    | `#334155` | Koyu yardımcı metin        |
| 800    | `#1E293B` | Koyu yüzey                 |
| 900    | `#0F172A` | Ana metin / logo koyu tonu |

---

## Erişilebilirlik Notları

Metin renkleri, açık ve koyu zeminler üzerinde yeterli kontrast sağlayacak şekilde kullanılmalıdır.

Primary ve Secondary renkleri uzun paragraflarda metin rengi olarak kullanılmamalıdır. Bu renkler aksiyon, ikon, vurgu, grafik ve durum göstergesi için uygundur.

Danger rengi yalnızca hata, güvenlik uyarısı veya engellenen işlem durumlarında kullanılmalıdır. Sürekli kırmızı kullanımı kullanıcıda gereksiz alarm etkisi oluşturabilir.

Success rengi yalnızca başarılı işlem, güvenilir retrieval sonucu veya tamamlanmış süreç anlamında kullanılmalıdır.

---

## Kısa Tasarım Gerekçesi

MikroAsistan renk paleti, güvenilirlik ve teknolojik modernlik üzerine kurulmuştur. Lacivert tonları sistemin kurumsal ve kontrollü yapısını temsil ederken, mavi renk yapay zeka destekli dijital ürün kimliğini güçlendirir. Turkuaz vurgu rengi, RAG mimarisindeki veri bağlantılarını ve akıllı retrieval sürecini temsil eder. Açık gri ve beyaz yüzeyler, sohbet arayüzünde sade, okunabilir ve profesyonel bir kullanıcı deneyimi sağlar.
