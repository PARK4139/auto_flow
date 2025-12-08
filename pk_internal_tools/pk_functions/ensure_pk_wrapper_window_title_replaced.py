from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pk_wrapper_window_title_replaced(window_title):
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced


    ensure_window_title_replaced(get_nx(window_title))
