# Ürün Excel Veri Sözleşmesi

Bu doküman, MikroAsistan uygulamasına aktarılacak ürün verilerinin Excel dosyasında nasıl hazırlanacağını tanımlar.

## Çalışma Kitabı Yapısı

Excel çalışma kitabı aşağıdaki sayfaları içerir:

- `Instructions`: Alan açıklamaları, veri tipleri ve kullanım kuralları
- `Products`: İçe aktarılacak ürün kayıtları
- `Lists`: Açılır listelerde kullanılan kontrollü değerler

İçe aktarma sistemi yalnızca `Products` sayfasındaki ürün kayıtlarını işler.

## Products Sayfası

`Products` sayfasının sütun adları değiştirilmemeli veya silinmemelidir.

| Alan | Zorunlu | Veri tipi | Açıklama |
|---|---:|---|---|
| `product_id` | Evet | Metin | Sistem içinde ürünü benzersiz olarak tanımlayan değişmeyen kimlik |
| `sku` | Evet | Metin | Mağazanın benzersiz stok kodu |
| `name` | Evet | Metin | Kullanıcıya gösterilecek ürün adı |
| `category` | Evet | Metin | Ürünün ana kategorisi |
| `brand` | Evet | Metin | Ürün markası |
| `price` | Evet | Ondalık sayı | Güncel satış fiyatı |
| `currency` | Evet | Metin | Fiyatın para birimi |
| `description` | Evet | Metin | Ürün açıklaması |
| `features` | Evet | Metin | Teknik ve öne çıkan özellikler |
| `stock` | Evet | Tam sayı | Satılabilir stok adedi |
| `rating` | Evet | Ondalık sayı | Ürün değerlendirme puanı |
| `image_url` | Hayır | URL | Ürün görselinin bağlantısı |
| `product_url` | Hayır | URL | Mağazadaki ürün detay sayfası |
| `is_active` | Evet | Boolean | Ürünün aktif olarak kullanılıp kullanılmayacağı |

## Benzersiz Alanlar

Aşağıdaki alanlar her ürün için benzersiz olmalıdır:

- `product_id`
- `sku`

Aynı `product_id` değerine sahip bir ürün tekrar içe aktarıldığında yeni kayıt oluşturulmaz. Mevcut ürün güncellenir.

`product_id` ürün oluşturulduktan sonra değiştirilmemelidir.

Önerilen kimlik biçimi:

```text
prd-001
prd-002
prd-003
```

Önerilen SKU biçimi:

```text
LNV-IPG3-001
ASU-TUF-A15-001
LOG-G502-001
```

## Doğrulama Kuralları

### product_id

- Boş olamaz.
- Excel dosyası içinde benzersiz olmalıdır.
- Başında ve sonunda boşluk bulunmamalıdır.

### sku

- Boş olamaz.
- Excel dosyası içinde benzersiz olmalıdır.
- Mağaza içinde değişmeyen bir stok kodu olmalıdır.

### name

- Boş olamaz.
- Ürünü kullanıcıya açık şekilde tanımlamalıdır.

### category

Kategori değeri `Lists` sayfasındaki kontrollü kategorilerden biri olmalıdır.

Başlangıç kategorileri:

```text
Laptop
Desktop
Monitor
Keyboard
Mouse
Headset
Accessory
Component
Phone
Tablet
```

Kategori listesi mağazanın ürün yapısına göre genişletilebilir.

### brand

- Boş olamaz.
- Marka adı tutarlı biçimde yazılmalıdır.
- Aynı marka için farklı yazımlar kullanılmamalıdır.

Doğru:

```text
Lenovo
```

Yanlış:

```text
lenovo
LENOVO
Lenovo Türkiye
```

### price

- Sayısal değer olmalıdır.
- Sıfırdan büyük olmalıdır.
- Para birimi simgesi hücreye yazılmamalıdır.

Doğru:

```text
32999.99
```

Yanlış:

```text
32.999,99 TL
₺32999
ücretsiz
```

### currency

Desteklenen başlangıç değerleri:

```text
TRY
USD
EUR
```

Yeni para birimleri eklenmeden önce backend doğrulama kuralları güncellenmelidir.

### description

- Boş olamaz.
- Ürünün kullanım amacını ve temel özelliklerini açıklamalıdır.
- HTML etiketi içermemelidir.
- Kullanıcıya gösterilemeyecek dahili mağaza notları içermemelidir.

### features

Ürün özellikleri ` | ` ayıracıyla yazılmalıdır.

Örnek:

```text
Ryzen 7 | 32 GB RAM | 1 TB SSD | RTX 4060 | 144 Hz
```

Her özellik kısa, açık ve bağımsız olmalıdır.

### stock

- Tam sayı olmalıdır.
- Negatif olamaz.
- Stokta bulunmayan ürünler için `0` kullanılmalıdır.

### rating

- Sayısal değer olmalıdır.
- `0` ile `5` arasında olmalıdır.
- Ondalık değer kullanılabilir.

Örnek:

```text
4.5
```

### image_url

- İsteğe bağlıdır.
- `http://` veya `https://` ile başlamalıdır.
- Doğrudan ürün görseline veya mağazanın güvenilir görsel adresine yönlenmelidir.

### product_url

- İsteğe bağlıdır.
- `http://` veya `https://` ile başlamalıdır.
- Mağazanın ürün detay sayfasına yönlenmelidir.

### is_active

Yalnızca aşağıdaki değerlerden biri kullanılmalıdır:

```text
TRUE
FALSE
```

`TRUE` olan ürünler mağaza aramalarına ve RAG sistemine dahil edilir.

`FALSE` olan ürünler veritabanında korunur ancak kullanıcı önerilerinde kullanılmaz.

## İçe Aktarma Davranışı

Excel dosyası içe aktarıldığında:

1. Çalışma kitabının açılabildiği kontrol edilir.
2. `Products` sayfasının mevcut olduğu doğrulanır.
3. Sütun başlıkları kontrol edilir.
4. Tamamen boş satırlar yok sayılır.
5. Her ürün satırı bağımsız olarak doğrulanır.
6. Yeni `product_id` değerleri veritabanına eklenir.
7. Mevcut `product_id` değerleri güncellenir.
8. Hatalı satırlar kaydedilmez ve hata raporuna eklenir.
9. Excel dosyasında bulunmayan mevcut ürünler otomatik olarak silinmez.
10. Başarılı değişikliklerden sonra ürün arama indeksi güncellenir.

## Hata Raporlama

İçe aktarma sonucu aşağıdaki bilgileri sağlamalıdır:

- Toplam satır sayısı
- Eklenen ürün sayısı
- Güncellenen ürün sayısı
- Atlanan satır sayısı
- Hatalı satır sayısı
- Satır numarası
- Hatalı alan
- Hata açıklaması

Örnek:

```json
{
  "success": false,
  "message": "Product import completed with validation errors",
  "data": {
    "total_rows": 25,
    "created": 18,
    "updated": 4,
    "skipped": 1,
    "failed": 2,
    "errors": [
      {
        "row": 7,
        "field": "price",
        "message": "Price must be greater than zero."
      },
      {
        "row": 12,
        "field": "sku",
        "message": "SKU must be unique."
      }
    ]
  }
}
```

## Dosya Güvenliği

- Excel dosyasında makro kullanılmamalıdır.
- Dosya biçimi `.xlsx` olmalıdır.
- Gerçek API anahtarları veya gizli bilgiler Excel dosyasına yazılmamalıdır.
- Kullanıcı parolası, ödeme bilgisi veya kişisel müşteri verisi ürün dosyasına eklenmemelidir.
- İçe aktarma öncesinde dosya boyutu ve satır sayısı sınırlandırılmalıdır.

## Şablon Konumu

Standart ürün şablonu repository içinde şu konumda tutulur:

```text
docs/templates/product_import_template.xlsx
```