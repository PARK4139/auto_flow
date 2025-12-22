from pk_internal_tools.pk_objects.pk_ttl_cache_manager import ensure_pk_ttl_cached
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
@ensure_pk_ttl_cached(ttl_seconds=60, maxsize=64)
def get_idle_title_of_losslesscut():
    try:
        return "LosslessCut"
    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
