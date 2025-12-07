import sys
from typing import Callable, Union

from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared
from pk_internal_tools.pk_functions.ensure_pk_terminal_output_printed import ensure_pk_terminal_output_printed
from pk_internal_tools.pk_functions.ensure_pwd_moved import ensure_pwd_moved
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_text_saved_to_clipboard import ensure_text_saved_to_clipboard
from pk_internal_tools.pk_functions.get_d_working_in_python import get_pwd_in_python
from pk_internal_tools.pk_functions.get_sanitized_file_path import get_sanitized_file_path
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
from pk_internal_tools.pk_objects.pk_directories import d_pk_root
from pk_internal_tools.pk_objects.pk_fzf_theme import PkFzfTheme


def _open_pk_log():
    """pk_system 디렉토리를 파일 탐색기로 열기 (OS별로 다른 명령어 사용)"""
    import logging
    if is_os_windows():
        ensure_command_executed(cmd=f"explorer.exe {d_pk_root}")
    else:
        # Linux: xdg-open 또는 nautilus 사용
        try:
            ensure_command_executed(cmd=f"xdg-open {d_pk_root}")
        except Exception as e:
            logging.warning(f"xdg-open 실패, nautilus 시도: {e}")
            try:
                ensure_command_executed(cmd=f"nautilus {d_pk_root}")
            except Exception as e2:
                logging.error(f"파일 탐색기 열기 실패: {e2}")


def _get_commander_commands() -> dict[str, Union[str, Callable]]:
    """
    PK Commander에서 사용할 수 있는 명령어 딕셔너리를 반환합니다.
    
    Returns:
        dict: {command_name: code_or_function} 형태의 딕셔너리
    """

    def _copy_pwd_to_clipboard():
        """현재 디렉토리를 클립보드로 복사"""
        import logging
        pwd = get_pwd_in_python()
        ensure_text_saved_to_clipboard(pwd)
        logging.info(f"현재 디렉토리가 클립보드로 복사되었습니다: {pwd}")

    def _copy_dir_list_to_clipboard():
        """현재 디렉토리의 파일 목록을 클립보드로 복사 (OS별로 다른 명령어 사용)"""
        import logging
        import subprocess

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

    def _show_pwd():
        """현재 디렉토리 출력"""
        import logging
        pwd = get_pwd_in_python()
        logging.info(f"현재 디렉토리: {pwd}")
        print(pwd)
        input("continue:enter")

    def _show_current_time():
        """현재 시간 출력"""
        import logging
        from datetime import datetime
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logging.info(f"현재 시간: {current_time}")
        print(f"현재 시간: {current_time}")
        input("continue:enter")

    def _show_python_version():
        """Python 버전 확인"""
        import logging
        import sys
        logging.info(f"Python 버전: {sys.version}")
        print(f"Python 버전: {sys.version}")
        input("continue:enter")

    # OS에 따라 다른 명령어 표시
    if is_os_windows():
        return {
            "x": sys.exit,
            "echo %cd% | clip": _copy_pwd_to_clipboard,
            "dir /b | clip": _copy_dir_list_to_clipboard,
            "cd {d_destination}": ensure_pwd_moved,
            "cd": _show_pwd,  # Windows에서도 cd만 입력하면 현재 경로 표시
            "explorer.exe .": _open_pk_log,
            "python --version": _show_python_version,
            "date /t": _show_current_time,
        }  # TODO:  fzf | clip 이거 어떻게 추가하나?   "fzf | clip" :  None 이면 되나?
    else:
        return {
            "cd {d_destination}": ensure_pwd_moved,
            "pwd": _show_pwd,
            "pwd | xclip": _copy_pwd_to_clipboard,
            "ls -1 | xclip": _copy_dir_list_to_clipboard,
            "xdg-open .": _open_pk_log,
            "python --version": _show_python_version,
            "date": _show_current_time,
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

    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
    from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done

    func_n = get_caller_name()
    logging.info(PK_UNDERLINE)
    logging.info(f"{PK_ANSI_COLOR_MAP['BRIGHT_CYAN']}PK Commander 실행 시작{PK_ANSI_COLOR_MAP['RESET']}")
    logging.info(PK_UNDERLINE)

    # 명령어와 코드 매핑 딕셔너리 가져오기
    commander_commands = _get_commander_commands()

    # fzf 옵션 목록 생성
    command_options = list(commander_commands.keys())

    if not command_options:
        logging.warning("실행할 명령어가 없습니다.")
        return

    command_failed = False  # Flag to track if the executed command failed

    # fzf로 명령어 선택
    # 경로를 안전한 파 일명으로 변환 (특수 문자 제거)
    pwd = get_pwd_in_python()
    safe_key_name = get_sanitized_file_path(pwd.replace("\\", "/").replace("_", "/").replace(":", "_"))
    if is_os_windows():
        key_name = "pk_windows_commands"
    else:
        key_name = "pk_unix_commands"
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
    if selected_command in commander_commands:
        code_to_execute = commander_commands[selected_command]
        # 코드 실행
        try:
            logging.info(PK_UNDERLINE)
            logging.info(f"{PK_ANSI_COLOR_MAP['BRIGHT_CYAN']}사전 정의된 명령어 실행 중: {selected_command}{PK_ANSI_COLOR_MAP['RESET']}")
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
            else:
                logging.error(f"지원하지 않는 코드 타입: {type(code_to_execute)}")
                command_failed = True
                return

            logging.info(PK_UNDERLINE)
            logging.info(f"{PK_ANSI_COLOR_MAP['BRIGHT_CYAN']}사전 정의된 명령어 실행 완료: {selected_command}{PK_ANSI_COLOR_MAP['RESET']}")
            logging.info(PK_UNDERLINE)
            input("continue:enter")

        except Exception as exception:
            command_failed = True  # Set flag if exception occurs
            ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
            logging.error(f"사전 정의된 명령어 실행 중 오류 발생: {selected_command}")
            raise
    else:
        # 딕셔너리에 없는 경우, 일반 쉘 명령어로 간주하고 실행
        try:
            ensure_console_cleared()
            stdout_lines, stderr_lines, returncode = ensure_command_executed(cmd=selected_command, mode_silent=True)
            if returncode != 0:
                command_failed = True  # Set flag if command returned non-zero exit code

            ensure_pk_terminal_output_printed(selected_command, stdout_lines, stderr_lines)
            input("continue:enter")
        except Exception as exception:
            command_failed = True  # Set flag if exception occurs
            ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
            logging.error(f"사용자 입력 명령어 실행 중 오류 발생: {selected_command}")
            raise
