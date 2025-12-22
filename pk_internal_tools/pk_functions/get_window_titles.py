def _normalize_window_title(s: str, *, collapse_inner_spaces: bool = False) -> str:
    import unicodedata

    if s is None:
        return ""

    # n. Unicode normalize
    s = unicodedata.normalize("NFKC", s)

    # 2) NBSP -> normal space
    s = s.replace("\u00A0", " ")

    # 3) remove zero-width chars
    for zw in ("\u200B", "\u200C", "\u200D", "\uFEFF"):
        s = s.replace(zw, "")

    # 5) trim edges
    return s


def _visualize_string(s: str) -> str:
    """
    Make invisible characters visible for logging.
    Example output:
      [ ABC ] raw_len=5 | repr=' ABC ' | chars= (0x20),A(0x41),B(0x42),C(0x43),(0x20)
    """
    parts = []
    for ch in s:
        parts.append(f"{ch}({hex(ord(ch))})")
    return f"[{s}] raw_len={len(s)} | repr={repr(s)} | chars={', '.join(parts)}"


# @ensure_seconds_measured
# @ensure_pk_ttl_cached(ttl_seconds=60, maxsize=64)
def get_window_titles(
        process_img_n: str | None = None,
        *,
        normalize: bool = True,
        collapse_inner_spaces: bool = False,
        unique: bool = True,
        include_invisible: bool = False,
        debug_visualize: bool = False,
):
    # Lazy import to avoid circular dependencies and improve startup time
    from pk_internal_tools.pk_objects.pk_window_monitor import get_window_monitor

    monitor = get_window_monitor()
    titles = monitor.get_titles()

    # The old implementation had a unique flag, which is now handled by the monitor's dict structure.
    # For full compatibility, we can ensure uniqueness here again, though it should be redundant.
    if unique:
        return list(dict.fromkeys(titles))
    return titles

