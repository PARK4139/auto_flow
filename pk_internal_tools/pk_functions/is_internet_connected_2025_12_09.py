def is_internet_connected_2025_12_09():
    from pk_internal_tools.pk_functions.ensure_pinged import ensure_pinged
    import logging
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from time import time
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    # cache used
    if not hasattr(is_internet_connected_2025_12_09, "_cache_time"):
        is_internet_connected_2025_12_09._cache_time = 0
        is_internet_connected_2025_12_09._cached_result = False
    now = time()
    if now - is_internet_connected_2025_12_09._cache_time < 5:
        logging.debug(f"{func_n}() cache used")
        return is_internet_connected_2025_12_09._cached_result

    # cache updated
    result = ensure_pinged(ip="8.8.8.8")
    if QC_MODE:
        logging.debug(f"{func_n}() cache updated")
    is_internet_connected_2025_12_09._cached_result = result
    is_internet_connected_2025_12_09._cache_time = now
    return result

