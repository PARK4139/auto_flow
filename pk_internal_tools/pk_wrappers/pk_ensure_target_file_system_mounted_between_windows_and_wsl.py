

import traceback

from colorama import init as pk_colorama_init

# from pk_internal_tools.pk_objects.500_live_logic import ensure_tmux_pk_session_removed, get_nx, ensure_value_completed_2025_10_12_0000, get_pk_wsl_mount_d, get_pnxs, is_os_linux, ensure_slept, ensure_spoken
# from pk_internal_tools.pk_objects.static_logic import d_pk_external_tools, UNDERLINE, '{PkTexts.TRY_GUIDE}', d_pk_system, '[ UNIT TEST EXCEPTION DISCOVERED ]'
#, print_red

ensure_pk_colorama_initialized_once()

if __name__ == "__main__":
    try:

        # d_working = get_pnx_from_fzf()
        windows_path = ensure_value_completed_2025_10_12_0000(key_hint="windows_path=", values=[])
        # path_to_mount = ensure_value_completed_2025_10_12_0000(key_name="path_to_mount=", options=available_ip_without_localhost_list)
        d_pk_wsl_mount = get_pk_wsl_mount_d(windows_path=windows_path, path_to_mount='Downloads/pk_working')
        # d_pk_wsl_mount = get_pk_wsl_mount_d(windows_path=d_working, path_to_mount=path_to_mount)
        
        ensure_slept(100000)
        if is_os_linux():
            # ensure_command_executed('exit')
            # available_pk_process_pnx = get_pnx_from_fzf(d_pk_external_tools)
            available_pk_process_pnx = None
            pnx_list = get_pnxs(d_working=d_pk_external_tools, mode="f", with_walking=False)
            for pnx in pnx_list:
                if __file__ not in pnx:
                    continue
                available_pk_process_pnx = pnx
            tmux_session = get_nx(available_pk_process_pnx).replace(".", "_")
            ensure_tmux_pk_session_removed(tmux_session)

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__,traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_system=d_pk_system)
