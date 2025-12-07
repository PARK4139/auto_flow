def get_pk_time_2025_10_20_1159(pattern: str):
    from pk_internal_tools.pk_functions.get_weekday import get_weekday
    import time
    from datetime import datetime
    now = datetime.now()
    weekday = get_weekday()
    epoch_time = time.time()
    seconds = int(epoch_time)
    nanoseconds = int((epoch_time - seconds) * 1e9)  # 나노초 부분
    milliseconds = (now.microsecond // 1000)  # 마이크로초 ->> 밀리초
    time_styles = {
        'now': f"{now.year}_{now.month:02}_{now.day:02}_{weekday}_{now.hour:02}_{now.minute:02}_{now.second:02}_{milliseconds:03}_{nanoseconds:09}",
        'yyyy': str(now.year),
        'MM': str(now.month).zfill(2),
        'dd': str(now.day).zfill(2),
        'HH': str(now.hour).zfill(2),
        'mm': str(now.minute).zfill(2),
        'ss': str(now.second).zfill(2),
        'fff': str(milliseconds).zfill(3),  # 밀리초
        'fffffff': str(nanoseconds).zfill(9),  # 나노초
        'weekday': weekday,
        'elapsed_days_from_jan_01': str(now.timetuple().tm_yday),  # 금년 1월 1일부터 오늘까지의 일수
        'yyyy MM dd (weekday) HH mm': f"{now.year} {now.month:02} {now.day:02} ({weekday}) {now.hour:02} {now.minute:02}",
        'yyyy MM dd (weekday) HH:mm': f"{now.year} {now.month:02} {now.day:02} ({weekday}) {now.hour:02}:{now.minute:02}",
        'yyyy MM dd weekday HH mm ss': f"{now.year} {now.month:02} {now.day:02} {weekday} {now.hour:02} {now.minute:02} {now.second:02}",
        'yyyy MM dd weekday HH mm ss fff': f"{now.year} {now.month:02} {now.day:02} {weekday} {now.hour:02} {now.minute:02} {now.second:02} {milliseconds:03}",
        'yyyy MM dd weekday HH mm ss fff ffffff': f"{now.year} {now.month:02} {now.day:02} {weekday} {now.hour:02} {now.minute:02} {now.second:02} {milliseconds:03} {nanoseconds:09}",
        'yyyy MM dd weekday HHmm': f"{now.year} {now.month:02} {now.day:02} {weekday} {now.hour:02} {now.minute:02}",
        'yyyy MM dd weekday': f"{now.year} {now.month:02} {now.day:02} {weekday}",
    }
    if pattern in time_styles:
        return time_styles[pattern]
    return now.strftime(pattern)

