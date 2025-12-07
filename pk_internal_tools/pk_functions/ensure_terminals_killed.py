from typing import List, Union

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_processes_killed(process_names: Union[str, List[str]], sleep_ms: int = 100) -> None:
    from pk_internal_tools.pk_functions.ensure_process_killed_by_image_name import ensure_process_killed_by_image_name
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept

    # 단일 문자열을 리스트로 변환
    if isinstance(process_names, str):
        process_names = [process_names]

    # 모든 프로세스 종료
    for process_name in process_names:
        ensure_process_killed_by_image_name(process_name)

    # 한 번만 sleep (개별 함수에서 각각 sleep하는 것보다 효율적)
    if sleep_ms > 0:
        ensure_slept(milliseconds=sleep_ms)

@ensure_seconds_measured
def ensure_terminals_killed() -> None:
    """모든 터미널 프로세스들을 종료합니다."""
    terminal_processes = ['wsl.exe', 'powershell.exe', 'cmd.exe']
    ensure_processes_killed(terminal_processes)


@ensure_seconds_measured
def ensure_wsl_exe_killed() -> None:
    """WSL.exe 프로세스를 종료합니다. (하위 호환성용)"""
    ensure_processes_killed('wsl.exe')


@ensure_seconds_measured
def ensure_powershell_exe_killed() -> None:
    """PowerShell.exe 프로세스를 종료합니다. (하위 호환성용)"""
    ensure_processes_killed('powershell.exe')


