# Görev Kartları — AI Destekli KVKK/GDPR Uyumluluk Kontrol Uygulaması

> Her üye yalnızca kendi kartındaki dosyaları yazar. Başkasının dosyasına dokunmadan önce haber ver.

---

## Üye 2 — Uyumluluk Analizi

**Dosya:** `app/services/compliance_checker.py`

**Görev:** `parser.py`'den gelen tespit sonuçlarını `data/kvkk_gdpr_checklist.json` ile karşılaştırarak uyumluluk skoru üret.

**Yazacağın fonksiyon:**

```python
def run_checks(detected_sections: dict) -> dict:
```

**Girdi (`detected_sections`):**
```python
{
    "has_privacy_policy": True,
    "has_cookie_policy": False,
    "has_kvkk_text": True,
    "has_consent_mechanism": False,
    "has_retention_info": False,
    "has_user_rights": False,
    "has_data_processing_info": False
}
```

**Döndürmesi gereken:**
```python
{
    "kvkk_score": 35.0,        # 0-100 arası float
    "gdpr_score": 20.0,        # 0-100 arası float
    "risk_level": "Yüksek Risk",  # "Düşük Risk" / "Orta Risk" / "Yüksek Risk"
    "kvkk_items": [...],       # list[ScanItem]
    "gdpr_items": [...]        # list[ScanItem]
}
```

**Risk seviyesi kuralı:**
- 80 ve üzeri → Düşük Risk
- 50-79 arası → Orta Risk
- 50 altı → Yüksek Risk

**Referans dosyalar:**
- `data/kvkk_gdpr_checklist.json` → kontrol maddeleri ve ağırlıklar
- `app/models/scan_item.py` → ScanItem sınıfı
- `app/services/scan_service.py` → entegrasyon noktası

---

## Üye 3 — AI Entegrasyonu

**Dosya:** `app/services/llm_service.py`

**Görev:** Analiz sonuçlarını Ollama API'sine göndererek Türkçe düzeltme önerileri üret.

**Yazacağın fonksiyon:**

```python
def generate_suggestions(detected_sections: dict, relevant_text: str,
                          kvkk_score: float, gdpr_score: float) -> str:
```

**Girdi:**
- `detected_sections` → `parser.py`'den gelen `True/False` sözlüğü
- `relevant_text` → `parser.py`'den gelen özet metin
- `kvkk_score`, `gdpr_score` → `compliance_checker.py`'den gelen skorlar

**Döndürmesi gereken:**
```python
"1. Gizlilik Politikası: Web sitenize bir gizlilik politikası sayfası ekleyin..."
# Türkçe, madde madde, düz string
```

**Ollama API çağrısı:**
```python
requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "llama3.2:3b", "prompt": "...", "stream": False}
)
# Yanıt: response.json()["response"]
```

**Önemli:** Prompt'u Türkçe yaz ve modele yalnızca Türkçe yanıt vermesini söyle. Bağlantı hatalarını yakala, hata mesajı da Türkçe olsun.

**Referans dosyalar:**
- `app/config.py` → `Config.OLLAMA_BASE_URL`, `Config.OLLAMA_MODEL`
- `app/services/scan_service.py` → entegrasyon noktası

---

## Üye 4 — Arayüz

**Dosyalar:**
- `app/templates/index.html`
- `app/templates/result.html`
- `app/templates/history.html`
- `app/templates/scan_detail.html`
- `app/static/css/`
- `app/static/js/` (isteğe bağlı)

**Görev:** Flask Jinja2 şablonları ile kullanıcı arayüzünü yaz.

**Her sayfada kullanılacak değişkenler:**

| Sayfa | Jinja2 değişkenleri |
|---|---|
| `index.html` | `{{ error }}` |
| `result.html` | `{{ scan }}`, `{{ kvkk_items }}`, `{{ gdpr_items }}` |
| `history.html` | `{{ scans }}` |
| `scan_detail.html` | `{{ scan }}`, `{{ kvkk_items }}`, `{{ gdpr_items }}` |

**`scan` objesi şu alanları içerir:**
```
scan.id, scan.url, scan.kvkk_score, scan.gdpr_score,
scan.risk_level, scan.llm_suggestions, scan.created_at
```

**`kvkk_items` / `gdpr_items` her eleman şunları içerir:**
```
item.item_label, item.status  # status: 1=geçti, 0=eksik
```

**Endpoint'ler:**
- `GET /` → index.html
- `POST /scan` → form action
- `GET /history` → history.html
- `GET /scan/<id>` → scan_detail.html

**Referans dosyalar:**
- `app/routes.py` → hangi değişkenin hangi template'e gittiğini görmek için

---

## Üye 5 — Raporlama

**Dosya:** `app/services/report_service.py`

**Görev:** Tarama sonucunu JSON ve HTML formatında `reports/` klasörüne kaydet.

**Yazacağın fonksiyonlar:**

```python
def generate_json_report(scan: Scan, kvkk_items: list, gdpr_items: list) -> str:
    # reports/ klasörüne JSON dosyası kaydeder
    # Döndürür: dosya yolu (str)

def generate_html_report(scan: Scan, kvkk_items: list, gdpr_items: list) -> str:
    # reports/ klasörüne HTML dosyası kaydeder
    # Döndürür: dosya yolu (str)
```

**JSON rapor içeriği:**
```python
{
    "rapor_tarihi": "2026-04-01 14:30:00",
    "url": "https://orneksite.com",
    "kvkk_skoru": 35.0,
    "gdpr_skoru": 20.0,
    "risk_seviyesi": "Yüksek Risk",
    "kvkk_kontrolleri": [...],
    "gdpr_kontrolleri": [...],
    "ai_onerileri": "..."
}
```

**Dosya isimlendirme:**
```
reports/rapor_<scan_id>_<tarih>.json
reports/rapor_<scan_id>_<tarih>.html
```

**Referans dosyalar:**
- `app/models/scan.py` → Scan sınıfı
- `app/models/scan_item.py` → ScanItem sınıfı
- `app/routes.py` → `/report/<id>/<format>` endpoint'i

---

## Herkese Ortak Notlar

1. `scan_service.py` içindeki yorum satırlarına bak — fonksiyon isimleri ve dönüş değerleri orada tanımlı.
2. Kendi branch'inde çalış: `git checkout -b feature/senin-modülün`
3. Yeni kütüphane eklediysen `pip freeze > requirements.txt` yap ve commit et.
4. Detaylı Git kuralları için → `CONTRIBUTING.md`
