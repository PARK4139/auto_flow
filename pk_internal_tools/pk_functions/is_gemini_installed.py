from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


# @ensure_pk_ttl_cached(ttl_seconds=5, maxsize=64)
@ensure_seconds_measured
def is_gemini_installed():
    from pk_internal_tools.pk_functions.get_gemini_version_installed import get_gemini_version_installed
    gemini_version = get_gemini_version_installed()
    if gemini_version is None:
        return False
    return True
