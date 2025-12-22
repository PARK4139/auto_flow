from pk_internal_tools.pk_functions.alert_as_gui import alert_as_gui


def ensure_alert_after_at_hh_mm(
        hh_mm_input: str,
        message: str = "알림 시간입니다.",
        test_mode: bool = False
) -> bool:
    """
    지정된 hh:mm 시간 이후에 알림을 발생시킵니다.

    Args:
        hh_mm_input (str): 'HH:MM' 형식의 문자열 (예: '14:30').
        message (str): 알림 발생 시 표시할 메시지.
        test_mode (bool): 테스트 모드 여부. True일 경우 실제 시간 대기 없이 즉시 실행됩니다.

    Returns:
        bool: 알림 설정 및 실행 성공 여부.
    """

    import logging
    import time
    from datetime import datetime, timedelta

    func_n = "ensure_alert_after_at_hh_mm"

    # ensure_pk_system_log_initialized는 래퍼 스크립트에서 호출됩니다.
    # pk_functions 내부 함수에서는 호출하지 않습니다.

    logging.info(f"[{func_n}] 알림 설정 시작. 목표 시간: {hh_mm_input}, 메시지: {message}, 테스트 모드: {test_mode}")

    try:
        # 1. 입력 유효성 검사
        try:
            target_hour, target_minute = map(int, hh_mm_input.split(':'))
            if not (0 <= target_hour <= 23 and 0 <= target_minute <= 59):
                logging.error(f"[{func_n}] hh_mm_input 형식이 잘못되었습니다: {hh_mm_input}. 시간은 0-23, 분은 0-59 사이여야 합니다.")
                return False
        except ValueError:
            logging.error(f"[{func_n}] hh_mm_input 형식이 잘못되었습니다. 'HH:MM' 형식을 따르세요. 입력: {hh_mm_input}")
            return False

        now = datetime.now()
        target_time_today = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)

        # 2. 목표 시간 계산
        if now > target_time_today:
            # 목표 시간이 현재 시간보다 이전이면 다음 날로 설정
            target_time_today += timedelta(days=1)
            logging.info(f"[{func_n}] 목표 시간({hh_mm_input})이 이미 지났으므로 다음 날 {target_time_today.strftime('%H:%M')}에 알림을 설정합니다.")
        else:
            logging.info(f"[{func_n}] 금일 {target_time_today.strftime('%H:%M')}에 알림을 설정합니다.")

        time_to_wait = (target_time_today - now).total_seconds()

        if test_mode:
            logging.info(f"[{func_n}] 테스트 모드이므로 즉시 알림을 발생시킵니다. (대기 시간: {time_to_wait:.2f}초)")
            # 실제 대기 대신 즉시 알림 발생
            # 실제 알림 기능 (TTS, GUI 등)은 이 위치에 추가될 수 있습니다.
            logging.info(f"[{func_n}] 📢 알림: {message}")
            return True
        else:
            logging.info(f"[{func_n}] 알림까지 {time_to_wait:.2f}초 대기합니다...")
            time.sleep(time_to_wait)

            logging.info(f"[{func_n}] 📢 알림: {message}")
            alert_as_gui(text=f"📢 알림: {message}")

            # 실제 알림 기능 (TTS, GUI 등)은 이 위치에 추가될 수 있습니다.
            # 예: TTS 알림을 위해 ensure_spoken 함수를 호출할 수 있습니다.
            # from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
            # ensure_spoken(message)

            return True

    except Exception as e:
        # pk_system_exception_routine은 래퍼 스크립트에서 호출되므로, 여기서는 직접 로깅만 수행
        logging.error(f"[{func_n}] 예외 발생: {e}", exc_info=True)
        return False
