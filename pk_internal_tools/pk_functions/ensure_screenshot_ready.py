from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_screenshot_ready():
    from pk_internal_tools.pk_functions.ensure_window_minimized import ensure_window_minimized
    import inspect
    from pk_internal_tools.pk_objects.pk_etc import pk_
    from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    ensure_window_minimized(window_title=f"{pk_}{func_n}")
    ensure_slept(milliseconds=50)
    ensure_pressed("win", "shift", "s")
