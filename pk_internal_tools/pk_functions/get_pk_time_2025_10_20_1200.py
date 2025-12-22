def get_pk_time_2025_10_20_1200(time_pattern: str, base=None) -> str:
    import re
    import time
    from datetime import datetime
    # from pk_internal_tools.pk_functions.get_weekday import get_weekday  # not needed now

    def _parse_base_dt(b):
        if b is None:
            return datetime.now()
        if isinstance(b, datetime):
            return b
        s = str(b).strip()
        for fmt in (
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y/%m/%d %H:%M:%S",
            "%Y/%m/%d %H:%M",
            "%Y_%m_%d_%H%M%S",
            "%Y_%m_%d_%H%M",
            "%Y%m%d%H%M%S",
            "%Y%m%d%H%M",
            "%Y-%m-%d",
        ):
            try:
                return datetime.strptime(s, fmt)
            except ValueError:
                pass
        try:
            return datetime.fromisoformat(s)
        except Exception as e:
            raise ValueError(f"Unsupported datetime string format: {s}")

    now = _parse_base_dt(base)

    # Weekday based on 'now' (i.e., base), Korean short names without "요일"
    _weekday_names = ["월", "화", "수", "목", "금", "토", "일"]
    weekday = _weekday_names[now.weekday()]

    epoch_time = time.mktime(now.timetuple()) + now.microsecond / 1_000_000
    epoch_seconds = int(epoch_time)
    epoch_millis = int(epoch_time * 1_000)
    epoch_nanos = int(epoch_time * 1_000_000_000)

    milliseconds = now.microsecond // 1000
    nanoseconds_9 = (now.microsecond * 1000) % 1_000_000_000

    token_map = {
        "pk_year": f"{now.year}",
        "pk_month": f"{now.month:02}",
        "pk_day": f"{now.day:02}",
        "pk_hour": f"{now.hour:02}",
        "pk_minute": f"{now.minute:02}",
        "pk_second": f"{now.second:02}",
        "pk_millis": f"{milliseconds:03}",
        "pk_nanos": f"{nanoseconds_9:09}",
        "pk_weekday": weekday,  # base 기준
        "pk_fff": f"{milliseconds:03}",
        "pk_fffffff": f"{nanoseconds_9:09}",
        "pk_fffffffff": f"{nanoseconds_9:09}",
        "pk_elapsed_days_from_jan_01": f"{now.timetuple().tm_yday}",
        "pk_epoch_seconds": f"{epoch_seconds}",
        "pk_epoch_millis": f"{epoch_millis}",
        "pk_epoch_nanos": f"{epoch_nanos}",
        "now": f"{now.year}_{now.month:02}_{now.day:02}_{weekday}_{now.hour:02}_{now.minute:02}_{now.second:02}_{milliseconds:03}_{nanoseconds_9:09}",
    }

    tokens_sorted = sorted(token_map.keys(), key=len, reverse=True)
    pattern_re = re.compile(r"(?<!\\)(" + "|".join(map(re.escape, tokens_sorted)) + r")")

    def _repl(m):
        return token_map[m.group(1)]

    replaced = pattern_re.sub(_repl, time_pattern)

    esc_re = re.compile(r"\\(" + "|".join(map(re.escape, tokens_sorted)) + r")")
    replaced = esc_re.sub(lambda m: m.group(1), replaced)

    try:
        replaced = now.strftime(replaced)
    except Exception as e:
        pass

    return replaced
