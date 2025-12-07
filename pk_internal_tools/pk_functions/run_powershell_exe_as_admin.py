def run_powershell_exe_as_admin():
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    # ensure_command_executed('PowerShell -cmd "Start-Process powershell"')
    ensure_command_executed('powershell -cmd "Start-Process powershell -Verb RunAs"')
    ensure_window_to_front("관리자: Windows PowerShell")
