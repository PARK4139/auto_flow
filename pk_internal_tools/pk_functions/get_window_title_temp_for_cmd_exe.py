from pk_internal_tools.pk_objects.pk_ttl_cache_manager import ensure_pk_ttl_cached


@ensure_pk_ttl_cached(ttl_seconds=60 * 60 * 1, maxsize=11)
def get_window_title_temp_for_cmd_exe():
    return "cmd.exe controllable"
