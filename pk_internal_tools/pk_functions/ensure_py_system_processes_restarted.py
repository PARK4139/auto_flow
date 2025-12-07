

def ensure_py_system_processes_restarted(pk_python_files):
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_process_killed import ensure_process_killed
    from pk_internal_tools.pk_functions.ensure_py_system_process_ran_by_pnx import ensure_py_system_process_ran_by_pnx
    from pk_internal_tools.pk_functions.get_nx import get_nx
    for file_to_execute in pk_python_files:
        ensure_process_killed(window_title_seg=get_nx(file_to_execute))
    ensure_slept(milliseconds=77)
    for file_to_execute in pk_python_files:
        ensure_py_system_process_ran_by_pnx(file_to_execute=file_to_execute)
