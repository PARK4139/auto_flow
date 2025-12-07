import logging
import traceback

from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
from pk_internal_tools.pk_functions.ensure_env_var_completed_2025_11_24 import ensure_env_var_completed_2025_11_24
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.ensure_windows_killed_like_human_by_window_title import ensure_windows_killed_like_human_by_window_title
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_commit_message import get_commit_message
from pk_internal_tools.pk_functions.get_current_console_title import get_current_console_title
from pk_internal_tools.pk_functions.get_text_cyan import get_text_cyan

step_counter = 1


def _ensure_git_add(start_time):
    import logging
    from pk_internal_tools.pk_functions.ensure_status_printed_step import ensure_status_printed_step
    from pk_internal_tools.pk_functions.run_command import run_command
    cmd = "git add ."
    code, output = run_command(cmd, capture_output=True)
    outputs = output.split('\n')
    for _ in outputs:
        logging.debug(f"{_}")
    label = ensure_status_printed_step(step_counter + 1, cmd, code, output)
    if not ensure_label_process_done(label, start_time):
        return


def _get_save_point_commit_message_with_timestamp(__file__):
    from pk_internal_tools.pk_functions.get_pk_time_2025_10_20_1159 import get_pk_time_2025_10_20_1159
    from pk_internal_tools.pk_functions.get_nx import get_nx
    auto_commit_message = f"feat: make savepoint, automatically by {get_nx(__file__)} at {get_pk_time_2025_10_20_1159("%Y-%m-%d %H:%M")}"
    return auto_commit_message


def _get_ai_commit_massage(__file__):
    gemini_cli_headless_mode_data = get_commit_message()

    # Check if the call to get_commit_message was successful and returned a response
    if gemini_cli_headless_mode_data and gemini_cli_headless_mode_data.status == "success" and gemini_cli_headless_mode_data.response:
        commit_message = gemini_cli_headless_mode_data.response
        logging.debug(f'AI에 의해서 commit_message가 생성되었습니다.')
    else:
        logging.warning("AI commit message 생성을 실패하여, save point commit message를 사용합니다.")
        commit_message = _get_save_point_commit_message_with_timestamp(__file__)

    return commit_message


def _ensure_git_commit(start_time, ai_commit_massage_mode, __file__, editable):
    import logging
    from pk_internal_tools.pk_functions.ensure_status_printed_step import ensure_status_printed_step
    from pk_internal_tools.pk_functions.run_command import run_command
    from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
    from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    logging.debug(f'''ai_commit_massage_mode={ai_commit_massage_mode} ''')
    func_n = get_caller_name()
    if ai_commit_massage_mode:
        commit_message = _get_ai_commit_massage(__file__)
    else:
        ensure_window_to_front(window_title_seg=get_current_console_title())
        timestamp_commit_option = f"< {_get_save_point_commit_message_with_timestamp(__file__)} style option >"
        try:
            commit_message = ensure_value_completed(
                key_name='commit_message',
                func_n=func_n,
                options=[timestamp_commit_option],
            )
            commit_message = commit_message.strip() or ""
            if commit_message == timestamp_commit_option:
                logging.debug(f'''commit_message is empty''')
                commit_message = _get_ai_commit_massage(__file__)
            else:
                commit_message = commit_message
            logging.debug(f'''finally checked commit_message: {get_text_cyan(commit_message)} ''')
        except Exception as e:
            # fzf 실행 실패 시 자동으로 기본 메시지 사용 (중복 입력 방지)
            import traceback
            logging.debug(f"{PK_ANSI_COLOR_MAP['RED']}{PK_UNDERLINE}")
            logging.debug(f"FZF 실행 실패 - 상세 오류 정보{PK_ANSI_COLOR_MAP['RESET']}")
            logging.debug(f'''예외 타입: {type(e).__name__} ''')
            logging.debug(f'''예외 메시지: {str(e)} ''')
            logging.debug(f'''상세 스택 트레이스: ''')
            logging.debug(f"{PK_ANSI_COLOR_MAP['RED']}{PK_UNDERLINE}")
            logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")
            logging.debug(f"{PK_ANSI_COLOR_MAP['YELLOW']}{PK_UNDERLINE}")
            logging.debug(f"[SOLUTION] 해결 방법:{PK_ANSI_COLOR_MAP['RESET']}")
            logging.debug(f"1. Windows: choco install fzf 또는 scoop install fzf")
            logging.debug(f"2. Linux: sudo apt install fzf 또는 sudo yum install fzf")
            logging.debug(f"3. fzf가 PATH에 있는지 확인: which fzf 또는 where fzf")
            logging.debug(f"{PK_ANSI_COLOR_MAP['YELLOW']}{PK_UNDERLINE}" + PK_ANSI_COLOR_MAP['RESET'])
            logging.debug(f'''[FALLBACK] 기본 커밋 메시지를 사용합니다 ''')

            commit_message_fallback = ensure_value_completed(
                key_name='commit_message_fallback',
                func_n=func_n,
                options=[timestamp_commit_option],
            )
            commit_message = commit_message_fallback

    cmd = f'git commit -m "{commit_message}"'
    code, output = run_command(cmd, capture_output=True)
    outputs = output.strip().split('\n')
    for _ in outputs:
        logging.debug(f"{_}")
    label = ensure_status_printed_step(step_counter + 1, cmd, code, output)
    if not ensure_label_process_done(label, start_time):
        return


def _ensure_upstream_branch_checked(current_branch):
    import logging
    from pk_internal_tools.pk_functions.run_command import run_command
    cmd_upstream = f"git rev-parse --abbrev-ref {current_branch}@{{upstream}}"
    code_upstream, output_upstream = run_command(cmd_upstream, capture_output=True)
    cmd = None
    if code_upstream != 0:
        logging.debug(f"업스트림 브랜치가 설정되지 않음. 설정 중...")
        # 업스트림 설정과 함께 푸시
        cmd = f"git push --set-upstream origin {current_branch}"
        # 업스트림이 없을 때는 ahead/behind 정보를 가져올 수 없으므로 기본값 반환
        return cmd, 1, ""  # code_ahead_behind=1 (에러), output_ahead_behind="" (빈 문자열)
    else:
        upstream_branch = output_upstream.strip()
        logging.debug(f"업스트림 브랜치: {upstream_branch}")

        # 3-4. 로컬과 원격 브랜치 비교
        cmd_ahead_behind = f"git rev-list --left-right --count origin/{current_branch}...{current_branch}"
        code_ahead_behind, output_ahead_behind = run_command(cmd_ahead_behind, capture_output=True)

        return cmd, code_ahead_behind, output_ahead_behind


def _ensure_git_pushed(cmd, code_ahead_behind, output_ahead_behind, current_branch, start_time):
    from pk_internal_tools.pk_functions.ensure_git_state_checked import ensure_git_state_checked
    from pk_internal_tools.pk_functions.ensure_status_printed_step import ensure_status_printed_step

    import logging
    from pk_internal_tools.pk_functions.run_command import run_command
    if code_ahead_behind == 0:
        behind, ahead = output_ahead_behind.strip().split('\t')
        logging.debug(f"브랜치 상태 - 뒤처진 커밋: {behind}개, 앞선 커밋: {ahead}개")
        if int(behind) > 0:
            logging.debug(f"로컬 브랜치가 {behind}개 커밋만큼 뒤처져 있습니다.")
            logging.debug("강제 푸시를 시도합니다...")
            cmd = f"git push origin {current_branch} --force-with-lease"
        else:
            cmd = "git push"
    else:
        # 원격 브랜치 정보를 가져올 수 없는 경우
        logging.debug("원격 브랜치 정보를 확인할 수 없습니다. 일반 푸시를 시도합니다.")
        cmd = "git push"
    logging.debug(f"cmd={cmd}")
    state_code, output = run_command(cmd, capture_output=True)
    outputs = output.strip().split('\n')
    for _ in outputs:
        logging.debug(f"{_}")

    # 푸시 실패 시 추가 시도
    if state_code != 0:
        if "no upstream branch" in output.lower():
            logging.debug("업스트림 브랜치 미설정으로 인한 실패. 재시도...")
            cmd_retry = f"git push --set-upstream origin {current_branch}"
            logging.debug(f"cmd_retry={cmd_retry}")
            state_code, output = run_command(cmd_retry, capture_output=True)
            outputs = output.strip().split('\n')
            for _ in outputs:
                logging.debug(f"{_}")

        elif "non-fast-forward" in output.lower() or "rejected" in output.lower():
            logging.debug("Fast-forward 불가로 인한 실패. 강제 푸시 시도...")
            cmd_force = f"git push origin {current_branch} --force-with-lease"
            logging.debug(f"cmd_force={cmd_force}")
            state_code, output = run_command(cmd_force, capture_output=True)
            outputs = output.strip().split('\n')
            for _ in outputs:
                logging.debug(f"{_}")

            if state_code != 0:
                logging.debug("--force-with-lease 실패. 완전 강제 푸시 시도...")
                cmd_force_hard = f"git push origin {current_branch} --force"
                logging.debug(f"cmd_force_hard={cmd_force_hard}")
                state_code, output = run_command(cmd_force_hard, capture_output=True)
                outputs = output.strip().split('\n')
                for _ in outputs:
                    logging.debug(f"{_}")

    label = ensure_status_printed_step(step_counter + 1, cmd, state_code, output)
    if label == "FAILED":
        logging.debug("푸시 실패 상세 분석")
        logging.debug(f"최종 명령어: {cmd}")
        logging.debug(f"반환 코드: {state_code}")
        logging.debug(f"출력 메시지: {output}")
        logging.debug("가능한 해결 방법")
        logging.debug("1. git pull origin main (원격 변경사항 병합)")
        logging.debug("2. git push --force (강제 푸시)")
        logging.debug("3. GitHub 인증 토큰 확인")
        logging.debug("4. 네트워크 연결 상태 확인")
        state = ensure_git_state_checked(start_time, label)
        if state == False:
            return
    return state_code, output


def ensure_label_process_done(label, start_time):
    from pk_internal_tools.pk_functions.ensure_git_state_checked import ensure_git_state_checked
    if label == "FAILED":
        state = ensure_git_state_checked(start_time, label)
        if state == False:
            return False

    if label == "SKIPPED":
        state = ensure_git_state_checked(start_time, label)
        if state == False:
            return False
    return True


def ensure_git_repo_pushed(d_local_repo, ai_commit_massage_mode=None):
    from pk_internal_tools.pk_functions.get_nx import get_nx

    import os
    import time

    import logging
    from pk_internal_tools.pk_functions.ensure_git_state_checked import ensure_git_state_checked
    from pk_internal_tools.pk_functions.ensure_status_printed_step import ensure_status_printed_step
    from pk_internal_tools.pk_functions.run_command import run_command
    from pk_internal_tools.pk_functions.set_text_from_history_file import set_text_from_history_file
    from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
    from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE

    # pk_option
    # ensure_window_minimized(window_title=get_current_console_title())

    pwd = os.getcwd()

    try:

        ensure_windows_killed_like_human_by_window_title(window_title=rf"pk_ensure_routine_file_executed_as_hot_reloader.py")

        os.chdir(d_local_repo)

        global step_counter

        if ai_commit_massage_mode is None:
            ai_commit_massage_mode = False
        editable = False

        start_time = time.time()
        logging.debug(PK_UNDERLINE)
        d_project_to_push = get_nx(os.getcwd())
        # easy_speakable_text = get_easy_speakable_text(d_project_to_push)
        # ensure_spoken(rf"{easy_speakable_text} 푸쉬 시도")
        logging.debug(f"LOCAL LEPO : {PK_ANSI_COLOR_MAP['CYAN']}{d_project_to_push}{PK_ANSI_COLOR_MAP['RESET']}")
        logging.debug(f"STARTED AT : {PK_ANSI_COLOR_MAP['CYAN']}{time.strftime('%Y-%m-%d %H:%M:%S')}{PK_ANSI_COLOR_MAP['RESET']}")

        # git config set
        func_n = get_caller_name()
        user_email = ensure_env_var_completed_2025_11_24(key_name="user_email", func_n=func_n)
        user_name = ensure_env_var_completed_2025_11_24(key_name="user_name", func_n=func_n)

        if len(user_email.strip()) == 0:
            user_email = input("user_email=").strip()
            cmd = f'git config --global user.email "{user_email}"'
            code, output = run_command(cmd, capture_output=True)
            logging.debug(output.strip())
            set_text_from_history_file("user_email", user_email)
            label = ensure_status_printed_step(step_counter + 1, cmd, code, output)
            if not ensure_label_process_done(label, start_time):
                raise
            step_counter += 1

        if len(user_name.strip()) == 0:
            user_name = input("user_name=").strip()
            cmd = f'git config --global user.name "{user_name}"'
            code, output = run_command(cmd, capture_output=True)
            logging.debug(output.strip())
            set_text_from_history_file("user_name", user_name)
            label = ensure_status_printed_step(step_counter + 1, cmd, code, output)
            if not ensure_label_process_done(label, start_time):
                raise
            step_counter += 1

        # git add
        logging.debug(PK_UNDERLINE)
        _ensure_git_add(start_time)
        step_counter += 1

        # git commit
        logging.debug(PK_UNDERLINE)
        _ensure_git_commit(start_time, ai_commit_massage_mode, __file__, editable)
        # commit_number = get_next_commit_number()
        step_counter += 1

        # git push (에러 처리 강화)
        logging.debug(PK_UNDERLINE)

        # 현재 브랜치 확인 (에러 처리 강화)
        cmd_branch = "git branch --show-current"
        code_branch, output_branch = run_command(cmd_branch, capture_output=True)
        current_branch = output_branch.strip()
        logging.debug(f"현재 브랜치: {current_branch}")

        # 원격 저장소 확인 (에러 처리 강화)
        cmd_remote = "git remote -v"
        code_remote, output_remote = run_command(cmd_remote, capture_output=True)
        outputs = output_remote.split("\n")
        for output in outputs:
            logging.debug(f"원격 저장소: {output}")

        # 업스트림 브랜치 확인 (에러 처리 강화)
        cmd, code_ahead_behind, output_ahead_behind = _ensure_upstream_branch_checked(current_branch)

        # 실제 푸시 실행
        code, output = _ensure_git_pushed(cmd, code_ahead_behind, output_ahead_behind, current_branch, start_time)
        step_counter += 1

        logging.debug(PK_UNDERLINE)
        if any(protocol in output for protocol in ["To https://", "To http://", "To git@"]):
            pass
        elif "everything up-to-date" in output.lower():
            pass  # TODO
        else:
            label = "FAILED"
            if ensure_git_state_checked(start_time, label) == False:
                raise

        duration = time.time() - start_time
        logging.debug(f"{PK_ANSI_COLOR_MAP['CYAN']}ALL PROCESS COMPLETED SUCCESSFULLY. TOTAL EXECUTION TIME: {duration:.2f} SECONDS {PK_ANSI_COLOR_MAP['RESET']}")

        return {
            "state": True
        }
    except:
        ensure_debug_loged_verbose(traceback=traceback)
    finally:
        os.chdir(pwd)
