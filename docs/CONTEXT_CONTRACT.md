# Frontend ↔ Backend Context Sözleşmesi

> **Sahip:** Üye 4 (Arayüz)
> **Hedef okuyucu:** Üye 1 (Backend/Routing), Üye 2 (Scraper/Analiz), Üye 5 (DB/Modeller)
> **Amaç:** Bu doküman, Jinja2 şablonlarının `render_template(...)` çağrılarında **hangi değişkenleri** ve **hangi yapıda** beklediğini, hangi alanların **zorunlu / opsiyonel** olduğunu sözleşme olarak sabitler. Backend tarafı bu sözleşmeye uyduğu sürece arayüz hiçbir değişiklik gerektirmeden çalışır.

---

## 1. Rotalar ve Beklenen Context

### `GET /` → `index.html`

| Anahtar  | Tip    | Zorunlu? | Açıklama |
|----------|--------|----------|----------|
| `error`  | `str`  | hayır    | Sadece form sonrası hata olursa gönderilir (örn. "Geçersiz URL"). Tanımsızsa hata bloğu hiç render edilmez. |

**Örnek minimum çağrı:**
```python
return render_template("index.html")
```

**Hata akışında:**
```python
return render_template("index.html", error="Geçersiz URL formatı")
```

---

### `POST /scan` → `result.html` (veya redirect → `/scan/<id>`)

| Anahtar       | Tip               | Zorunlu? | Açıklama |
|---------------|-------------------|----------|----------|
| `scan`        | `Scan` objesi     | **evet** | Aşağıdaki "Scan Şeması" tablosuna uygun olmalı. |
| `kvkk_items`  | `list[Item]`      | **evet** | "KVKK Şeması" tablosuna uygun. Boş liste de geçerli. |
| `gdpr_items`  | `list[Item]`      | **evet** | "GDPR Şeması" tablosuna uygun. Boş liste de geçerli. |

**Örnek çağrı:**
```python
return render_template(
    "result.html",
    scan=scan,
    kvkk_items=kvkk_items,
    gdpr_items=gdpr_items,
)
```

> **Öneri:** `POST /scan` doğrudan sonucu render etmek yerine **PRG (Post-Redirect-Get)** desenini uygulayıp `redirect(url_for("main.scan_detail", id=scan.id))` döndürebilir. Bu, kullanıcının F5 yenilemesinde aynı taramanın tekrar tetiklenmesini engeller. Tercih sizin.

---

### `GET /history` → `history.html`

| Anahtar | Tip               | Zorunlu? | Açıklama |
|---------|-------------------|----------|----------|
| `scans` | `list[Scan]`      | **evet** | Boş liste de geçerli (boş durum ekranı otomatik gösterilir). Tipik olarak `created_at DESC` sıralı gönderilir, ama frontend kendi sıralamasını uygular. |

```python
scans = Scan.query.order_by(Scan.created_at.desc()).all()
return render_template("history.html", scans=scans)
```

---

### `GET /scan/<int:id>` → `scan_detail.html`

| Anahtar       | Tip            | Zorunlu? | Açıklama |
|---------------|----------------|----------|----------|
| `scan`        | `Scan` objesi  | **evet** | Aynı şema. |
| `kvkk_items`  | `list[Item]`   | **evet** | Aynı şema. |
| `gdpr_items`  | `list[Item]`   | **evet** | Aynı şema. |

ID bulunamazsa `abort(404)` ile 404 sayfası dönmeli.

---

## 2. Veri Şemaları

### Scan Şeması

Bir taramayı temsil eden ana obje. Öznitelikler dot-erişimle (`scan.url`) ulaşılabilir olmalı — yani SQLAlchemy modeli, `dataclass`, namedtuple veya `dict` (Jinja'da fark etmez ama tutarlılık için **model objesi** önerilir).

| Alan             | Tip                          | Zorunlu? | Geçerli Değerler / Notlar |
|------------------|------------------------------|----------|---------------------------|
| `id`             | `int`                        | evet     | Pozitif tam sayı. Detay sayfasına link kurmakta kullanılır. |
| `url`            | `str`                        | evet     | Tam URL (`http://` veya `https://` ile başlamalı — frontend bunu kontrol edip link olarak gösterir). |
| `kvkk_score`     | `int` (0-100) veya `None`    | hayır    | `None`/`null` ise `—` gösterilir. |
| `gdpr_score`     | `int` (0-100) veya `None`    | hayır    | Aynı. |
| `risk_level`     | `str` veya `None`            | hayır    | Aşağıdaki kabul edilen değerler listesinden biri. Tanınmayan değer "Orta" olarak gösterilir; `None` ise rozet hiç gösterilmez. |
| `llm_suggestions`| `str` veya `None`            | hayır    | Çok satırlı serbest metin. Frontend `white-space: pre-wrap` ile satır sonlarını korur. Markdown render edilmez. |
| `created_at`     | `datetime` veya `str`        | evet     | İdeal: `datetime`. Frontend `scan.created_at.strftime('%d.%m.%Y %H:%M')` çağırır, fakat string ise de bozulmadan basar. |

**`risk_level` kabul edilen değerler** (büyük/küçük harf farketmez; frontend normalize eder):

| Anlam   | Kabul edilen değerler              |
|---------|-----------------------------------|
| Düşük   | `"Düşük"`, `"Dusuk"`, `"low"`     |
| Orta    | `"Orta"`, `"medium"`              |
| Yüksek  | `"Yüksek"`, `"Yuksek"`, `"high"`  |

> Backend'in **Türkçe (Düşük/Orta/Yüksek)** seçmesi önerilir; rapor PDF çıktısı bu metni doğrudan basar.

---

### Item Şeması (`kvkk_items` ve `gdpr_items` listelerinin elemanları)

Her bir kontrol maddesi.

| Alan         | Tip                | Zorunlu? | Açıklama |
|--------------|--------------------|----------|----------|
| `item_label` | `str`              | evet     | Kullanıcıya gösterilecek tam Türkçe etiket (örn. "Gizlilik politikası bağlantısı bulunuyor"). |
| `status`     | `int` (`0` veya `1`)| evet    | `1` → karşılandı (yeşil tik). `0` → eksik (kırmızı çarpı). **Sadece tamsayı `0`/`1` kullanın**; bool döndürürseniz `==1` karşılaştırması yanlış sonuç verir. |

> Frontend, listedeki `1` ve `0`'ları sayarak başlık yanında **otomatik özetleme** yapar ("12 başarılı / 5 eksik"). Bu yüzden backend ek bir özet alanı göndermek zorunda değildir.

---

## 3. Üç Önemli Davranışsal Not

### 3.1. `None` toleransı
Frontend tüm sayısal alanlarda `None` durumunu zarafetle karşılar. `scan.kvkk_score = None` ise:
- Skor halkasında `—` görünür.
- Renk "kırmızı" (0 muamelesi) olarak değil, halka boş gösterilir.

Yani backend hesaplanamayan bir skoru **`0` olarak göndermesin** — `None` göndersin. Frontend doğru ayırt eder.

### 3.2. Tarih formatı
`created_at` mümkünse `datetime` objesi olsun. SQLAlchemy modeli `created_at = db.Column(db.DateTime, default=datetime.utcnow)` şeklinde tanımlıysa otomatik geçer.

Eğer ISO-string olarak göndereceksen (`"2026-05-14T12:30:00"`), frontend bunu olduğu gibi yazar (gün/ay/yıl ayrıştıramaz). Datetime tercih edilsin.

### 3.3. URL temizliği
Frontend `scan.url` ile gelen değeri olduğu gibi gösterir. Backend tarafında:
- Sondaki `/`, `?utm_source=...` gibi gürültü temizlenmiş olsun.
- Yoksa kullanıcı `https://example.com/` ve `https://example.com` taramalarını ayrı kayıtlar gibi görür.

---

## 4. Hata Akışları

| Durum                            | Beklenen davranış |
|----------------------------------|-------------------|
| Boş URL gönderildi               | `render_template("index.html", error="URL boş olamaz")` |
| Geçersiz format (`example`)      | `render_template("index.html", error="Geçerli bir URL giriniz (örnek: https://...)")` |
| Site erişilemiyor (timeout/404)  | `render_template("index.html", error="Site şu an erişilebilir değil.")` |
| LLM servisi düştü                | Tarama yine kaydedilsin, `scan.llm_suggestions = None` gönderilsin. Frontend "Bu tarama için henüz AI önerisi üretilmemiş" der. |
| Detay ID'si bulunamadı           | `abort(404)` |

---

## 5. Frontend'in Karşılamadığı Şeyler (Backend'e Yük)

Frontend bu sözleşmeyi tüketir; aşağıdaki sorumlulukları **karşılamaz**:

- ❌ Skor hesabı (yüzde, ağırlık)
- ❌ Risk seviyesi tayini
- ❌ LLM öneri metni üretimi
- ❌ HTML escape (Jinja2 zaten otomatik yapar, ama backend'den gelen veri içinde **ham HTML/JS göndermeyin** — siteden çekilen ham metinleri sanitize edilmiş halde gönderin)
- ❌ Dil seçimi (her şey Türkçe)

---

## 6. Sözleşmeyi Test Etmek İçin Sahte Veri

Backend tamamlanmadan önce arayüzü test etmek için aşağıdaki sahte context'i bir geliştirme route'unda kullanabilirsiniz:

```python
from datetime import datetime
from types import SimpleNamespace

@app.route("/dev/result")
def dev_result():
    scan = SimpleNamespace(
        id=1,
        url="https://example.com",
        kvkk_score=72,
        gdpr_score=58,
        risk_level="Orta",
        llm_suggestions=(
            "1. Gizlilik politikası sayfası eksik. Aşağıdaki bölümleri içeren bir sayfa eklenmeli...\n"
            "2. Çerez bildirimi yalnızca İngilizce. Türkçe versiyon da eklenmeli.\n"
            "3. Açık rıza onay kutusu önceden işaretli geliyor. Boş gelmeli."
        ),
        created_at=datetime.now(),
    )
    kvkk_items = [
        SimpleNamespace(item_label="Gizlilik politikası bağlantısı bulunuyor", status=1),
        SimpleNamespace(item_label="Çerez politikası mevcut", status=1),
        SimpleNamespace(item_label="KVKK aydınlatma metni mevcut", status=0),
        SimpleNamespace(item_label="Açık rıza mekanizması doğru çalışıyor", status=0),
        SimpleNamespace(item_label="Veri sorumlusu iletişim bilgisi yayınlanmış", status=1),
    ]
    gdpr_items = [
        SimpleNamespace(item_label="Privacy Policy mevcut", status=1),
        SimpleNamespace(item_label="Cookie banner GDPR uyumlu", status=0),
        SimpleNamespace(item_label="Veri işleme amacı açıklanmış", status=1),
        SimpleNamespace(item_label="Kullanıcı hakları listesi mevcut", status=0),
    ]
    return render_template("result.html", scan=scan, kvkk_items=kvkk_items, gdpr_items=gdpr_items)
```

---

## 7. Sürüm Notu

- **v1.0** (mevcut): Yukarıdaki şema. Tüm 4 sayfa stabilize.
- İleride alan eklenirse (örn. `scan.scan_duration_ms`), bu doküman güncellenir ve değişiklik notları en üste eklenir.

---

**Soru/itiraz durumunda:** Üye 4 ile iletişime geçin. Bu sözleşmeyi tek taraflı değiştirmek **iki tarafı da kıracak** koordinasyonsuz değişiklikler yaratabilir.
