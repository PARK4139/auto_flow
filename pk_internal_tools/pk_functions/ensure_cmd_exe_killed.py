from pk_internal_tools.pk_functions.ensure_seconds_performance_benchmarked import ensure_seconds_performance_benchmarked
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_terminals_killed import ensure_processes_killed


@ensure_seconds_measured
def ensure_cmd_exe_killed():
    """
    # cmd.exe 프로세스가 없을떄
     1위: ensure_cmd_exe_killed_v2 (0.330034초)
     2위: ensure_cmd_exe_killed_v1 (0.835398초)


    # cmd.exe 프로세스가 있을때
    
    """

    ensure_cmd_exe_killed_v2()


@ensure_seconds_performance_benchmarked(metadata={"category": "kill process", "description": "ensure_cmd_exe_killed_v1()"})
def ensure_cmd_exe_killed_v1() -> None:
    ensure_processes_killed('cmd.exe')
    return ensure_processes_killed('cmd.exe')


@ensure_seconds_performance_benchmarked(metadata={"category": "kill process", "description": "ensure_cmd_exe_killed_v2()"})
def ensure_cmd_exe_killed_v2():
    from pk_internal_tools.pk_functions.ensure_process_killed_by_image_name import ensure_process_killed_by_image_name
    return ensure_process_killed_by_image_name('cmd.exe')


@ensure_seconds_performance_benchmarked(metadata={"category": "kill process", "description": "ensure_cmd_exe_killed_v3()"})
def ensure_cmd_exe_killed_v3():
    from pk_internal_tools.pk_functions.ensure_windows_killed_like_human_by_window_title import ensure_windows_killed_like_human_by_window_title
    return ensure_windows_killed_like_human_by_window_title('cmd.exe')
