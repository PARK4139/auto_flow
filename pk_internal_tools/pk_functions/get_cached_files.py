from functools import lru_cache

from pk_internal_tools.pk_functions.get_pnxs_from_d_working import get_pnxs_from_d_working
from pk_internal_tools.pk_objects.pk_ttl_cache_manager import ensure_pk_ttl_cached
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
# @ensure_pk_ttl_cached(ttl_seconds=10 * 1 * 1, maxsize=10)
@lru_cache(maxsize=5)
def get_cached_pk_wrappers_path(d_working):
    pnxs = get_pnxs_from_d_working(d_working)
    return pnxs
