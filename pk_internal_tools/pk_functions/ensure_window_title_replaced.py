from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured




@ensure_seconds_measured
def ensure_window_title_replaced(window_title):
    import ctypes
    # return ensure_command_executed(f"title {window_title}") # slow
    # return os.system(f"title {window_title}") # slow
    return ctypes.windll.kernel32.SetConsoleTitleW(str(window_title)) # time performance improved from
