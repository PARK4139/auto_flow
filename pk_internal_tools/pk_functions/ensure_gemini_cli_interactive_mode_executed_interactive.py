import logging

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_gemini_cli_interactive_mode_executed_interactive(__file__):
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_gemini_cli_installed_for_one_session import ensure_gemini_cli_installed_for_one_session
    from pk_internal_tools.pk_functions.is_gemini_installed import is_gemini_installed
    from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
    from pk_internal_tools.pk_functions.ensure_gemini_cli_opened import ensure_gemini_cli_opened
    from pk_internal_tools.pk_functions.ensure_gemini_cli_interactive_mode_prompt_sent import ensure_gemini_cli_interactive_mode_prompt_sent
    from pk_internal_tools.pk_functions.ensure_window_resized_and_positioned_left_half import ensure_window_resized_and_positioned_left_half
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
    from pk_internal_tools.pk_functions.get_gemini_cli_window_title import get_gemini_cli_window_title
    from pk_internal_tools.pk_functions.get_gemini_cli_interactive_mode_initial_prompt import get_gemini_cli_interactive_mode_initial_prompt
    from pk_internal_tools.pk_functions.is_gemini_cli_window_found import is_gemini_cli_window_found

    opened = is_gemini_cli_window_found()
    logging.debug(f'opened={opened}')

    installed = is_gemini_installed()  # 최신버전 설치인지 확인하는게 어떨까?
    logging.debug(f'installed={installed}')

    if not installed:
        ensure_gemini_cli_installed_for_one_session(installed)
        ensure_slept(milliseconds=1000 * 60)

    if not opened:
        if not ensure_gemini_cli_opened(__file__=__file__, opened=opened):
            return False
        while 1:
            opened = is_gemini_cli_window_found()
            logging.debug(f'opened={opened}')
            if opened:
                ensure_gemini_cli_interactive_mode_prompt_sent([get_gemini_cli_interactive_mode_initial_prompt()])
                ensure_slept(milliseconds=1000)  # 실패 거의 없었음. # 이벤트로 만들 방법을 못찾음
                # ensure_slept(milliseconds=500)
                return True
            ensure_slept(milliseconds=10)

    gemini_cli_window_title = get_gemini_cli_window_title()
    if is_window_opened_via_window_title(gemini_cli_window_title):
        logging.info(f'gemini 가 이미 실행중입니다.')
        ensure_window_to_front(gemini_cli_window_title)
        ensure_window_resized_and_positioned_left_half()
        # ensure_spoken(f'', wait=True)
        return True
