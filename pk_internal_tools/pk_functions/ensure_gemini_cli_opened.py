def _open_gemini_cli(local_gemini_root=None):
    from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT
    from pk_internal_tools.pk_functions.ensure_command_executed_like_human import ensure_command_executed_like_human

    if local_gemini_root is None:
        local_gemini_root = D_PK_ROOT
        
    ensure_command_executed_like_human(f'cd "{local_gemini_root}" && gemini')

    # ensure_function_executed_in_new_process(
    #     module_path="pk_internal_tools.pk_functions.ensure_pk_gemini_executed",
    #     function_name="ensure_pk_gemini_executed",
    #     keep_open=True
    # )


def _login_gemini_cli():
    import time

    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_functions.is_gemini_auth_chrome_tab_detected import is_gemini_auth_chrome_tab_detected
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_gemini_cli_logined import ensure_gemini_cli_logined
    # ensure_slept(seconds=2)
    # key_name = '로그인인증창 실행 대기'
    # timeout_seconds_limit = ensure_slept_by_following_history(key_name=key_name, func_n=func_n ,history_reset=history_reset)
    timeout_seconds_limit = 10
    # timeout_seconds_limit = 30
    time_s = time.time()
    while True:
        elapsed = time.time() - time_s
        if elapsed > timeout_seconds_limit:
            # ensure_spoken("제미나이 인증 크롬탭 탐지 타임아웃")
            return
        if is_gemini_auth_chrome_tab_detected():
            # 제미나이 인증 크롬탭 나타나면 로그인 안된것으로 간주
            ensure_spoken("크롬 제미나이 인증 크롬탭 탐지")
            ensure_gemini_cli_logined()
            return
        ensure_slept(milliseconds=500)


def _resize_gemini_cli():
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
    from pk_internal_tools.pk_functions.get_gemini_cli_window_title import get_gemini_cli_window_title
    gemini_cli_window_title = get_gemini_cli_window_title()
    ensure_window_to_front(gemini_cli_window_title)
    ensure_slept(milliseconds=77)


from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_gemini_cli_opened(__file__, local_gemini_root=None, opened=None):
    import traceback

    from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_functions.is_gemini_cli_window_found import is_gemini_cli_window_found
    try:
        if opened is None:
            opened = is_gemini_cli_window_found(local_gemini_root)

        if not opened:
            _open_gemini_cli(local_gemini_root)
            _login_gemini_cli()
            _resize_gemini_cli()

        return True
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
    finally:
        ensure_spoken(read_finished_wait_mode=True)
