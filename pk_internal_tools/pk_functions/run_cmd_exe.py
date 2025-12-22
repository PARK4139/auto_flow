from enum import IntFlag, auto


class _PkModes(IntFlag):
    CUSTOM_TITLE = auto()
    WITH_TITLE = auto()
    WITHOUT_TITLE = auto()



def ensure_cmd_exe_executed(setup_op : "_PkModes", custom_title=None):
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.get_window_title_temp import get_window_title_temp
    window_title = None
    if setup_op == _PkModes.WITH_TITLE:
        window_title = get_window_title_temp()
    elif setup_op == _PkModes.WITHOUT_TITLE:
        window_title = ""
    elif setup_op == _PkModes.CUSTOM_TITLE:
        window_title = custom_title
    # ensure_command_executed(cmd=rf'start /MAX "{window_title}" cmd.exe /k', mode="a")
    ensure_command_executed(cmd=rf'start "{window_title}" cmd.exe /k', mode="a")
