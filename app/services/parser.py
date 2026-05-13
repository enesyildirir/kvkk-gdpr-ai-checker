from bs4 import BeautifulSoup


# Tespit için anahtar kelimeler
PRIVACY_KEYWORDS  = ["gizlilik politikası", "gizlilik bildirimi", "privacy policy"]
COOKIE_KEYWORDS   = ["çerez politikası", "çerez bildirimi", "cookie policy", "çerez"]
KVKK_KEYWORDS     = ["kvkk", "kişisel verilerin korunması", "aydınlatma metni", "6698"]
CONSENT_KEYWORDS  = ["açık rıza", "onaylıyorum", "kabul ediyorum", "rızam"]
RETENTION_KEYWORDS= ["saklama süresi", "veri saklama", "muhafaza süresi"]
RIGHTS_KEYWORDS   = ["veri sahibi hakları", "haklarınız", "başvuru hakkı", "ilgili kişi hakları"]
DATA_KEYWORDS     = ["veri sorumlusu", "veri işleme", "işlenen veriler", "veri kategorileri"]


def extract_text(html: str) -> str:
    """HTML'den script/style temizlenmiş düz metin çıkarır."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return soup.get_text(separator=" ", strip=True).lower()


def detect_sections(html: str) -> dict:
    """
    HTML içinde KVKK/GDPR ile ilgili bölümlerin varlığını tespit eder.

    Döndürür:
    {
        "has_privacy_policy":       bool,
        "has_cookie_policy":        bool,
        "has_kvkk_text":            bool,
        "has_consent_mechanism":    bool,
        "has_retention_info":       bool,
        "has_user_rights":          bool,
        "has_data_processing_info": bool
    }
    """
    text = extract_text(html)

    return {
        "has_privacy_policy":       any(k in text for k in PRIVACY_KEYWORDS),
        "has_cookie_policy":        any(k in text for k in COOKIE_KEYWORDS),
        "has_kvkk_text":            any(k in text for k in KVKK_KEYWORDS),
        "has_consent_mechanism":    any(k in text for k in CONSENT_KEYWORDS),
        "has_retention_info":       any(k in text for k in RETENTION_KEYWORDS),
        "has_user_rights":          any(k in text for k in RIGHTS_KEYWORDS),
        "has_data_processing_info": any(k in text for k in DATA_KEYWORDS),
    }


def extract_relevant_text(html: str, max_chars: int = 3000) -> str:
    """
    LLM'e gönderilecek özet metni çıkarır.
    Tüm sayfa yerine yalnızca ilgili kısımları alır.
    """
    text = extract_text(html)

    all_keywords = (
        PRIVACY_KEYWORDS + COOKIE_KEYWORDS + KVKK_KEYWORDS +
        CONSENT_KEYWORDS + RETENTION_KEYWORDS + RIGHTS_KEYWORDS + DATA_KEYWORDS
    )

    relevant_parts = []
    for keyword in all_keywords:
        idx = text.find(keyword)
        if idx != -1:
            start = max(0, idx - 100)
            end = min(len(text), idx + 300)
            relevant_parts.append(text[start:end])

    if relevant_parts:
        return " ... ".join(relevant_parts)[:max_chars]

    # İlgili kısım bulunamazsa metnin başını döndür
    return text[:max_chars]
