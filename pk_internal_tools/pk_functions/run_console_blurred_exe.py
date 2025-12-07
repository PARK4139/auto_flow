from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed


def run_console_blurred_exe():
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    # console_blurred.exe exec
    cmd_str = rf".\dist\console_blurred\console_blurred.exe"
    ensure_command_executed(cmd_str)
