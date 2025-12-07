def get_today_day_info():
    from pk_internal_tools.pk_functions.get_weekday import get_weekday
    from pk_internal_tools.pk_functions.get_pk_time_2025_10_20_1200 import get_pk_time_2025_10_20_1200
    yyyy = get_pk_time_2025_10_20_1200(time_pattern='pk_year')
    MM = get_pk_time_2025_10_20_1200(time_pattern='pk_month')
    dd = get_pk_time_2025_10_20_1200(time_pattern='pk_day')
    HH = get_pk_time_2025_10_20_1200(time_pattern='pk_hour')
    mm = get_pk_time_2025_10_20_1200(time_pattern='pk_minute')
    week_name = get_weekday()
    return f'{int(yyyy)} {int(MM)} {int(dd)} {week_name} {int(HH)} {int(mm)}'
