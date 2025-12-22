from pk_internal_tools.pk_objects.pk_ttl_cache_manager import ensure_pk_ttl_cached


@ensure_pk_ttl_cached(ttl_seconds=60 * 1 * 1, maxsize=10)
def get_pk_gemini_title(local_gemini_root=None):
    return f"pk_gemini"
