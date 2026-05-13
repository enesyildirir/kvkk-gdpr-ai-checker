# Mimari Dokümantasyon — AI Destekli KVKK/GDPR Uyumluluk Kontrol Uygulaması

> Bu doküman, projeye yeni katılan ekip üyelerinin sistemi hızlıca anlaması için hazırlanmıştır.

---

## 1. Projenin Amacı

Kullanıcıdan alınan bir web sitesi URL'sini otomatik olarak analiz ederek:
- Gizlilik politikası, çerez politikası ve KVKK aydınlatma metni varlığını kontrol etmek
- KVKK ve GDPR uyumluluk skoru üretmek
- Risk seviyesini belirlemek
- Yapay zekâ destekli Türkçe düzeltme önerileri sunmak
- Tarama geçmişini kaydetmek ve raporlamak

**Önemli Not:** Uygulama hukuki danışmanlık sağlamaz. Sonuçlar yalnızca teknik ön değerlendirme amacı taşır.

---

## 2. Genel Sistem Akışı

```
Kullanıcı → URL girer
     ↓
[crawler.py] → Web sitesinin HTML içeriğini çeker
     ↓
[parser.py] → Gizlilik politikası, çerez politikası, KVKK metinlerini tespit eder
     ↓
[compliance_checker.py] → KVKK/GDPR kontrol listesine göre değerlendirme yapar
     ↓
[llm_service.py] → Ollama (llama3.2:3b) ile Türkçe öneriler üretir
     ↓
[scan_service.py] → Tüm süreci koordine eder, skoru hesaplar
     ↓
[scan_repository.py] → Sonuçları SQLite veritabanına kaydeder
     ↓
[report_service.py] → JSON veya HTML rapor üretir
     ↓
Kullanıcı → Sonucu görüntüler / raporu indirir
```

---

## 3. Klasör Yapısı ve Dosyaların Görevleri

```
ai-kvkk-gdpr-checker/
│
├── app/                          → Uygulamanın ana dizini
│   ├── __init__.py               → Flask uygulamasını başlatır
│   ├── routes.py                 → URL yönlendirmeleri (endpoint'ler)
│   ├── config.py                 → .env dosyasından ayarları okur
│   ├── database.py               → SQLite bağlantısını yönetir
│   │
│   ├── models/                   → Veri modelleri
│   │   ├── scan.py               → Tarama objesi (URL, skor, tarih...)
│   │   └── scan_item.py          → Tek bir kontrol maddesi objesi
│   │
│   ├── repositories/             → Veritabanı işlemleri
│   │   └── scan_repository.py    → Tarama kaydet / listele / getir
│   │
│   ├── services/                 → İş mantığı (core logic)
│   │   ├── crawler.py            → Web sitesi HTML'ini çeker
│   │   ├── parser.py             → HTML'den ilgili metinleri ayıklar
│   │   ├── compliance_checker.py → Kontrol listesine göre analiz yapar
│   │   ├── llm_service.py        → Ollama API'siyle iletişim kurar
│   │   ├── scan_service.py       → Tüm servisleri koordine eder
│   │   └── report_service.py     → Rapor üretir (JSON/HTML)
│   │
│   ├── templates/                → HTML arayüz şablonları
│   │   ├── index.html            → Ana sayfa (URL giriş formu)
│   │   ├── result.html           → Analiz sonuç sayfası
│   │   ├── history.html          → Geçmiş taramalar listesi
│   │   └── scan_detail.html      → Tek tarama detay sayfası
│   │
│   └── static/                   → CSS ve JavaScript dosyaları
│       ├── css/
│       └── js/
│
├── data/
│   └── kvkk_gdpr_checklist.json  → Kontrol listesi (tüm maddeler burada)
│
├── instance/
│   └── app.db                    → SQLite veritabanı dosyası
│
├── reports/                      → Üretilen raporlar burada saklanır
│
├── tests/                        → Otomatik testler
│   ├── test_crawler.py
│   ├── test_parser.py
│   ├── test_compliance_checker.py
│   ├── test_scan_service.py
│   └── test_scan_repository.py
│
├── docs/                         → Dokümantasyon
│   ├── architecture.md           → Bu dosya
│   ├── database.md               → Veritabanı şeması
│   └── usage.md                  → Kullanım kılavuzu
│
├── .env                          → Gizli ayarlar (repoya eklenmez!)
├── .env.example                  → .env şablonu (repoya eklenir)
├── .gitignore                    → Git'e gönderilmeyecek dosyalar
├── requirements.txt              → Python bağımlılıkları
├── README.md                     → Proje tanıtımı
└── run.py                        → Uygulamayı başlatan dosya
```

---

## 4. Servisler Arası İlişki

```
routes.py
   └── scan_service.py          ← Merkezi koordinatör
         ├── crawler.py         ← HTML çekme
         ├── parser.py          ← Metin ayıklama
         ├── compliance_checker.py  ← Analiz
         ├── llm_service.py     ← AI öneriler
         ├── scan_repository.py ← Veritabanı
         └── report_service.py  ← Rapor
```

`scan_service.py` tüm servisleri sırayla çağırır. Diğer servisler birbirinden bağımsızdır — bu sayede her ekip üyesi kendi modülünü bağımsız geliştirebilir.

---

## 5. Kullanılan Teknolojiler

| Teknoloji | Kullanım Amacı |
|---|---|
| Python 3.10 | Ana programlama dili |
| Flask | Web framework |
| requests | Web sitesi HTML'ini çekme |
| BeautifulSoup4 | HTML parse etme |
| SQLite | Veritabanı |
| Ollama (llama3.2:3b) | Yerel LLM — Türkçe öneriler |
| python-dotenv | .env dosyasını okuma |
| HTML/CSS/JS | Arayüz |

---

## 6. Ekip İş Bölümü Önerisi

| Üye | Sorumluluk | İlgili Dosyalar |
|---|---|---|
| Üye 1 | Veri Toplama | `crawler.py`, `parser.py`, `scan_service.py` |
| Üye 2 | Uyumluluk Analizi | `compliance_checker.py`, `kvkk_gdpr_checklist.json` |
| Üye 3 | AI Entegrasyonu | `llm_service.py` |
| Üye 4 | Arayüz | `routes.py`, `templates/`, `static/` |
| Üye 5 | Veritabanı & Raporlama | `database.py`, `models/`, `repositories/`, `report_service.py` |

> Her üye kendi modülünü geliştirirken `scan_service.py`'yi referans alsın. Servisler arası bağlantı orada kurulur.

---

## 7. Ortam Kurulumu (Özet)


```bash
# 1. Sanal ortamı oluştur ve aktif et
python -m venv .venv --without-pip
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux

# 2. Bağımlılıkları yükle
python -m ensurepip --upgrade
pip install -r requirements.txt

# 3. .env dosyasını oluştur (.env.example'dan kopyala)
# OLLAMA_BASE_URL ve OLLAMA_MODEL değerlerini doldur

# 4. Ollama'yı başlat ve modeli indir
ollama pull llama3.2:3b

# 5. Uygulamayı çalıştır
python run.py
```

---

## 8. Önemli Notlar

- `.env` dosyası **asla** Git'e gönderilmez. Her ekip üyesi kendi `.env` dosyasını `.env.example`'dan oluşturur.
- `instance/app.db` dosyası Git'e gönderilmez, uygulama ilk çalıştığında otomatik oluşur.
- Ollama'nın arka planda çalışıyor olması gerekir (`ollama serve` veya uygulama açıkken).
- Tüm servisler Türkçe hata mesajı ve öneri üretecek şekilde tasarlanmalıdır.

---

*Son güncelleme: Nisan 2026*
