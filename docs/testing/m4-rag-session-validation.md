# M4 RAG ve Oturum Hafızası Doğrulama Notları

Bu doküman, M4 kapsamında geliştirilen RAG cevap üretimi, OpenAI hata yönetimi, SQLite tabanlı oturum hafızası ve LangSmith gözlemlenebilirlik özellikleri için gerçekleştirilen doğrulama adımlarını içerir.

## Test Ortamı

- Backend: FastAPI
- Model sağlayıcısı: OpenAI API
- Oturum veritabanı: SQLite
- API dokümantasyonu ve manuel test aracı: Scalar
- Gözlemlenebilirlik: LangSmith
- Vector store: In-memory

## 1. RAG Cevap Üretimi

### Test isteği

```json
{
  "message": "Oyun için ASUS laptop önerir misin?"
}
```

### Beklenen sonuç

- Kullanıcı sorgusuna uygun ürün dokümanları aranmalıdır.
- Model yalnızca bulunan mağaza bağlamına göre cevap üretmelidir.
- Ürün adı, fiyatı, stok durumu ve teknik özellikleri veri setindeki değerlerle uyumlu olmalıdır.
- Cevapla birlikte yeni bir `session_id` dönmelidir.

### Sonuç

Test başarılı oldu. Sistem ilgili ASUS ürününü mağaza veri setinden buldu ve RAG bağlamına dayalı bir cevap üretti.

## 2. Yeni Oturum Kimliği Oluşturma

### Test isteği

```json
{
  "message": "Laptop önerir misin?"
}
```

### Beklenen sonuç

İstekte `session_id` bulunmadığında backend yeni bir UUID oluşturmalı ve cevap içinde döndürmelidir.

### Sonuç

Test başarılı oldu. Yeni konuşma için benzersiz bir `session_id` üretildi.

## 3. Aynı Oturumda Konuşmaya Devam Etme

### İlk istek

```json
{
  "message": "ASUS bilgisayar önerir misin?"
}
```

### Devam isteği

```json
{
  "message": "Bunun fiyatı nedir?",
  "session_id": "İLK_CEVAPTAN_GELEN_SESSION_ID"
}
```

### Beklenen sonuç

- İkinci istekte aynı `session_id` korunmalıdır.
- Sistem, “bunun” ifadesinin önceki mesajda önerilen ASUS ürününü belirttiğini anlamalıdır.
- Ürünün veri setindeki fiyatı cevaplanmalıdır.

### Sonuç

Test başarılı oldu. Konuşma geçmişi retrieval sorgusuna ve RAG prompt’una eklendiği için devam sorusu doğru cevaplandı.

## 4. SQLite Kalıcılık Testi

### Test adımları

1. Aynı `session_id` ile birden fazla mesaj gönderildi.
2. Backend durduruldu.
3. Backend yeniden başlatıldı.
4. Önceki `session_id` kullanılarak yeni bir devam sorusu gönderildi.

### Test isteği

```json
{
  "message": "Peki stokta kaç tane var?",
  "session_id": "ÖNCEKİ_SESSION_ID"
}
```

### Beklenen sonuç

Backend yeniden başlatılsa bile önceki konuşma SQLite veritabanından okunmalı ve ürünün stok bilgisi doğru cevaplanmalıdır.

### Sonuç

Test başarılı oldu. Oturum geçmişinin uygulama belleğinde değil, SQLite veritabanında kalıcı olarak saklandığı doğrulandı.

## 5. Konuşma Geçmişi Sınırı

Sistemde prompt boyutunun kontrol altında tutulması için yalnızca yapılandırılmış sayıdaki son mesajlar kullanılmaktadır.

Kullanılan ayar:

```env
SESSION_MEMORY_LIMIT=5
```

Bu değer, RAG prompt’una eklenecek yakın dönem konuşma geçmişini sınırlar.

## 6. İlgisiz Ürün Sorgusu

### Test isteği

```json
{
  "message": "Mağazada uçak motoru bulunuyor mu?"
}
```

### Beklenen sonuç

- İlgili ürün bağlamı bulunmamalıdır.
- Sistem ürün veya özellik uydurmamalıdır.
- Mağaza veri setinde yeterli bilgi bulunmadığını bildiren güvenli cevap dönmelidir.

### Sonuç

Test başarılı oldu. Sistem veri seti dışında ürün bilgisi üretmedi.

## 7. OpenAI Hata Yönetimi

Aşağıdaki hata durumları için kullanıcı dostu fallback cevapları tanımlanmıştır:

- Eksik API anahtarı
- Kimlik doğrulama hatası
- Yetki hatası
- Rate limit
- Zaman aşımı
- Bağlantı hatası
- Geçersiz istek
- OpenAI servis hatası
- Boş model cevabı

Hata durumlarında teknik istisnalar kullanıcıya doğrudan gösterilmeden kontrollü cevap üretilmektedir.

## 8. LangSmith Trace Testi

### Test adımları

1. `.env` içinde LangSmith tracing etkinleştirildi.
2. Geçerli LangSmith API anahtarı yapılandırıldı.
3. Scalar üzerinden gerçek bir chat isteği gönderildi.
4. LangSmith projesindeki trace kayıtları kontrol edildi.

### Kullanılan ayarlar

```env
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=smart-e-commerce-assistant
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
```

`LANGSMITH_API_KEY` güvenlik nedeniyle dokümana eklenmemiştir.

### Sonuç

Test başarılı oldu. OpenAI çağrısı LangSmith üzerinde trace olarak görüntülendi. İstek, model cevabı, çalışma süresi ve token kullanım bilgilerinin kaydedildiği doğrulandı.

## Genel Sonuç

M4 kapsamında geliştirilen RAG cevap üretimi, kontrollü prompt yapısı, OpenAI hata yönetimi, session tabanlı konuşma geçmişi, SQLite kalıcılığı ve LangSmith gözlemlenebilirlik özellikleri başarıyla doğrulandı.