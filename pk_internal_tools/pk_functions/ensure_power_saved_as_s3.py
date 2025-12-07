
from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.get_pnx_wsl_unix_style import get_pnx_wsl_unix_style
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows


def ensure_power_saved_as_s3():
    # 절전모드
    # ensure_command_executed(cmd=rf"powercfg /setacvalueindex scheme_current sub_buttons button=1-3 action=0")
    cmd = rf"rundll32.exe powrprof.dll,SetSuspendState 0,1,0"
    if is_os_windows():
        ensure_command_executed(cmd=cmd)
    else:
        cmd = get_pnx_wsl_unix_style(pnx=cmd)
        ensure_command_executed(cmd=cmd)
