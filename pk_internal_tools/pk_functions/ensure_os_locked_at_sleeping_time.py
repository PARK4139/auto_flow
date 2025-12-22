from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken


def ensure_os_locked_at_sleeping_time():
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    from pk_internal_tools.pk_functions.ensure_power_saved_as_s3 import ensure_power_saved_as_s3
    import logging

    from datetime import datetime, time, timedelta
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept

    def parse_time_ranges(text_list):
        """sample: ["12:00-13:00", "15:00-15:10"] -> [(time(12,0), time(13,0)), (time(15,0), time(15,10))]"""
        ranges = []
        for txt in text_list:
            try:
                start_str, end_str = txt.split("-")
                h1, m1 = map(int, start_str.strip().split(":"))
                h2, m2 = map(int, end_str.strip().split(":"))
                ranges.append((time(h1, m1), time(h2, m2)))
            except Exception as e:
                continue
        return ranges

    def is_now_in_time_ranges(now_time, time_ranges):
        """현재 시간이 설정된 시간 범위에 속하는지 확인 (자정 포함)"""
        for start, end in time_ranges:
            # 시작 시간이 종료 시간보다 늦는 경우 (예: 23:00-05:00)
            if start > end:
                if now_time >= start or now_time <= end:
                    return True
            # 일반적인 경우 (예: 09:00-18:00)
            else:
                if start <= now_time <= end:
                    return True
        return False

    def is_warning_time(now_time, time_ranges, warning_minutes=15):
        """예약된 시간 warning_minutes분 전인지 확인"""
        for start, end in time_ranges:
            # 시작 시간 15분 전 계산
            warning_time = (datetime.combine(datetime.today(), start) - timedelta(minutes=warning_minutes)).time()
            if warning_time <= now_time < start:
                return True
        return False

    ensure_spoken("시스템 통제를 시작합니다")

    range_reserved = ["23:00-05:00"]  # pk_option

    # 파싱
    all_time_blocks = parse_time_ranges(range_reserved)

    last_cleared_min = -1  # 아직 클리어된 적 없음을 의미
    try:
        ensure_spoken("나이트 튜토리얼으로서, 시스템 통제를 시작합니다")
        while True:
            now = datetime.now()
            now_time = now.time()
            current_min = now.minute

            # 분이 바뀌었을 때만 콘솔 클리어
            if current_min != last_cleared_min:
                # ensure_console_cleared()
                last_cleared_min = current_min
                logging.debug(f"current_tiem={now.strftime('%H:%M:%S')}")

            # 시간 블럭에 해당하면 잠금
            if is_now_in_time_ranges(now_time, all_time_blocks):
                ensure_spoken("시스템 잠금 모드 활성화")
                if is_os_windows():
                    logging.debug("Windows 절전 모드로 전환")
                    ensure_power_saved_as_s3()
                # elif is_os_wsl_linux():
                #     logging.debug("Linux 절전 모드로 전환")
                #     ensure_power_saved_as_s3()
                else:
                    logging.debug("지원되지 않는 OS")
            else:
                logging.debug(f"예약된 시간이 아닙니다. current_tiem={now.strftime('%H:%M:%S')}  range_reserved={range_reserved} ")
                break

            ensure_slept(milliseconds=1000)

    except KeyboardInterrupt:
        logging.debug(" 사용자에 의해 모니터링이 중단되었습니다.")
    except Exception as e:
        logging.debug(f"오류 발생: {e}")
        logging.debug("모니터링을 재시작합니다...")
        # 재시작 로직 (선택사항)
        # ensure_os_locked_v4()
