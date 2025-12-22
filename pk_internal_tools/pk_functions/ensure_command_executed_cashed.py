from pk_internal_tools.pk_objects.pk_ttl_cache_manager import ensure_pk_ttl_cached


@ensure_pk_ttl_cached(ttl_seconds=60, maxsize=64)
def ensure_command_executed_cashed(cmd):
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    result = ensure_command_executed(cmd=cmd)
    return result
