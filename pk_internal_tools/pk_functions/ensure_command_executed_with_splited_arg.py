from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed


def ensure_command_executed_with_splited_arg(cmd, capture_output=False, **kwargs):
    """ensure_command_executed로 OS 명령 실행"""
    cmd_str = ' '.join(cmd) if isinstance(cmd, (list, tuple)) else str(cmd)
    print(f"> {cmd_str}")
    return ensure_command_executed(cmd=cmd_str)
