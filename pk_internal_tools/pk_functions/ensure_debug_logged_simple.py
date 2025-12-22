from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_debug_logged_simple(exception):
    import logging

    logging.debug(rf"exception={exception}")
