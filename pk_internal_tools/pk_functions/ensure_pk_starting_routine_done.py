from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pk_starting_routine_done(*, traced_file, traceback, window_relocate_mode=True):
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    import logging

    from pk_internal_tools.pk_functions.ensure_window_resized_and_positioned_left_half import ensure_window_resized_and_positioned_left_half
    from pk_internal_tools.pk_objects.pk_windows_state_manager import pk_windows_state_manager
    from pk_internal_tools.pk_functions.ensure_pk_colorama_initialized_once import ensure_pk_colorama_initialized_once
    from pk_internal_tools.pk_functions.ensure_pk_log_initialized import ensure_pk_log_initialized
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_window_title_replaced import ensure_pk_wrapper_starter_window_title_replaced

    # if is_windows_os():
    #     ensure_chcp_65001()

    # pk_option
    # if is_os_windows():
    #     ensure_chcp_65001()

    if window_relocate_mode:
        ensure_window_resized_and_positioned_left_half()  # -> succeeded
    # ensure_pressed("f11")  # -> succeeded

    ensure_pk_wrapper_starter_suicided(traced_file)
    ensure_pk_colorama_initialized_once()
    ensure_pk_log_initialized(traced_file)
    ensure_pk_wrapper_starter_window_title_replaced(traced_file)

    # ensure_windows_killed_like_human_by_window_title(window_title="cmd.exe") # pk_* -> 위험한 코드
    # ensure_windows_killed_like_person()

    helper = pk_windows_state_manager
    if not helper.is_window_title_db_thread_executed():
        helper.ensure_windows_updater_started(update_interval_seconds=0.4)  # 애플리케이션 시작 시 한 번만 호출(window title db 캐시 업데이트 스레드 시작)하면 됩니다.
        logging.info("백그라운드 윈도우 업데이트 스레드가 시작되었습니다.")
        # ensure_slept(500)  # 스레드가 초기 데이터를 가져올 시간대기
        # ensure_slept(milliseconds=22)
        ensure_slept(milliseconds=2)
