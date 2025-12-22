from datetime import date, timedelta

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured




@ensure_seconds_measured
def get_calendar(year: int | None = None, month: int | None = None,
                 fmt: str = "YYYY MM DD (weekday)") -> list[str]:
    """
    # n. 올해 전체 (기본 포맷)
    all_this_year = get_calendar()

    # 2) 2025년 전체 (한국식 포맷)
    all_2025_kr = get_calendar(2025, fmt="YYYY년 M월 D일 (weekday)")

    # 3) 2025년 10월만
    oct_2025 = get_calendar(2025, 10)

    # 4) 이번 달만
    this_month = get_calendar(month=date.today().month)

    """
    # datetime.weekday(): 월=0 ... 일=6
    KOREAN_WEEKDAYS = ["월", "화", "수", "목", "금", "토", "일"]
    try:
        today = date.today()
        year = year or today.year

        if month is None:
            # 연초 ~ 연말
            start = date(year, 1, 1)
            end = date(year, 12, 31)
        else:
            # 해당 월의 1일 ~ 말일
            start = date(year, month, 1)
            # 다음 달 1일에서 하루 빼기
            if month == 12:
                next_month_first = date(year + 1, 1, 1)
            else:
                next_month_first = date(year, month + 1, 1)
            end = next_month_first - timedelta(days=1)

        out = []
        d = start
        while d <= end:
            wd = KOREAN_WEEKDAYS[d.weekday()]
            if fmt == "YYYY MM DD (weekday)":
                s = f"{d.year:04d} {d.month:02d} {d.day:02d} ({wd})"
            elif fmt == "YYYY년 M월 D일 (weekday)":
                s = f"{d.year}년 {d.month}월 {d.day}일 ({wd})"
            else:
                # 간단한 토큰 치환 (필요 시 확장 가능)
                s = (fmt.replace("YYYY", f"{d.year:04d}")
                     .replace("MM", f"{d.month:02d}")
                     .replace("DD", f"{d.day:02d}")
                     .replace("(weekday)", f"({wd})"))
            out.append(s)
            d += timedelta(days=1)
        return out

    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
    finally:
        pass


