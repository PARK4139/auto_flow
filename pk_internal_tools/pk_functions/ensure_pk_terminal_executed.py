from typing import Callable, Union

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


def _copy_pwd_to_clipboard():
    """현재 디렉토리를 클립보드로 복사"""
    import logging

    from pk_internal_tools.pk_functions.ensure_text_saved_to_clipboard import ensure_text_saved_to_clipboard
    from pk_internal_tools.pk_functions.get_d_working_in_python import get_pwd_in_python

    pwd = get_pwd_in_python()
    ensure_text_saved_to_clipboard(pwd)
    logging.info(f"현재 디렉토리가 클립보드로 복사되었습니다: {pwd}")


def _copy_dir_list_to_clipboard():
    """현재 디렉토리의 파일 목록을 클립보드로 복사 (OS별로 다른 명령어 사용)"""
    import logging
    import subprocess

    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.get_d_working_in_python import get_pwd_in_python
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows

    current_dir = get_pwd_in_python()

    if is_os_windows():
        # Windows: dir /b | clip 사용
        try:
            ensure_command_executed(cmd=f'cd /d "{current_dir}" && dir /b | clip', mode_silent=True)
            logging.info(f"Windows dir /b 명령어로 디렉토리 목록이 클립보드로 복사되었습니다")
        except Exception as e:
            logging.error(f"dir /b 명령어 실행 실패: {e}")
            # 폴백: Python으로 직접 처리
            _copy_dir_list_to_clipboard_fallback(current_dir)
    else:
        # Linux: ls -1 | xclip 또는 ls -1 | xsel 사용
        try:
            # xclip 먼저 시도
            result = subprocess.run(['which', 'xclip'], capture_output=True, text=True)
            if result.returncode == 0:
                ensure_command_executed(cmd=f'cd "{current_dir}" && ls -1 | xclip -selection clipboard', mode_silent=True)
                logging.info(f"Linux ls -1 | xclip 명령어로 디렉토리 목록이 클립보드로 복사되었습니다")
            else:
                # xsel 시도
                result = subprocess.run(['which', 'xsel'], capture_output=True, text=True)
                if result.returncode == 0:
                    ensure_command_executed(cmd=f'cd "{current_dir}" && ls -1 | xsel --clipboard --input', mode_silent=True)
                    logging.info(f"Linux ls -1 | xsel 명령어로 디렉토리 목록이 클립보드로 복사되었습니다")
                else:
                    # 폴백: Python으로 직접 처리
                    logging.warning("xclip 또는 xsel을 찾을 수 없습니다. Python으로 직접 처리합니다.")
                    _copy_dir_list_to_clipboard_fallback(current_dir)
        except Exception as e:
            logging.error(f"ls 명령어 실행 실패: {e}")
            # 폴백: Python으로 직접 처리
            _copy_dir_list_to_clipboard_fallback(current_dir)


def _copy_dir_list_to_clipboard_fallback(current_dir):
    """Python으로 직접 디렉토리 목록을 클립보드로 복사 (폴백 방법)"""
    import logging
    from pathlib import Path

    from pk_internal_tools.pk_functions.ensure_text_saved_to_clipboard import ensure_text_saved_to_clipboard

    dir_path = Path(current_dir)

    # 현재 디렉토리의 모든 항목 목록 가져오기
    items = []
    try:
        for item in dir_path.iterdir():
            items.append(item.name)
    except Exception as e:
        logging.error(f"디렉토리 목록 읽기 실패: {e}")
        return

    # 정렬
    items.sort()

    # 줄바꿈으로 연결
    dir_list = "\n".join(items)

    # 클립보드로 복사
    ensure_text_saved_to_clipboard(dir_list)
    logging.info(f"디렉토리 목록이 클립보드로 복사되었습니다 ({len(items)}개 항목)")


def _get_pk_terminal_commands() -> dict[str, Union[str, Callable]]:
    """
    PK Commander에서 사용할 수 있는 명령어 딕셔너리를 반환합니다.

    Returns:
        dict: {command_name: code_or_function} 형태의 딕셔너리
    """

    import sys

    from pk_internal_tools.pk_functions.ensure_pwd_moved import ensure_pwd_moved
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    from pk_internal_tools.pk_objects.pk_directories import D_USERPROFILE

    # OS에 따라 다른 명령어 표시
    if is_os_windows():
        return {
            rf'{D_USERPROFILE}\Downloads\fzf.exe | clip': None,
            rf'cd "{D_USERPROFILE}\Downloads\pk_memo\" && "{D_USERPROFILE}\Downloads\pk_memo\ensure_project_push_to_github_light.bat"': None,
            rf'cd "{D_USERPROFILE}\Downloads\pk_memo\" && git status': None,
            rf'cd "{D_USERPROFILE}\Downloads\pk_system\" && "{D_USERPROFILE}\Downloads\pk_system\ensure_project_push_to_github_light.bat"': None,
            rf'cd "{D_USERPROFILE}\Downloads\pk_system\" && git status': None,
            rf'echo "hello world"': None,
            rf'echo hello world': None,
            rf'explorer.exe .': None,
            rf'for /f "usebackq delims=" %f in (`dir /b /s *.mp4 *.mkv ^| {D_USERPROFILE}\Downloads\fzf.exe --query "Hitodenashi -"`) do start "" "{D_USERPROFILE}\Downloads\pk_system\pk_external_tools_lager_than_4MB\pk_windows_tools\LosslessCut-win-x64_3.64.0\LosslessCut.exe" "%f"': None,
            rf'for /f "usebackq delims=" %f in (`dir /b /s *.mp4 *.mkv ^| {D_USERPROFILE}\Downloads\fzf.exe --query "Yami"`) do start "" "{D_USERPROFILE}\Downloads\pk_system\pk_external_tools_lager_than_4MB\pk_windows_tools\LosslessCut-win-x64_3.64.0\LosslessCut.exe" "%f"': None,
            rf'for /f "usebackq delims=" %f in (`dir /b /s *.mp4 *.mkv ^| {D_USERPROFILE}\Downloads\fzf.exe`) do start "" "{D_USERPROFILE}\Downloads\pk_system\pk_external_tools_lager_than_4MB\pk_windows_tools\LosslessCut-win-x64_3.64.0\LosslessCut.exe" "%f"': None,
            r"cd {d_destination}": ensure_pwd_moved,
            rf"cd": None,
            rf"date /t": None,
            rf"dir /b | clip": None,
            rf"echo %cd% | clip": _copy_pwd_to_clipboard,
            rf"echo test": None,
            rf"python --version": None,
            rf"x": sys.exit,
        }
    else:
        return {
            "cd {d_destination}": ensure_pwd_moved,
            "pwd": None,
            "pwd | xclip": _copy_pwd_to_clipboard,
            "ls -1 | xclip": _copy_dir_list_to_clipboard,
            "python --version": None,
            "date": None,
            "x": sys.exit,
        }


@ensure_seconds_measured
def ensure_pk_terminal_executed():
    """
    fzf를 사용하여 명령어와 코드를 선택하고 실행하는 함수
    
    명령어와 코드를 딕셔너리로 관리하며, fzf로 선택한 항목을 실행합니다.
    """
    import logging
    import traceback

    from rich.progress import Progress, SpinnerColumn, TextColumn  # rich.progress 임포트

    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared
    from pk_internal_tools.pk_functions.ensure_paused import ensure_paused
    from pk_internal_tools.pk_functions.ensure_paused import ensure_paused
    from pk_internal_tools.pk_functions.ensure_pk_terminal_output_printed import ensure_pk_terminal_output_printed
    from pk_internal_tools.pk_functions.get_d_working_in_python import get_pwd_in_python
    from pk_internal_tools.pk_functions.get_sanitized_file_path import get_sanitized_file_path
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    from pk_internal_tools.pk_objects.pk_fzf_theme import PkFzfTheme

    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_objects.pk_colors import PkColors
    from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_exception_routine_done import ensure_pk_wrapper_exception_routine_done

    func_n = get_caller_name()
    logging.info(PK_UNDERLINE)
    logging.info(f"{PkColors.BRIGHT_CYAN}PK Commander 실행 시작{PkColors.RESET}")
    logging.info(PK_UNDERLINE)

    # 명령어와 코드 매핑 딕셔너리 가져오기
    commander_commands = _get_pk_terminal_commands()

    # fzf 옵션 목록 생성
    command_options = list(commander_commands.keys())

    if not command_options:
        logging.warning("실행할 명령어가 없습니다.")
        return

    command_failed = False  # Flag to track if the executed command failed

    # fzf로 명령어 선택
    # 경로를 안전한 파 일명으로 변환 (특수 문자 제거)
    pwd = get_pwd_in_python()
    # safe_key_name = get_sanitized_file_path(pwd.replace("\\", "/").replace("_", "/").replace(":", "_"))
    key_name = "TERMINAL COMMAND TO EXECUTE"
    pk_fzf_theme = PkFzfTheme(layout_reverse=True, border_style="rounded")
    selected_command = ensure_value_completed(
        key_name=key_name,
        func_n=func_n,
        options=command_options,
        guide_text="명령어 선택 또는 입력",
        history_mode=not command_failed,  # Pass based on whether the command failed
        fzf_theme=pk_fzf_theme
    )

    if not selected_command:
        logging.warning("선택된 명령어가 없어 PK Commander 실행을 종료합니다.")
        return

    logging.info(f"선택된 명령어: {selected_command}")

    # 선택된 명령어의 코드 가져오기
    code_to_execute = commander_commands.get(selected_command)  # 딕셔너리에 없으면 None 반환

    # code_to_execute가 None이 아니고, callable이거나 문자열인 경우 사전 정의된 명령어로 실행
    if code_to_execute is not None and (callable(code_to_execute) or isinstance(code_to_execute, str)):
        # 코드 실행
        try:
            logging.info(PK_UNDERLINE)
            logging.info(f"{PkColors.BRIGHT_CYAN}사전 정의된 명령어 실행 중: {selected_command}{PkColors.RESET}")
            logging.info(PK_UNDERLINE)
            ensure_console_cleared()

            # 코드가 문자열인 경우 exec()로 실행 (이 부분은 현재 사용되지 않지만, 확장성을 위해 유지)
            if isinstance(code_to_execute, str):
                # 로컬 네임스페이스 생성
                local_namespace = {
                    '__name__': '__main__',
                    '__file__': __file__,
                }
                # 필요한 모듈들을 네임스페이스에 추가
                import sys
                import os
                from pathlib import Path
                from datetime import datetime
                local_namespace.update({
                    'sys': sys,
                    'os': os,
                    'Path': Path,
                    'datetime': datetime,
                    'logging': logging,
                })
                exec(code_to_execute, local_namespace)
            # 코드가 함수인 경우 직접 호출
            elif callable(code_to_execute):
                code_to_execute()

            logging.info(PK_UNDERLINE)
            logging.info(f"{PkColors.BRIGHT_CYAN}사전 정의된 명령어 실행 완료: {selected_command}{PkColors.RESET}")
            logging.info(PK_UNDERLINE)
            ensure_paused()

        except Exception as e:
            command_failed = True  # Set flag if exception occurs
            ensure_pk_wrapper_exception_routine_done(traced_file=__file__, traceback=traceback, e=e)
            logging.error(f"사전 정의된 명령어 실행 중 오류 발생: {selected_command}")
            raise
    else:  # 딕셔너리에 없거나, code_to_execute가 None이거나 지원하지 않는 타입인 경우, 일반 쉘 명령어로 간주
        try:
            # pk_option : TODO : gemini-cli 처럼 단축키로 비우는게 좋겠는데. # pk_terminal_shortcut 구현
            ensure_console_cleared()

            # "fzf interactive mode" 와 'rich / progress' 의 충돌예방 분기처리
            if not "fzf" in selected_command:
                with Progress(
                        SpinnerColumn(style="white"),  # pk_fzf 테마컬러와 일치 (#007fff).
                        # SpinnerColumn(style="bold magenta"), # sexy color
                        # SpinnerColumn(style="bold yellow"),
                        TextColumn("[progress.description]{task.description}"),
                        transient=True,  # 작업 완료 시 자동으로 제거
                ) as live_text:
                    guide_task_working = "command is working..."
                    guide_task_done = "command is done"
                    task = live_text.add_task(f"{guide_task_working}", total=None)  # total=None으로 무한 스피너

                    stdout_lines, stderr_lines, returncode = ensure_command_executed(cmd=selected_command, mode_silent=True)

                    live_text.update(task, description=f"[green] '{guide_task_done}'")
            else:
                stdout_lines, stderr_lines, returncode = ensure_command_executed(cmd=selected_command, mode_silent=True)

            if returncode != 0:
                command_failed = True  # Set flag if command returned non-zero exit code

            ensure_pk_terminal_output_printed(selected_command, stdout_lines, stderr_lines)
            ensure_paused()
        except Exception as e:
            command_failed = True  # Set flag if exception occurs
            ensure_pk_wrapper_exception_routine_done(traced_file=__file__, traceback=traceback, e=e)
            logging.error(f"사용자 입력 명령어 실행 중 오류 발생: {selected_command}")
            raise
