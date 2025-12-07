from pk_internal_tools.pk_objects.pk_ttl_cache_manager import ensure_pk_ttl_cached
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

@ensure_seconds_measured
@ensure_pk_ttl_cached(ttl_seconds=60 * 1 * 1, maxsize=10)
def get_pk_gemini_starter_title():
    return "pk_gemini_starter"




