from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_windows_minimized():
    ensure_windows_minimized_v3()


def ensure_windows_minimized_v1():
    from pk_internal_tools.pk_functions.ensure_window_minimized import ensure_window_minimized
    from pk_internal_tools.pk_functions.get_windows_opened_with_hwnd import get_windows_opened_with_hwnd

    for window_title in get_windows_opened_with_hwnd():
        ensure_window_minimized(window_title=window_title)


def ensure_windows_minimized_v2():
    from pk_internal_tools.pk_functions.ensure_windows_minimized_callback import ensure_windows_minimized_callback

    import win32gui
    win32gui.EnumWindows(ensure_windows_minimized_callback, None)


def ensure_windows_minimized_v3():
    from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
    ensure_pressed("win", "m")
