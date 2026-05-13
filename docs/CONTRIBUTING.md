# Katkı Rehberi — AI Destekli KVKK/GDPR Uyumluluk Kontrol Uygulaması

> Ekip üyelerine not: Bu dokümanı okumadan kod yazmaya başlamayın. Hep birlikte aynı kurallara uyarsak çakışma ve karışıklık yaşamayız.

---

## 1. Genel Kurallar

- Kod her zaman Türkçe yorum satırlarıyla yazılır
- Değişken ve fonksiyon isimleri İngilizce olur (`get_scan`, `parse_html` gibi)
- Bir şeyden emin değilsen **direkt `main` branch'e commit atma**, branch aç (aşağıda anlatıldı)
- Hata alırsan önce kendin çözmeye çalış, çözemezsen ekibe sor

---

## 2. Başlangıç

Projeyi ilk kez kuracaksan şu adımları takip et:

```bash
# 1. Repoyu klonla
git clone https://github.com/kullanici-adi/ai-kvkk-gdpr-checker.git
cd ai-kvkk-gdpr-checker

# 2. Sanal ortamı oluştur
python -m venv .venv --without-pip
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux

# 3. pip ve bağımlılıkları yükle
python -m ensurepip --upgrade
pip install -r requirements.txt

# 4. .env dosyasını oluştur
# .env.example dosyasını kopyala, adını .env yap, içini doldur

# 5. Ollama modelini indir
ollama pull llama3.2:3b
```

---

## 3. Branch (Dal) Kullanımı

**Altın kural: `main` branch'e direkt kod gönderme.**

Her görev için yeni bir branch aç:

```bash
# Branch açma
git checkout -b feature/crawler

# Bitince main'e geri dön
git checkout main
```

### Branch İsimlendirme

| Durum | Format | Örnek |
|---|---|---|
| Yeni özellik | `feature/açıklama` | `feature/crawler` |
| Hata düzeltme | `fix/açıklama` | `fix/parser-encoding` |
| Doküman | `docs/açıklama` | `docs/database-md` |

---

## 4. Commit Mesajı Nasıl Yazılır?

Commit mesajı ne yaptığını **kısaca ve net** anlatmalı.

```bash
# İyi örnekler
git commit -m "crawler.py: URL'den HTML çekme fonksiyonu eklendi"
git commit -m "parser.py: gizlilik politikası tespiti düzeltildi"
git commit -m "compliance_checker.py: GDPR maddeleri eklendi"

# Kötü örnekler
git commit -m "düzeltme"
git commit -m "asdfgh"
git commit -m "bitti"
```

---

## 5. Ekip İş Bölümü

| Üye | Sorumluluk | Dosyalar |
|---|---|---|
| Üye 1 | Veri Toplama | `crawler.py`, `parser.py`, `scan_service.py` |
| Üye 2 | Uyumluluk Analizi | `compliance_checker.py`, `kvkk_gdpr_checklist.json` |
| Üye 3 | AI Entegrasyonu | `llm_service.py` |
| Üye 4 | Arayüz | `routes.py`, `templates/`, `static/` |
| Üye 5 | Veritabanı & Raporlama | `database.py`, `models/`, `repositories/`, `report_service.py` |

> Başkasının sorumluluğundaki dosyayı değiştirmen gerekiyorsa önce o kişiye haber ver.

---

## 6. Genel Git Akışı

Her gün çalışmaya başlamadan önce şunu yap:

```bash
# Ana branch'i güncelle
git checkout main
git pull origin main

# Kendi branch'ine geç
git checkout feature/senin-branch-adin

# Ana branch'teki yenilikleri al
git merge main
```

Günün sonunda:

```bash
git add .
git commit -m "ne yaptığını açıkla"
git push origin feature/senin-branch-adin
```

---

## 7. Sık Yapılan Hatalar

**`.env` dosyasını repoya gönderme!**
```bash
# Bunu yaptıysan hemen geri al
git rm --cached .env
```

**`main` branch'e direkt commit atma.**
Her zaman branch aç, işini yap, sonra birleştir.

**`requirements.txt` dosyasını güncellemeyi unutma.**
Yeni bir kütüphane yüklediysen:
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "requirements.txt güncellendi"
```

---

## 8. Yardım Kaynakları

- Proje mimarisi → `docs/architecture.md`
- Veritabanı şeması → `docs/database.md`
- Kullanım kılavuzu → `docs/usage.md`
- Git'e yeni başlayanlar → [git-scm.com/book/tr](https://git-scm.com/book/tr/v2)

---

*Son güncelleme: Nisan 2026*
