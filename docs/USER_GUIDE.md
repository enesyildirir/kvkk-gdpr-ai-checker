# Kullanıcı Kılavuzu — KVKK / GDPR AI Checker

> Bu doküman, son kullanıcı (uygulamayı kullanan kişi) için arayüzdeki tüm etkileşimleri ve özellikleri açıklar.

---

## Genel Yerleşim

Uygulamanın her sayfasında üstte aynı **navigasyon çubuğu** ve altta aynı **alt bilgi** bulunur. Arada içerik değişir.

### Navigasyon çubuğu (her sayfada)

| Öğe | İşlevi |
|-----|--------|
| **K/G logo** (sol) | Anasayfaya gider. |
| **Anasayfa** linki | URL girip yeni tarama yapma sayfası. |
| **Geçmiş Taramalar** linki | Daha önce yaptığınız tüm taramaların listesi. |
| **Tema değiştirici** ikon | Açık / Koyu / Otomatik mod arası geçiş (aşağıda detaylı anlatıldı). |

---

## 1. Anasayfa — Yeni Tarama Yapmak

Tarayıcıdan `http://127.0.0.1:5000` adresini açtığınızda buraya gelirsiniz.

### URL girdi formu

1. Ortadaki büyük metin kutusuna **tam URL** yazın.
   - Doğru örnek: `https://example.com`
   - Yanlış örnek: `example.com` (başında `https://` olmalı)
2. **Taramayı Başlat** butonuna basın.
3. Buton "Taranıyor…" yazısına dönüşür ve dönen bir gösterge belirir. Bu **5 ila 15 saniye** sürebilir; sayfayı yenilemeyin veya kapatmayın.

### Hata mesajları

URL geçersizse veya site erişilemez ise formun üstünde kırmızı bir uyarı kutusu çıkar:
> ⚠ İşlem gerçekleştirilemedi. (Hatanın detayı burada)

Hata sonrası tekrar deneyebilirsiniz.

### Bilgi kartları

Form altında **üç tanıtım kartı** bulunur:
- **Otomatik Kriter Kontrolü** — Gizlilik politikası, çerez bildirimi gibi maddelerin nasıl tarandığı.
- **Skor ve Risk Seviyesi** — KVKK ve GDPR için ayrı skor + risk değerlendirmesi.
- **Yapay Zekâ Önerileri** — LLM destekli Türkçe iyileştirme önerileri.

---

## 2. Sonuç Sayfası — Tarama Sonuçlarını Okumak

Tarama tamamlandığında otomatik olarak buraya yönlendirilirsiniz.

### Üst başlık şeridi

- Yeşil "Tarama tamamlandı" rozeti.
- "Sonuç Raporu" başlığı.
- Sağda üç buton:
  - **Yeni Tarama** → Anasayfaya döner, yeni URL girebilirsiniz.
  - **Yazdır / PDF** → Tarayıcının yazdırma penceresini açar (detayı aşağıda).
  - **Kalıcı bağlantı** → Bu taramanın URL'sini gösterir (sonradan paylaşmak için).

### Tarama özet kartı

Tek satırda toplu bilgi:
- **Taranan URL**: Tıklanabilir; siteyi yeni sekmede açar.
- **Tarama tarihi**: Gün/ay/yıl + saat.
- **Risk seviyesi pili**: Düşük / Orta / Yüksek (renk ve nokta ile).

### Skor halkaları

İki adet daire şeklinde gösterge:

- **KVKK Uyum Skoru**: 0-100 arası.
- **GDPR Uyum Skoru**: 0-100 arası.

Halkanın rengi skorunuza göre değişir:
- 🟢 **75-100** → Yeşil (iyi durum)
- 🟡 **50-74** → Amber/Turuncu (geliştirilebilir)
- 🔴 **0-49** → Kırmızı (kritik eksikler var)

> Sayfa ilk yüklendiğinde halkalar 0'dan başlayıp skorunuza kadar yumuşakça büyür. Bu animasyon yaklaşık 1 saniye sürer.

### Kontrol listeleri

İki sütun, yan yana:

**KVKK Maddeleri** ve **GDPR Maddeleri** ayrı bölümlerde sunulur. Her madde için:
- ✅ **Yeşil tik + yeşil sol kenar** → Bu kriter karşılanmış.
- ❌ **Kırmızı çarpı + kırmızı sol kenar** → Bu kriter eksik.

Her bölümün başında otomatik özet rozet vardır:
> ✓ 12 başarılı   ✗ 5 eksik

### Yapay Zekâ Önerileri kutusu

Sayfanın en altında, "AI" rozetli bir bölümde tespit edilen eksiklerin **nasıl düzeltileceğine dair Türkçe öneriler** yer alır. Bu metin bir dil modeli (LLM) tarafından üretilmiştir.

Altında bir hukuki uyarı: *"Bu öneriler bir dil modeli tarafından üretildi, hukuki danışmanlık yerine geçmez."*

---

## 3. Geçmiş Taramalar — Arşivi Yönetmek

Navbar'daki **Geçmiş Taramalar** linkine basarak ulaşılır (`/history`).

### İstatistik şeridi (üstte)

Üç sayı tek bakışta:
- **Toplam Tarama** — Şimdiye kadar yapılan tarama sayısı.
- **Ortalama KVKK** — Tüm taramaların KVKK skor ortalaması.
- **Ortalama GDPR** — Tüm taramaların GDPR skor ortalaması.

### Filtre çubuğu

Üç araç tek satırda:

#### 🔍 Arama kutusu
- URL'de geçen herhangi bir kelimeyi yazın (örn. "github").
- Eşleşmeyen satırlar anında gizlenir.
- Yazdığınızı X butonuyla temizleyebilirsiniz.
- **Klavye kısayolu**: `/` tuşuna basarak doğrudan kutuya odaklanın. `Esc` tuşuyla temizleyin.

#### ⚪ Risk pill'leri (sağında)
**Tümü / Düşük / Orta / Yüksek** sekmeleri:
- Birine basınca sadece o risk seviyesine ait taramalar görünür.
- "Tümü" varsayılan.

#### ⬇ Sıralama dropdown'ı (en sağda)
Şu seçenekleri sunar:
- En yeni önce (varsayılan)
- En eski önce
- KVKK skoru (düşük → yüksek)
- KVKK skoru (yüksek → düşük)
- GDPR skoru (düşük → yüksek)
- GDPR skoru (yüksek → düşük)

### Filtre sonuç sayacı

Filtre uygulandığında çubuğun altında dinamik mesaj:
> **5** kayıt gösteriliyor *(toplam 23)*

### Tarama listesi

**Masaüstünde (geniş ekran)** — Tablo görünümü:

| Sütun | Açıklama |
|-------|----------|
| URL | Taranan sitenin adresi (kısaltılır, üzerine gelince tam görünür). |
| Tarih | Tarama tarih ve saati. |
| KVKK | Renkli skor "chip" (yeşil/amber/kırmızı). |
| GDPR | Aynı şekilde. |
| Risk | Risk pili. |
| Detay | "Detay →" butonu, ayrıntı sayfasına gider. |

**Mobilde (dar ekran)** — Kart görünümü:
Her tarama bir kart olarak gösterilir. Karta tıklamak detay sayfasını açar.

### Hiç kayıt yoksa

İlk kez kullanıyorsanız boş durum kartı görünür:
> 📋 Henüz bir tarama yok
> Anasayfadan bir URL girerek ilk taramanızı başlatabilirsiniz.

[ **Hemen Başla** ] butonu ile anasayfaya yönlenirsiniz.

### Filtre sonucu boşsa

Aramanız hiçbir kayıtla eşleşmezse:
> "Arama veya filtre kriterlerine uyan kayıt bulunamadı."

---

## 4. Tarama Detayı — Arşivden Bir Taramayı Yeniden Görmek

Geçmiş listesinden bir taramaya tıklayınca buraya gelirsiniz (`/scan/5` gibi).

### Konum belirteci (breadcrumb)

Sayfa tepesinde:
> Geçmiş Taramalar / Tarama #5

Geçmiş bağlantısına basarak arşive dönebilirsiniz.

### Sayfa başlığı

- **"Arşivden görüntüleniyor"** rozeti (yeni bir tarama değil, eski kayıt olduğunu belirtir).
- "Tarama Detayı" başlığı.
- Sağda butonlar:
  - **Geçmişe Dön**
  - **Yazdır / PDF**
  - **Yeni Tarama**

### İçerik

Sonuç sayfasıyla **aynı yapı**: Üst özet kartı + iki skor halkası + iki kontrol listesi + AI önerileri kutusu. Tek farkı yukarıdaki konum belirteci ve rozet.

---

## 5. Yazdır / PDF Oluştur

Result veya scan_detail sayfasındaki **Yazdır / PDF** butonuna basın (veya `Ctrl + P` klavye kısayolu).

### Açılan yazdırma penceresinde

- **Hedef** dropdown'ından "Mikrosoft Print to PDF" veya "Save as PDF" seçeneğini seçebilirsiniz.
- Önizlemede şunları göreceksiniz:
  - Navbar, footer, butonlar **görünmez**.
  - URL, tarih, risk seviyesi **belirgin** üst bilgi olarak.
  - Skor halkaları kompakt boyutta renkli.
  - Kontrol listeleri yan yana, ikonlu.
  - Sayfa altında **rapor künyesi**: "Tarama ID, tarih, hukuki uyarı".
- A4 boyutu, kenar boşluklarıyla profesyonel görünüm.

### Karanlık temadayken yazdırma

Karanlık modda olsanız bile çıktı **otomatik olarak açık renklere döner** — toner tasarrufu için.

---

## 6. Tema Değiştirme

Navbar'ın en sağındaki ikon butona basarak temayı değiştirin:

| İkon | Mod | Davranış |
|------|-----|----------|
| ☀ | **Açık tema** | Beyaz arka plan, koyu yazılar (varsayılan). |
| 🌙 | **Koyu tema** | Koyu lacivert arka plan, açık yazılar. Gece kullanım için ideal. |
| ◐ | **Otomatik** | Bilgisayarınızın sistem ayarına göre otomatik. Windows "Karanlık moda al" deyince uygulama da geçer. |

Her tıkta sırayla bir sonraki moda geçer (Açık → Koyu → Otomatik → Açık...).

### Tercihiniz kalıcı

Seçtiğiniz tema tarayıcıda saklanır. Sayfayı yenilesek, kapatıp tekrar açsanız da hatırlanır. "Otomatik" modunu seçerseniz bilgisayarın sistem teması neyse onu takip eder.

---

## 7. Klavye Kısayolları

| Kısayol | Etki |
|---------|------|
| `Tab` | Tıklanabilir bir sonraki öğeye geç. |
| `Shift + Tab` | Önceki öğeye dön. |
| `Enter` veya `Space` | Üzerinde durduğunuz butona bas. |
| `Ctrl + P` | Yazdırma penceresini aç (yazdırılabilir sayfalarda). |
| `/` | History sayfasında: arama kutusuna doğrudan odaklan. |
| `Esc` | Arama kutusundayken: aramayı temizle. |

---

## 8. Mobil Cihazda Kullanım

Telefon veya tabletten girdiğinizde:
- Navbar daralır.
- Form butonları tüm genişliği kaplar.
- Skor halkaları daha küçük boyutta gösterilir.
- Geçmiş listesi tablo yerine **kart yığını** olarak görünür — yatayda kaydırma yapmak zorunda kalmazsınız.
- Filtre çubuğu dikey istiflenir.

Her şey dokunmatik için optimize edilmiştir; çift tıklamaya, kaydırmaya gerek kalmaz.

---

## 9. Erişilebilirlik Notları

- Tüm renkler **WCAG AA** kontrast standardını karşılar.
- Renk körü kullanıcılar için: yeşil/kırmızı sadece renk değil, ✓/✗ ikonlarıyla da gösterilir.
- Ekran okuyucu kullanıcıları için: tüm interaktif öğelerde uygun ARIA etiketleri var.
- Hareket hassasiyeti olan kullanıcılar: tarayıcı ayarınızda "azaltılmış hareket" tercih ettiyseniz halka animasyonları otomatik kapatılır.
- Sayfa **klavye-yalnız** gezilebilir.

---

## 10. SSS (Sık Sorulan Sorular)

**Tarama ne kadar sürer?**
Genellikle 5-15 saniye. Site ağır yükleniyorsa 30 saniyeye kadar çıkabilir.

**Sonuçlar kaydediliyor mu?**
Evet, her tarama otomatik olarak geçmişe eklenir.

**Bu rapor hukuki olarak bağlayıcı mı?**
Hayır. Akademik / teknik bir ön değerlendirme aracıdır. Resmi bir uyumluluk denetimi için sertifikalı bir KVKK / GDPR danışmanına başvurun.

**AI önerileri ne kadar güvenilir?**
Bir dil modeli tarafından üretilen genel kılavuzlardır. Spesifik bir hukuki tavsiye değil; başlangıç noktası olarak değerlendirin.

**Skorum %100 olsa bile yine de problem olabilir mi?**
Evet — bu uygulama sayfa içeriğinin **otomatik kontrol** edebileceği maddeleri tarar. Veri saklama politikası, çalışan eğitimi gibi süreçsel uyumluluk maddeleri otomatik değerlendirilemez.

**Aynı siteyi tekrar tarayabilir miyim?**
Evet. Her tarama ayrı bir kayıt olarak saklanır; zamanla iyileştirmeleri takip edebilirsiniz.
