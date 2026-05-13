import requests
from bs4 import BeautifulSoup


def fetch_html(url: str) -> dict:
    """
    Verilen URL'nin HTML içeriğini çeker.

    Döndürür:
    {
        "url": str,
        "html": str | None,
        "status_code": int | None,
        "error": str | None
    }
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return {
            "url": url,
            "html": response.text,
            "status_code": response.status_code,
            "error": None
        }
    except requests.exceptions.Timeout:
        return {"url": url, "html": None, "status_code": None,
                "error": "Bağlantı zaman aşımına uğradı."}
    except requests.exceptions.ConnectionError:
        return {"url": url, "html": None, "status_code": None,
                "error": "Siteye bağlanılamadı."}
    except requests.exceptions.HTTPError as e:
        return {"url": url, "html": None, "status_code": response.status_code,
                "error": f"HTTP hatası: {e}"}
    except Exception as e:
        return {"url": url, "html": None, "status_code": None,
                "error": f"Beklenmeyen hata: {e}"}


def find_policy_links(html: str, base_url: str) -> dict:
    """
    Ana sayfadaki linkleri tarayarak gizlilik, çerez ve KVKK
    sayfalarına ait URL'leri bulur.

    Döndürür:
    {
        "privacy": str | None,
        "cookie":  str | None,
        "kvkk":    str | None
    }
    """
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", href=True)

    privacy_keywords = ["privacy", "gizlilik", "privacy-policy", "gizlilik-politikasi"]
    cookie_keywords  = ["cookie", "çerez", "cerez", "cookie-policy", "cerez-politikasi"]
    kvkk_keywords    = ["kvkk", "aydinlatma", "aydınlatma", "kisisel-veri", "kişisel-veri"]

    result = {"privacy": None, "cookie": None, "kvkk": None}

    for link in links:
        href = link["href"].lower()
        text = link.get_text().lower()

        # Tam URL oluştur
        if href.startswith("/"):
            full_url = base_url.rstrip("/") + href
        elif href.startswith("http"):
            full_url = href
        else:
            continue

        if not result["privacy"] and any(k in href or k in text for k in privacy_keywords):
            result["privacy"] = full_url

        if not result["cookie"] and any(k in href or k in text for k in cookie_keywords):
            result["cookie"] = full_url

        if not result["kvkk"] and any(k in href or k in text for k in kvkk_keywords):
            result["kvkk"] = full_url

    return result
