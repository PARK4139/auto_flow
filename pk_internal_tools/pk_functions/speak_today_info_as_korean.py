def speak_today_info_as_korean():
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_functions.get_pk_time_2025_10_20_1159 import get_pk_time_2025_10_20_1159

    yyyy = get_pk_time_2025_10_20_1159('%Y')
    MM = get_pk_time_2025_10_20_1159('%m')
    dd = get_pk_time_2025_10_20_1159('%d')

    ensure_spoken(text=f'{int(yyyy)}년 {int(MM)}월 {int(dd)}일', after_delay=0.95)
