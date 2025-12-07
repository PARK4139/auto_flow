from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_objects.pk_texts import PkTexts
from pk_internal_tools.pk_objects.pk_etc import


@ensure_seconds_measured
def run_pk_process_by_path(pnx, pk_arg_list=None):
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    from pk_internal_tools.pk_functions.ensure_tmux_pk_session_removed import ensure_tmux_pk_session_removed
    from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.get_cmd_to_autorun import get_cmd_to_autorun
    import logging
    import os
    import subprocess

    if pk_arg_list is None:
        pk_arg_list = []

    cmd_to_run = "python"
    # nx = get_nx(pnx) # pk_option
    # nx = rf"{pk_}{get_nx(pnx)}" # pk_option
    nx = get_nx(pnx).replace(pk_, "") # pk_option

    if is_os_windows():

        cmd_to_autorun = get_cmd_to_autorun()
        arg_cnt_allowed = 2
        while len(pk_arg_list) <= arg_cnt_allowed:
            pk_arg_list.append('')

        if pk_arg_list[2] in ['-ww', '--without window']:
            cmd = f'cmd /c "{cmd_to_autorun} && title {nx} && {cmd_to_run} {pnx}"'
            ensure_command_executed(cmd=cmd, mode='a', mode_with_window=0)
        else:
            cmd = f'start "" cmd /c "{cmd_to_autorun} && title {nx} && {cmd_to_run} {pnx}"'
            ensure_command_executed(cmd=cmd, mode='a', mode_with_window=True)

        if QC_MODE:
            logging.debug(f'{'{PkTexts.TRY_GUIDE}'} {cmd} %%%FOO%%%')

    elif is_os_wsl_linux():

        is_tmux = bool(os.environ.get("TMUX"))
        full_cmd = f"{cmd_to_run} {pnx}"
        if QC_MODE:
            full_cmd += "; sleep 99999"

        if is_tmux:
            current_pane = subprocess.check_output("tmux display -p '#{pane_id}'", shell=True).decode().strip()
            ensure_command_executed("tmux split-window -v")
            ensure_command_executed(f"tmux send-keys -t {current_pane} '{full_cmd}' C-m")
            if QC_MODE:
                logging.debug(f"{'{PkTexts.TRY_GUIDE}'} tmux split → send-keys: {full_cmd}")
        else:
            tmux_session = nx.replace(".", "_")
            ensure_tmux_pk_session_removed(tmux_session)
            ensure_command_executed(f"tmux new-session -s {tmux_session} -d '{full_cmd}'")
            ensure_command_executed(f"tmux attach-session -t {tmux_session}")
            if QC_MODE:
                logging.debug(f"{'{PkTexts.TRY_GUIDE}'} tmux new-session: {full_cmd}")
    else:
        # 기타 리눅스
        cmd = f"{cmd_to_run} {pnx}"
        ensure_command_executed(cmd=cmd)
        if QC_MODE:
            logging.debug(f"{'{PkTexts.TRY_GUIDE}'} {cmd}")
