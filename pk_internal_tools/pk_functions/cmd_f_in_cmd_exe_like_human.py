from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style
from pk_internal_tools.pk_functions.get_pnx_windows_style import get_pnx_windows_style


def cmd_f_in_cmd_exe_like_human(cmd_prefix, f):
    # make
    # make_version_new(via_f_txt=True, debug_mode=True)

    # src
    f = get_pnx_unix_style(pnx=f)

    dst = get_p(f)
    dst = get_pnx_unix_style(pnx=dst)

    # pnx_new
    pnx_new = get_pnx_new(d_working=dst, pnx=f)
    pnx_new = get_pnx_windows_style(pnx=pnx_new)

    # kill
    # ensure_process_killed_via_taskkill(process_name='cmd.exe')
    # ensure_process_killed_via_wmic(process_img_n='cmd.exe')
    window_title_seg = f
    window_title_seg = get_pnx_windows_style(window_title_seg)
    kill_window_like_human(window_title_seg=window_title_seg)

    # run
    try:
        ensure_command_executed_like_human(cmd=rf'"{D_PK_ROOT}\.venv\Scripts\activate.cmd"')
        ensure_command_executed_like_human(cmd=rf'{cmd_prefix} "{pnx_new}"')
    except Exception as e:
        pass

    # move (to pycharm64.exe)
    ensure_window_to_front_of_pycharm()