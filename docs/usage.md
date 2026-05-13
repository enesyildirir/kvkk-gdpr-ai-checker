# Kullanım Kılavuzu — AI Destekli KVKK/GDPR Uyumluluk Kontrol Uygulaması

---

## 1. Gereksinimler

- Python 3.10 veya üzeri
- [Ollama](https://ollama.com) kurulu ve çalışır durumda
- İnternet bağlantısı (web sitelerini analiz etmek için)

---

## 2. Kurulum

### Adım 1 — Repoyu klonla

```bash
git clone https://github.com/kullanici-adi/ai-kvkk-gdpr-checker.git
cd ai-kvkk-gdpr-checker
```

### Adım 2 — Sanal ortamı oluştur ve aktif et

```bash
# Windows
python -m venv .venv --without-pip
.venv\Scripts\activate

# Mac / Linux
python -m venv .venv --without-pip
source .venv/bin/activate
```

### Adım 3 — pip ve bağımlılıkları yükle

```bash
python -m ensurepip --upgrade
pip install -r requirements.txt
```

### Adım 4 — .env dosyasını oluştur

`.env.example` dosyasını kopyala, adını `.env` yap ve içini doldur:

```bash
# Windows
copy .env.example .env

# Mac / Linux
cp .env.example .env
```

`.env` içeriği:

```
FLASK_SECRET_KEY=buraya-uzun-rastgele-bir-yazi-yaz
FLASK_ENV=development
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
```

### Adım 5 — Ollama modelini indir

```bash
ollama pull llama3.2:3b
```

> İlk indirme ~2GB sürer.

---

## 3. Uygulamayı Çalıştırma

```bash
python run.py
```

Terminalde şunu görürsen uygulama hazır demektir:

```
* Running on http://127.0.0.1:5000
```

Tarayıcında `http://127.0.0.1:5000` adresini aç.

> **Not:** Her çalıştırmadan önce Ollama'nın arka planda açık olduğundan emin ol.

---

## 4. Kullanım

### Analiz Başlatma

1. Ana sayfaya git: `http://127.0.0.1:5000`
2. URL giriş kutusuna analiz etmek istediğin siteyi yaz (örn: `orneksite.com`)
3. **Analiz Et** butonuna tıkla
4. Sonuç ~10-30 saniye içinde gelir (AI önerileri biraz zaman alır)

### Sonuç Sayfası

Analiz tamamlandığında şunları göreceksin:

- **KVKK Skoru** — 0-100 arası puan
- **GDPR Skoru** — 0-100 arası puan
- **Risk Seviyesi** — Düşük / Orta / Yüksek
- **Kontrol Listesi** — hangi maddelerin geçip geçmediği
- **AI Önerileri** — eksiklikler için Türkçe düzeltme önerileri

### Rapor İndirme

Sonuç sayfasının altında iki buton bulunur:

- **JSON İndir** — makine tarafından okunabilir format
- **HTML Rapor İndir** — tarayıcıda açılabilir görsel rapor

### Geçmiş Taramalar

Sağ üstteki **Geçmiş Taramalar** linkine tıklayarak daha önce yapılan tüm analizleri listele ve detaylarına bak.

---

## 5. Sık Karşılaşılan Hatalar

| Hata | Neden | Çözüm |
|---|---|---|
| `Siteye bağlanılamadı` | Site erişilemez veya URL yanlış | URL'yi kontrol et, `https://` ile başladığından emin ol |
| `LLM'e bağlanılamadı` | Ollama çalışmıyor | `ollama serve` komutunu çalıştır |
| `Servisler henüz entegre edilmedi` | Geliştirme aşamasında | Ekip modüllerini tamamlayana kadar beklenen durum |
| `500 Internal Server Error` | Kod hatası | Terminaldeki hata mesajını ekibe ilet |

---

## 6. Geliştirici Notları

- Uygulama `debug=True` modunda çalışır — production'da kapatılmalı
- Veritabanı `instance/app.db` dosyasına kaydedilir, otomatik oluşur
- Üretilen raporlar `reports/` klasörüne kaydedilir
- Detaylı mimari için → `docs/architecture.md`
- Katkı kuralları için → `CONTRIBUTING.md`

---

*Son güncelleme: Nisan 2026*
