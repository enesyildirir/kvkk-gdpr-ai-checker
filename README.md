# AI Destekli KVKK/GDPR Uyumluluk Kontrol Uygulaması

Bu proje, verilen bir web sitesini KVKK ve GDPR uyumluluğu açısından otomatik olarak analiz eden, eksiklikleri tespit eden ve yapay zekâ destekli Türkçe düzeltme önerileri üreten bir web uygulamasıdır.

Uygulama; gizlilik politikası, çerez politikası, KVKK aydınlatma metni, açık rıza mekanizması, veri işleme amaçları, kullanıcı hakları ve veri saklama bilgileri gibi temel uyumluluk kriterlerini kontrol eder.

## Proje Amacı

Bu projenin amacı, web sitelerinin KVKK ve GDPR açısından temel uyumluluk durumunu ön değerlendirme seviyesinde analiz edebilen bir sistem geliştirmektir.

Uygulama hukuki danışmanlık sağlamaz. Üretilen sonuçlar yalnızca teknik ve akademik ön değerlendirme amacı taşır.

## Temel Özellikler

- Web sitesi URL’si üzerinden analiz başlatma
- HTML içeriklerini otomatik çekme
- Gizlilik politikası, çerez politikası ve KVKK metinlerini tespit etme
- KVKK/GDPR kontrol listesine göre değerlendirme yapma
- KVKK ve GDPR uyumluluk skoru üretme
- Risk seviyesini belirleme
- LLM destekli Türkçe öneriler üretme
- Yapılan taramaları SQLite veritabanına kaydetme
- Geçmiş taramaları listeleme
- Tarama detaylarını görüntüleme
- JSON veya HTML tabanlı rapor üretme

## Kullanılan Teknolojiler

- Python
- Flask
- requests
- BeautifulSoup
- SQLite
- HTML/CSS
- JavaScript
- OpenAI API veya Ollama
- python-dotenv
