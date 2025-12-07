from functools import lru_cache

from pk_internal_tools.pk_objects.pk_ttl_cache_manager import ensure_pk_ttl_cached
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
@lru_cache(maxsize=1)
def ensure_pk_colorama_initialized_once():
    from colorama import init as pk_colorama_init
    # pk_colorama_init(autoreset=True)
    pk_colorama_init(autoreset=True, strip=False, convert=False)
