from pk_internal_tools.pk_functions.ensure_gemini_cli_update_wait_completed import ensure_gemini_cli_update_wait_completed
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.get_window_titles import get_window_titles




@ensure_seconds_measured
def get_gemini_cli_expected_titles(local_gemini_root=None):
    """
        TODO :
        issue discovered :
        title 변경로직이 있는 경우, gemini 업데이트의 경우,
        초기 detected title 과 다르게 변화됨.
        이로인해, 오동작이 유도된다. 예외처리필요.
    """
    from pathlib import Path

    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.get_os_sys_environment_variable import get_os_sys_environment_variable
    from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT

    if local_gemini_root is None:
        local_gemini_root = D_PK_ROOT

    # window gemini cli updating
    ensure_gemini_cli_update_wait_completed()

    options = [
        f"Gemini - {get_os_sys_environment_variable('USERNAME')}",
        f"Gemini - {str(get_nx(Path(local_gemini_root)))}",
        "Windows PowerShell",  # pk_ensure_gemini_cli_worked_done 에서 ctrl + c 를 누른 경우
        "pk_ensure_gemini_cli_worked_done.py",  # gemini 실행 시
    ]
    return options
