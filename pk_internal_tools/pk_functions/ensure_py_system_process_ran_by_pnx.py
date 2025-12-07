from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_py_system_process_ran_by_pnx(file_to_execute, mode=''):
    import logging

    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_objects.pk_files import F_UV_PYTHON_EXE, F_UV_ACTIVATE_BAT
    import subprocess
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux

    if is_os_windows():
        cmd = rf'start "" cmd /c "cd /d "{d_pk_root}" && {F_UV_ACTIVATE_BAT} && {F_UV_PYTHON_EXE} "{file_to_execute}"'
        logging.debug(f"[실행 중 - Windows] {cmd}")
        if mode == 'a':
            # 비동기 동작검증 완료
            ensure_command_executed(cmd, mode='a')
        else:
            # 동기 동작검증 완료
            ensure_command_executed(cmd)
    elif is_os_wsl_linux():
        # WSL 환경
        cmd = f'{F_UV_PYTHON_EXE} {file_to_execute}'
        logging.debug(f"[실행 중 - WSL] {cmd}")
        ensure_command_executed(cmd=cmd)
    else:
        # 기타 리눅스/유닉스
        cmd = f'{F_UV_PYTHON_EXE} {file_to_execute}'
        logging.debug(f"[실행 중 - Linux/Unix] {cmd}")
        subprocess.run(cmd, shell=True)
