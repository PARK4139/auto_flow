import traceback
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose

@ensure_seconds_measured
def get_text_from_clipboard_legacy():
    import logging

    from pk_internal_tools.pk_functions.get_str_from_tuple import get_str_from_tuple
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows

    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

    if is_os_windows():
        results = ensure_command_executed('powershell.exe Get-Clipboard')
        logging.debug(f'type(results)={type(results)}')
        if isinstance(results, str):
            return results
        elif isinstance(results, list):
            for result in results:
                logging.debug("way1: powershell.exe Get-Clipboard list")
                logging.debug(rf"result={result}")
            return results.__str__()
        elif isinstance(results, tuple):
            for result in results:
                logging.debug("way1: powershell.exe Get-Clipboard list")
                logging.debug(rf"result={result}")
            return get_str_from_tuple(results, separator='\n')
        else:
            return ""
    else:
        try:
            import clipboard
            logging.debug("way3 : clipboard.paste()")
            return clipboard.paste()
        except ImportError:
            # clipboard 모듈이 없는 경우 빈 문자열 반환
            return ""
