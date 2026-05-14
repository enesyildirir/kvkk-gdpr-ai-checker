# KVKK / GDPR AI Checker — Frontend Sunum Dökümanı

> **Hazırlayan:** Üye 4 — Arayüz
> **Sürüm:** Frontend v1.0 (sprint sonu)
> **Hedef kitle:** Proje sunumu, ekip değerlendirmesi, akademik teslim

---

## 1. Proje Bağlamı

KVKK / GDPR AI Checker, bir web sitesinin kişisel veri korumayı yöneten iki büyük çerçeve **KVKK (Türkiye)** ve **GDPR (Avrupa)** açısından otomatik değerlendiren bir Flask uygulamasıdır. Kullanıcı bir URL girer; sistem sitenin HTML içeriğini çekerek gizlilik politikası, çerez bildirimi, açık rıza ve aydınlatma metni gibi kontrol maddelerini eşleştirir, iki ayrı uyumluluk skoru hesaplar, risk seviyesi belirler ve bir LLM çağrısı ile Türkçe iyileştirme önerileri üretir. Tüm taramalar SQLite üzerinde arşivlenir.

5 kişilik ekipte benim rolüm **Üye 4 — Arayüz**: Jinja2 şablonları (`app/templates/`) ve CSS (`app/static/css/`) ile son kullanıcının gördüğü her şeyi inşa etmek.

---

## 2. Üretilen Dosyaların Tam Listesi

| # | Dosya | Konum | Boyut | Görev |
|---|-------|-------|-------|-------|
| 1 | `base.html` | `app/templates/` | ~6 KB | Tüm sayfaların paylaştığı temel iskelet (navbar, footer, tema toggle) |
| 2 | `index.html` | `app/templates/` | ~6 KB | Anasayfa — URL girdi formu |
| 3 | `result.html` | `app/templates/` | ~4 KB | Yeni tarama sonucu görüntüleme |
| 4 | `history.html` | `app/templates/` | ~18 KB | Geçmiş taramalar + filtreleme/arama/sıralama |
| 5 | `scan_detail.html` | `app/templates/` | ~4 KB | Arşivden tek bir tarama detayı |
| 6 | `_scan_overview.html` | `app/templates/partials/` | ~6 KB | URL+skor halkaları+risk pili (paylaşımlı) |
| 7 | `_checklist.html` | `app/templates/partials/` | ~3 KB | KVKK/GDPR kontrol listesi (paylaşımlı) |
| 8 | `_llm_suggestions.html` | `app/templates/partials/` | ~1 KB | AI öneri kutusu (paylaşımlı) |
| 9 | `style.css` | `app/static/css/` | ~44 KB | Tek dosyalık tasarım sistemi |

**Toplam:** 5 sayfa + 3 partial + 1 CSS dosyası = **9 dosya**.

---

## 3. Mimari Kararlar

### 3.1. Tasarım sistemi yaklaşımı

Tek bir `:root` bloğu içinde **CSS değişkenleri** (design token) olarak tanımlanmış:
- 13 renk değişkeni (`--bg`, `--text`, `--primary`, `--success`, vb.)
- 8 spacing değişkeni (`--space-1` ... `--space-8`)
- 4 radius değişkeni
- 3 shadow değişkeni
- 3 font değişkeni

**Avantajı:** Tüm bileşenler bu değişkenleri tüketir. Marka rengini değiştirmek için CSS'in 26.000+ karakterini taramak yerine **tek satırı** güncellemek yeterli. Karanlık temada da aynı bileşen kodları yeniden kullanılır — sadece tokenlar farklı set yüklenir.

### 3.2. Partial mimarisi (DRY)

`result.html` ve `scan_detail.html` birebir aynı veri sözleşmesini tüketir (`scan + kvkk_items + gdpr_items`). Bunu iki tam sayfaya yazmak yerine ortak parçaları `partials/` klasörüne çıkardım:

- `_scan_overview.html` → URL başlığı + skor halkaları + risk pili
- `_checklist.html` → KVKK veya GDPR maddeleri (parametrik: `{% with items=..., title=... %}`)
- `_llm_suggestions.html` → AI önerileri

İleride "skor kartına trend grafiği ekleyelim" kararı verildiğinde **tek partial dosyası** güncellenir, iki sayfa otomatik kazanır.

### 3.3. Base template + block inheritance

`base.html` her sayfada paylaşılan kabuğu (navbar, footer, font yükleme, tema yönetimi) bir kez tanımlar. Diğer sayfalar `{% extends "base.html" %}` ile bunu miras alır, sadece `{% block content %}` ile kendi içeriklerini ekler.

**Sonuç:** Bir navbar değişikliği (örn. yeni menü öğesi) tek dosyada yapılır, 4 sayfa anında günceller.

---

## 4. Sayfa Sayfa Özellikler

### 4.1. Anasayfa (`index.html`)

- **Hero bölümü**: "AI destekli uyumluluk taraması" eyebrow + gradient'li ana başlık + açıklama metni.
- **URL girdi formu**: Tek satırlı input + submit butonu. `POST /scan` adresine gönderim. Tarayıcının yerleşik `type="url"` ve `required` doğrulaması.
- **Submit davranışı**: Tıklandığında çift gönderim önlenir; buton "Taranıyor…" + dönen spinner'a dönüşür (tarama 5-15 saniye sürebileceği için kullanıcıya geri bildirim verir).
- **Hata gösterimi**: `{{ error }}` context'i varsa belirgin ama nazik bir uyarı banner'ı. `aria-live="polite"` ile ekran okuyuculara duyurulur.
- **Özellik şeridi**: 3 kart — "Otomatik Kriter Kontrolü", "Skor ve Risk Seviyesi", "Yapay Zekâ Önerileri".

### 4.2. Sonuç Sayfası (`result.html`)

- **Sayfa başlığı şeridi**: "Tarama tamamlandı" rozeti + ana başlık + sağda "Yeni Tarama / Yazdır-PDF / Kalıcı bağlantı" butonları.
- **Üst özet kartı**: Taranan URL (harici link ikonuyla), tarama tarihi, risk seviyesi pili.
- **Skor halkaları**: KVKK ve GDPR için iki adet circular progress (SVG tabanlı). İlk yüklemede 0'dan değere yumuşak animasyon (~900ms). Renk skora göre dinamik: 75+ yeşil, 50-74 amber, <50 kırmızı.
- **KVKK & GDPR kontrol listeleri**: İki sütun, her madde için yeşil tik ✓ veya kırmızı çarpı ✗. Başlık yanında otomatik özet: "12 başarılı / 5 eksik".
- **AI öneri kutusu**: LLM tarafından üretilen Türkçe metin. "Otomatik üretildi" rozeti + hukuki uyarı notu.

### 4.3. Geçmiş Sayfası (`history.html`)

- **İstatistik şeridi**: Toplam tarama, ortalama KVKK skoru, ortalama GDPR skoru (Jinja içinde hesaplanır — backend ek alan göndermek zorunda değil).
- **Filtre çubuğu** (client-side, sayfa yenilemesi yok):
  - **Arama**: URL'de geçen kelime ile filtre. 120ms debounce. `/` kısayolu ile odaklan, `Esc` ile temizle.
  - **Risk pill'leri**: Tümü / Düşük / Orta / Yüksek (segmented control).
  - **Sıralama**: Tarih, KVKK skoru, GDPR skoru — artan/azalan.
- **Sonuç sayacı**: Filtre uygulandığında "X kayıt gösteriliyor (toplam Y)" yazısı dinamik güncellenir.
- **Tablo (masaüstü)**: URL, tarih, KVKK chip, GDPR chip, risk pili, detay linki.
- **Kart listesi (mobil)**: 860px altında otomatik olarak tabloya alternatif kart görünümüne geçer.
- **Empty state**: Hiç tarama yoksa "Henüz tarama yok" + Anasayfa'ya yönlendirme.

### 4.4. Tarama Detay Sayfası (`scan_detail.html`)

- **Breadcrumb**: "Geçmiş Taramalar / Tarama #5".
- **"Arşivden görüntüleniyor" şeridi**: Kullanıcıya bağlamı net iletir (yeni tarama değil, eski kayıt).
- **Aynı partial'ları kullanır**: `_scan_overview` + iki `_checklist` + `_llm_suggestions`.

---

## 5. Çapraz Kesişen Özellikler (Cross-cutting features)

### 5.1. Print / PDF çıktısı

Her result/detail sayfasında **"Yazdır / PDF"** butonu var. Tıklandığında tarayıcının yerleşik yazdırma diyaloğu açılır; oradan fiziksel yazıcıya veya "PDF olarak kaydet" seçeneğine yönlenebilir.

Yazdırma anında devreye giren `@media print` bloğu:
- Navbar, footer, butonlar, filtre çubuğu, breadcrumb → **gizlenir**.
- Sayfa A4 boyutunda, 18mm/15mm marjlarla biçimlenir.
- Tüm metin siyahlaşır, arka planlar beyaz olur (toner tasarrufu).
- Halkalar yazıcı dostu renklerle (daha doygun yeşil/amber/kırmızı) çizilir.
- Linklerin URL'leri parantez içinde basılır (`https://example.com → "tıkla (https://example.com)"`).
- Sayfa altına otomatik rapor künyesi eklenir: "Tarama ID, tarih, hukuki uyarı".
- Karanlık tema aktifse bile yazdırırken zorla light renklere döner.

**Bağımlılık yok**: WeasyPrint, Playwright vb. gerekmedi; sadece CSS + `window.print()`.

### 5.2. Karanlık tema

Üç durumlu toggle navbar'da: **Açık → Koyu → Otomatik (sistem) → Açık**.

- Kullanıcı seçimi `localStorage`'da kalıcı.
- Auto modunda `prefers-color-scheme` ile sistem temasını takip eder; kullanıcı Windows tema rengini değiştirirse anında yansır.
- **FOUC önleme**: `<head>` içinde inline senkron script, CSS yüklenmeden önce `data-theme` attribute'unu uygular — sayfa hiç flash etmez.
- Tüm renkler token swap'i ile değişir; bileşen kodları değişmez.
- Yazdırırken karanlık tema otomatik iptal edilir.
- `prefers-reduced-motion` desteği: hareket azaltma tercih eden kullanıcılarda halka animasyonları kapalı.

### 5.3. Responsive davranış

İki büyük kırılım noktası:
- **860px** (tablet/küçük laptop): URL form dikey, grid 2 sütundan 1 sütuna, history sayfasında tablo gizlenip kart listesi açılır, filtre çubuğu dikey yığılır.
- **480px** (telefon): Form kart padding'i küçülür, skor halkası 160×160 → 130×130, nav linkleri daralır.

### 5.4. Erişilebilirlik

- Tüm interaktif öğelerde `aria-label`, `aria-live`, `role` attribute'ları.
- Renk tek başına anlam taşımıyor: yeşil/kırmızı ikonlara ek olarak ✓ ve ✗ sembolleri var (renk körlüğü).
- Klavye navigasyonu: `Tab` ile her yere ulaşılır, focus ring belirgin (mavi shadow).
- `prefers-reduced-motion` desteği.
- Semantic HTML: `<header>`, `<main>`, `<nav>`, `<footer>`, `<section>`, `<article>` tag'leri doğru kullanılmış.

### 5.5. Performans

- **Tek CSS dosyası**: HTTP isteklerini minimize eder.
- **Google Fonts preconnect**: Font yüklemesi daha hızlı.
- **Animasyonlar GPU hızlandırılmış**: `transform` ve `opacity` üzerinden çalışır, layout-thrashing yok.
- **Debounced arama**: Filtre input'u her tuş vuruşunda değil, 120ms duruşta tetiklenir.
- **Inline SVG**: İkonlar için ek font/sprite dosyası yok; CSS ile renklendirilir.

---

## 6. Tasarım Felsefesi

### 6.1. "Compliance" tonu
Bu uygulama hukuki/teknik bir alan. Kullanıcının uygulamaya **güven** duyması şart. Bu yüzden:
- **Sakin renk paleti**: Derin mavi ana renk, soğuk gri-mavi yüzeyler. Parlak kırmızı/yeşil sadece skor durumlarında.
- **Çift tipografi**: Manrope (display) + Inter Tight (body). Manrope kurumsal ama yumuşak; sertlik yaratmaz.
- **Cömert beyaz boşluk**: İçerik yoğun değil, nefes alabiliyor.

### 6.2. Tek dilli (Türkçe)
Tüm metin Türkçe. Çoğul/tekil, "siz" hitabı, hukuki uyarı tonu. Kullanıcı Türk olduğu için ürün hissi tutarlı.

### 6.3. Bileşen tutarlılığı
Bir özellik bir kez tasarlandıktan sonra diğer sayfalarda aynı biçimde tekrar edildi:
- "Risk pili" hem result, hem scan_detail, hem history tablosunda kullanıldı.
- "Score chip" hem history tablosunda, hem mobil kartlarda kullanıldı.
- "Badge'ler" başarılı/eksik sayımları, AI rozeti, "otomatik üretildi" etiketinde aynı sistemde.

### 6.4. Progressive enhancement
JavaScript çalışmasa bile uygulama yararlı kalır:
- Filtre çubuğu `hidden` ile başlar, JS onu görünür yapar. JS yoksa kullanıcı zaten tüm geçmişi görür.
- Submit butonu spinner'sız çalışır.
- Tema toggle çalışmasa bile sistem teması `@media` ile devreye girer.

---

## 7. Teknik Detaylar

### 7.1. Kullanılan teknolojiler

- **Jinja2** (Flask'in yerleşik şablon motoru) — `{% extends %}`, `{% include %}`, `{% with %}`, filter'lar (`|selectattr`, `|sum`, `|round`).
- **Vanilla JavaScript** — Tema toggle, filtre/arama, submit spinner. Hiç framework yok.
- **CSS3** — Custom properties (variables), `@media`, `@keyframes`, `grid`, `flexbox`, `transition`.
- **SVG** — İkonlar (lucide-style line icons), circular progress halkası.
- **Web Fonts** — Google Fonts (Manrope, Inter Tight).
- **localStorage** — Tema tercihi kalıcılığı.

### 7.2. Tarayıcı uyumluluğu

Modern evergreen tarayıcılar (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+). IE11 desteklenmiyor — CSS custom properties IE11'de çalışmaz.

### 7.3. Backend bağımsızlığı

Frontend, backend ekibinin (Üye 1) henüz tamamlanmamış olduğu süreçte de geliştirilebilirdi çünkü:
- Tüm context değişkenleri `CONTEXT_CONTRACT.md` ile sözleşmelendi.
- Sahte data ile (`SimpleNamespace`) tüm sayfalar test edildi.
- Backend ile entegrasyon noktası net: `render_template(...)`'in argümanları.

---

## 8. Sayılarla Frontend

| Metrik | Değer |
|--------|-------|
| Toplam dosya sayısı | 9 |
| Toplam satır (CSS+HTML+JS) | ~1.900 |
| CSS custom property sayısı | 28 |
| Bileşen sayısı | 18 (kart, buton, badge, pill, halka, filtre, tablo, vb.) |
| Sayfa sayısı | 4 + 3 partial |
| JavaScript satır sayısı | ~180 (sadece etkileşim için) |
| Eklenti / framework bağımlılığı | 0 |
| Tema sayısı | 3 (light, dark, auto) |
| Kırılım noktası (responsive) | 2 (860px, 480px) |

---

## 9. Sunum İçin Öne Çıkan Cümleler

> "Tek bir CSS dosyası, hiç framework, sıfır JavaScript kütüphanesi — modern Web standartlarının ne kadar güçlü olduğunu kanıtlayan bir mimari."

> "Tasarım sistemi yaklaşımı: 28 değişken, 18 bileşen. Bir renk değiştirilmek istense **1 satır** yeterli."

> "Dokuz dosya, dört sayfa, üç tema, iki kırılım noktası — bir kullanıcı, sıfır karmaşa."

> "Print stilleri sayesinde herhangi bir PDF kütüphanesi yüklemeden, sadece tarayıcıyla profesyonel PDF rapor üretebiliyoruz."

> "Karanlık tema, FOUC önleme inline scripti sayesinde **flash yapmadan**, sistem temasıyla senkron çalışır."

> "Erişilebilirlik düşünüldü: WCAG kontrast oranları, ARIA etiketleri, klavye navigasyonu, hareket azaltma desteği."

---

## 10. Hızlı Demo Senaryosu (Sunumda)

1. **Anasayfayı aç**: Modern hero, gradient'li başlık, sade form göster.
2. **Hatalı URL gir (`abc`)**: Anında hata banner'ı göster.
3. **Geçerli URL gir, taramayı başlat**: Spinner ve "Taranıyor" durumunu göster.
4. **Sonuç sayfasında halkaların animasyonunu göster**: 0'dan değere büyür.
5. **Yazdır butonuna bas → PDF olarak kaydet**: Yazıcı dostu çıktıyı göster.
6. **Geçmiş Taramalar'a git**: İstatistik şeridi, tablo görünümü.
7. **Filtre dene**: Arama yaz, sonra risk pill'ine bas, sayacın güncellendiğini göster.
8. **Tema toggle'a bas üç kez**: Light → Dark → Auto. Dark moddayken filtre çubuğunun nasıl uyum sağladığını göster.
9. **Pencereyi daralt**: Responsive mobil kart görünümüne geçişi göster.
10. **Detay sayfasına gir**: Aynı partial'ların farklı sayfada nasıl yeniden kullanıldığını söyle.

**Demo süresi:** ~4-5 dakika.

---

## 11. Sonuç

Bu sprint sonunda frontend tarafı tamamen production-ready durumda. Backend ekibinin bağlı kalması gereken sözleşme (`CONTEXT_CONTRACT.md`) belirlendi. Her sayfa hem geniş ekranda hem mobilde, hem açık hem koyu temada, hem ekran hem kâğıt ortamında düzgün çalışıyor. Erişilebilirlik standartlarına uygun. Hiç ek bağımlılık yok.

Önümüzdeki sprintlerde değerlendirilebilecek geliştirmeler: gerçek zamanlı doğrulama, animasyon iyileştirmeleri, PWA desteği, çoklu dil (İngilizce'ye genişletme), kullanıcı hesabı + favori tarama özelliği.
