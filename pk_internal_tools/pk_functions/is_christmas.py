








def is_christmas():
    yyyy = get_pk_time_2025_10_20_1159('%Y')
    if is_month(mm=12) and is_day(dd=25):
        return 1
    else:
        return 0
