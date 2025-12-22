def _play_alarm_sound():
    """알람 사운드 재생"""
    import winsound
    import time

    import logging

    from pk_internal_tools.pk_objects.pk_colors import PkColors
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    for i in range(2):
        logging.debug(f"[{PkTexts.ALARM_BACKGROUND_RUNNING}] {PkColors.RED}사운드={i + 1}/{len(range(2))} {PkColors.RESET}")
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)  # 경고음
        time.sleep(0.6)


def _alarm_thread(alarm_message_for_gui, seconds):
    import time

    import logging

    from pk_internal_tools.pk_functions.ensure_paused import ensure_paused

    from pk_internal_tools.pk_functions.alert_as_gui import alert_as_gui
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken

    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front

    """알람 스레드 - 지정된 시간 후 알람 울리기"""
    try:

        # 카운트다운 표시
        remaining_seconds = seconds
        while remaining_seconds > 0:
            if remaining_seconds % 60 == 0:  # 1분마다 표시
                minutes_left = remaining_seconds // 60
                logging.debug(f"남은 시간: {minutes_left}분")
            elif remaining_seconds <= 10:  # 10초 이하일 때는 초 단위로 표시
                logging.debug(f"남은 시간: {remaining_seconds}초")

            time.sleep(1)
            remaining_seconds -= 1

        # 알람 시간 도달 - 알람 울리기
        ensure_window_to_front(alarm_message_for_gui)
        _play_alarm_sound()
        try:
            logging.debug(f"알람 내용 읽는 중...")
            ensure_spoken(alarm_message_for_gui, read_finished_wait_mode=True)
            alert_as_gui(text=alarm_message_for_gui)
        except Exception as e:
            logging.debug(f"알람 내용 읽기 오류: {e}")
            ensure_paused()

    except Exception as e:
        logging.debug(f"알람 스레드 오류: {e}")
        ensure_paused()


def ensure_alert_after_seconds_promised(alarm_message_for_gui=None, seconds=None):
    import threading

    import logging

    from pk_internal_tools.pk_objects.pk_colors import PkColors
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    # 알람 스레드 시작
    thread = threading.Thread(
        target=_alarm_thread,
        args=(alarm_message_for_gui, seconds),
        daemon=False  # 데몬=False로 변경하여 메인 프로그램 종료와 독립적으로 실행
    )
    thread.start()

    logging.debug(f"[{PkTexts.ALARM_BACKGROUND_RUNNING}] {PkColors.CYAN}상태=백그라운드실행 {PkColors.RESET}")
    logging.debug("프로그램을 종료해도 알람은 계속 작동합니다.")
    logging.debug("입력값이 히스토리에 저장되어 다음에 자동완성됩니다.")

    # 알람 스레드가 완료될 때까지 대기 (선택사항)
    # thread.join()
