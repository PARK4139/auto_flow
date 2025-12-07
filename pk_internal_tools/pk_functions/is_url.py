

def is_url(text: str) -> bool:
    from urllib.parse import urlparse
    try:
        result = urlparse(text)
        return result.scheme in ("http", "https") and result.netloc != ""
    except Exception:
        return False
