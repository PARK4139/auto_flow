from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured

@ensure_seconds_measured
def ensure_gemini_cli_interactive_mode_executed(local_gemini_root=None):
    import logging

    from pk_internal_tools.pk_functions.ensure_gemini_cli_opened import ensure_gemini_cli_opened
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_functions.get_gemini_prompt_interface_title import get_pk_gemini_title
    from pk_internal_tools.pk_functions.is_pk_gemini_opened import is_pk_gemini_opened
    from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title
    from pk_internal_tools.pk_functions.ensure_window_resized_and_positioned_left_half import ensure_window_resized_and_positioned_left_half
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front

    opened = is_pk_gemini_opened(local_gemini_root)
    pk_gemini_title = get_pk_gemini_title(local_gemini_root)
    if not opened:
        logging.debug(f'gemini cli 종료되어있습니다.')
        logging.debug(f'실행을 시도합니다')

        while ensure_gemini_cli_opened(local_gemini_root=local_gemini_root,__file__=__file__, opened=opened):
            break

    else:
        if is_window_opened_via_window_title(pk_gemini_title):
            logging.debug(f'gemini cli 가 이미 실행중입니다.')
            ensure_window_to_front(pk_gemini_title)
            ensure_window_resized_and_positioned_left_half()
            ensure_spoken(f'', read_finished_wait_mode=True)
            return
