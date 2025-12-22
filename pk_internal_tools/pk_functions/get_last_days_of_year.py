from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_last_days_of_year(year: int):
    """
        TODO: Write docstring for get_last_days_of_year.
    """
    try:

        import calendar
        """
        해당 년도의 각 달의 말일을 출력하는 함수. 
        """
        last_days = []
        for month in range(1, 13):
            last_day = calendar.monthrange(year, month)[1]  # 해당 월의 말일 계산
            last_days.append((year, month, last_day))
        return last_days
    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
