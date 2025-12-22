from pk_internal_tools.pk_functions.ensure_pinged import ensure_pinged
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured

@ensure_seconds_measured
def ensure_internet_connected():
    """
        TODO: Write docstring for ensure_internet_connected.
    """
    try:
        if ensure_pinged(ip="8.8.8.8"):
            return True
    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
