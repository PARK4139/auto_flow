# editable = True  # pk_option
from pk_internal_tools.pk_functions import ensure_console_cleared, ensure_spoken
from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
from pk_internal_tools.pk_objects.pk_texts import PkTexts

editable = False  # pk_option


def parse_time_input(time_str):
    import re

    import logging

    """시간 문자열을 파싱하여 초 단위로 변환"""
    try:
        # 정규식으로 숫자와 단위 추출
        pattern = r'^(\d+)\s*(초|분|시간|시)$'
        match = re.match(pattern, time_str.strip())

        if not match:
            return None, None

        value = int(match.group(1))
        unit = match.group(2)

        # 단위별 초 계산
        if unit == "초":
            seconds = value
            unit_display = "초"
        elif unit == "분":
            seconds = value * 60
            unit_display = "분"
        elif unit in ["시간", "시"]:
            seconds = value * 3600
            unit_display = "시간"
        else:
            return None, None

        return seconds, unit_display

    except Exception as e:
        logging.debug(f"시간 파싱 오류: {e}")
        return None, None


def get_time_input():
    import inspect

    import logging
    from pk_internal_tools.pk_functions.get_file_id import get_file_id
    from pk_internal_tools.pk_functions.get_values_from_historical_file_routine import get_values_from_historical_file_routine
    try:
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()

        # 알람 내용 입력 (히스토리 + 자동완성 지원)
        key_name = "alarm_content"
        alarm_content = get_values_from_historical_file_routine(
            file_id=get_file_id(key_name, func_n),
            key_hint=f'{key_name}=',
            options=[],
            editable=editable
        )

        key_name = "time_input"
        default_time_options = [
            "1초", "2초", "3초", "5초", "10초", "30초", "1분", "5분", "10분", "15분", "30분",
            "1시간", "2시간", "3시간", "5시간", "10시간"
        ]
        time_input = get_values_from_historical_file_routine(
            file_id=get_file_id(key_name, func_n),
            key_hint=f'{key_name}=',
            options=default_time_options,
            editable=editable
        )
        if not time_input or not time_input.strip():
            logging.debug("시간을 입력하지 않았습니다.")
            ensure_spoken("시간을 입력하지 않았습니다.")
            return None, None, None

        # 시간 파싱
        seconds, unit = parse_time_input(time_input)

        if seconds is None:
            logging.debug("올바른 시간 형식을 입력하세요. (예: 10초, 5분, 1시간)")
            return None, None, None

        if not alarm_content or not alarm_content.strip():
            alarm_content = f"{time_input} 시간경과 알람입니다!"

        return alarm_content, seconds, unit

    except Exception as e:
        logging.debug(f"입력 중 오류 발생: {e}")
        return None, None, None


def play_alarm_sound():
    """알람 사운드 재생"""
    import winsound
    import time

    import logging

    for i in range(2):
        logging.debug(f"[{PkTexts.ALARM_BACKGROUND_RUNNING}] {PK_ANSI_COLOR_MAP['RED']}사운드={i + 1}/{len(range(2))} {PK_ANSI_COLOR_MAP['RESET']}")
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)  # 경고음
        time.sleep(0.6)


def alarm_thread(alarm_content, seconds, unit):
    import time
    from datetime import datetime, timedelta

    import logging
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced

    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front

    """알람 스레드 - 지정된 시간 후 알람 울리기"""
    try:
        # 현재 시간과 알람 시간 계산
        now = datetime.now()
        alarm_time = now + timedelta(seconds=seconds)

        ensure_window_title_replaced(alarm_content)

        ensure_console_cleared()
        logging.debug(f"알람 설정 완료!")
        logging.debug(f"현재 시간: {now.strftime('%H:%M:%S')}")
        logging.debug(f"알람 시간: {alarm_time.strftime('%H:%M:%S')}")
        logging.debug(f"대기 시간: {seconds}초")
        logging.debug(f"알람 내용: {alarm_content}")

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

        # 알람 시간 도달 - 루프 시작
        while True:
            ensure_console_cleared()
            ensure_window_to_front(alarm_content)
            play_alarm_sound()
            try:
                logging.debug(f"알람 내용 읽는 중...")
                ensure_spoken(alarm_content)
            except Exception as e:
                logging.debug(f"알람 내용 읽기 오류: {e}")

            time.sleep(2)

    except Exception as e:
        logging.debug(f"알람 스레드 오류: {e}")


def ensure_alert_after_time_promised(alarm_content=None, seconds=None, unit=None):
    import threading

    import logging

    """약속된 시간 후 알람 울리기 (자동완성 + 히스토리 지원)
    
    Args:
        alarm_content (str, optional): 알람 내용. None이면 사용자 입력 받음
        seconds (int, optional): 대기 시간(초). None이면 사용자 입력 받음
        unit (str, optional): 시간 단위. None이면 사용자 입력 받음
    """
    # 인자가 제공되지 않은 경우 사용자 입력 받기
    if alarm_content is None or seconds is None or unit is None:
        input_alarm_content, input_seconds, input_unit = get_time_input()

        if input_alarm_content is None:
            logging.debug("알람 설정을 취소합니다.")
            return

        # 인자가 None인 경우에만 사용자 입력값 사용
        alarm_content = alarm_content or input_alarm_content
        seconds = seconds or input_seconds
        unit = unit or input_unit

    # 알람 스레드 시작
    thread = threading.Thread(
        target=alarm_thread,
        args=(alarm_content, seconds, unit),
        daemon=False  # 데몬=False로 변경하여 메인 프로그램 종료와 독립적으로 실행
    )
    thread.start()

    logging.debug(f"[{PkTexts.ALARM_BACKGROUND_RUNNING}] {PK_ANSI_COLOR_MAP['CYAN']}상태=백그라운드실행 {PK_ANSI_COLOR_MAP['RESET']}")
    logging.debug("프로그램을 종료해도 알람은 계속 작동합니다.")
    logging.debug("입력값이 히스토리에 저장되어 다음에 자동완성됩니다.")

    # 알람 스레드가 완료될 때까지 대기 (선택사항)
    # thread.join()
