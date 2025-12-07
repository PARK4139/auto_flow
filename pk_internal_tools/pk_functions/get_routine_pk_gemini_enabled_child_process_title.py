from pk_internal_tools.pk_objects.pk_ttl_cache_manager import ensure_pk_ttl_cached


@ensure_pk_ttl_cached(ttl_seconds=60 * 1 * 1, maxsize=10)
def get_routine_pk_gemini_enabled_child_process_title():
    # return rf"routine_pk_gemini_enabled_child_process"
    return rf"ensure_gemini_cli_executed.py_child_process"
