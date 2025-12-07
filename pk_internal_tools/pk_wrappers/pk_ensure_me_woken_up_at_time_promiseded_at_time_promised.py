
#  get_seconds_from_HH_mm,
#  set_wake_up_next_HH_mm



def get_yyyy_MM_dd_hh_mm_from_seconds(seconds: int):
    yyyy = 0
    MM = 0  # 월
    dd = 0  # 일
    hh = seconds // 3600  # 시간 계산
    remaining_seconds = seconds % 3600
    mm = remaining_seconds // 60  # 분 계산

    return yyyy, MM, dd, hh, mm


def get_hh_mm_from_seconds(seconds):
    # 전체 초에서 시간을 계산
    hours = seconds // 3600
    # 남은 초에서 분을 계산
    minutes = (seconds % 3600) // 60
    return hours, minutes


def convert_to_seconds(dd: int, hh: int, mm: int) -> int:
    """
    일(dd), 시간(hh), 분(mm)을 초로 변환하는 함수.

    Args:
        dd (int): 일 수
        hh (int): 시간
        mm (int): 분

    Returns:
        int: 총 초 단위 값
    """
    total_seconds = dd * 86400 + hh * 3600 + mm * 60
    return total_seconds


def get_last_days_of_year(year: int):
    import calendar
    """
    해당 년도의 각 달의 말일을 출력하는 함수. 
    """
    last_days = []
    for month in range(1, 13):
        last_day = calendar.monthrange(year, month)[1]  # 해당 월의 말일 계산
        last_days.append((year, month, last_day))
    return last_days


if __name__ == "__main__":
    try:
        # todo

        # sleep_and_wake_up_at_HH_mm()
        # yyyy, MM, dd, hh, mm = get_yyyy_MM_dd_hh_mm_from_seconds(seconds=21600)
        # hh, mm = get_hh_mm_from_seconds(seconds=21600)
        # seconds = convert_to_seconds(dd, hh, mm)
        # print(f"{hh}hour {mm}min")

        # 6시간(21600초) 후에 깨우기
        seconds = get_seconds_from_HH_mm(HH=0, mm=3)
        # set_wake_up_via_schtasks(seconds=seconds)
        set_wake_up_next_HH_mm(HH=21, mm=19)
        # powercfg -h off
        # ensure_command_executed(cmd=rf"rundll32.exe powrprof.dll,SetSuspendState Sleep")
        # change_os_mode_to_power_saving_mode_as_s3()
        # change_os_mode_to_power_saving_mode_as_s4()

        # last_days = get_last_days_of_year(2025) #  [(2025, 1, 31), (2025, 2, 28), ..., (2025, 12, 31)]
    except:
        f_current_n= get_f_current_n()
        d_current_n=get_d_current_n_like_human()
        ensure_finally_routine_done(traced_file=__file__, d_pk_system=d_pk_system)
        traceback_format_exc_list = traceback.format_exc().split("\n")
        
        logging.debug(f'{PK_UNDERLINE}')
        for traceback_format_exc_str in traceback_format_exc_list:
            logging.debug(f'{STAMP_EXCEPTION_OCCURED} {traceback_format_exc_str}')
        logging.debug(f'{PK_UNDERLINE}')

        logging.debug(f'{PK_UNDERLINE}\n')
        logging.debug(f'{'[ DEBUGGING NOTE ]'} f_current={f_current_n}\nd_current={d_current_n}\n')
        logging.debug(f'{PK_UNDERLINE}\n')

        