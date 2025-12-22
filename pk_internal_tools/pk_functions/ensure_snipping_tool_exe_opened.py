def ensure_snipping_tool_exe_opened():
    from pk_internal_tools.pk_objects.pk_files import F_SNIPPING_TOOL_EXE
    import inspect
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.ensure_window_minimized import ensure_window_minimized
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
    from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
    from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.is_os_linux import is_os_linux
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    if is_os_windows():
        # ensure_command_executed(cmd=fr"explorer.exe {F_SNIPPING_TOOL}")
        ensure_command_executed(cmd=fr"start "" snippingtool.exe")
        # ensure_window_minimized(window_title=f"{pk_}{func_n}")
        ensure_window_minimized(window_title=get_nx(__file__))
        while True:
            ensure_window_to_front("캡처 도구")
            if is_window_title_front(window_title="캡처 도구"):
                ensure_slept(milliseconds=5)
                ensure_pressed("ctrl", "n")
                ensure_slept(milliseconds=5)
                ensure_pressed("enter")
                return
            ensure_slept(milliseconds=5)

    elif is_os_linux():
        # Linux에서는 gnome-screenshot 사용
        ensure_command_executed(cmd="gnome-screenshot --interactive")
        ensure_slept(milliseconds=5)
    else:
        # macOS나 다른 OS에서는 기본 스크린샷 도구 사용
        ensure_command_executed(cmd="screenshot")
        ensure_slept(milliseconds=5)
