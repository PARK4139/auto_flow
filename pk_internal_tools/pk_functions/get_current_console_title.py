import logging

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_current_console_title() -> str:
    import ctypes

    from pk_internal_tools.pk_functions.ensure_guided_not_prepared_yet import ensure_not_prepared_yet_guided
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    if is_os_windows():
        buffer = ctypes.create_unicode_buffer(1024)
        ctypes.windll.kernel32.GetConsoleTitleW(buffer, len(buffer))
        current_terminal_console_title = buffer.value
        logging.debug(rf'current_terminal_console_title={current_terminal_console_title}')
        return current_terminal_console_title
    else:
        ensure_not_prepared_yet_guided()
