from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_windows_deduplicated_as_loop():
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_windows_deduplicated_by_title import ensure_windows_deduplicated_by_title
    while 1:
        ensure_windows_deduplicated_by_title()
        ensure_slept(milliseconds=200)
