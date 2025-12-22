from typing import Optional


# @ensure_seconds_measured
def ensure_sensitive_info_masked(text: str, visible_chars: int = 6) -> str:
    if not text:
        return ""
    if len(text) <= visible_chars * 2:
        return "*" * len(text)
    return (
            text[:visible_chars]
            + "*" * (len(text) - visible_chars * 2)
            + text[len(text) - visible_chars:]
    )


def ensure_sensitive_info_masked_legacy(s: Optional[str], keep: int = 4) -> str:
    if not s:
        return "<empty>"
    s = str(s)
    if len(s) <= keep * 2:
        return s[:1] + "*" * max(0, len(s) - 2) + s[-1:]
    return s[:keep] + "*" * (len(s) - keep * 2) + s[-keep:]

# def ensure_sensitive_info_masked(info: str):
#     masked_info =   info[:3] +  "*" * int(len(info)-3) + "*" * get_random_int(4)
#     return masked_info
