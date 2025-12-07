

def is_newyear():
    yyyy = get_pk_time_2025_10_20_1159('%Y')
    state_yearly = None
    if is_month(mm=1) and is_day(dd=1):
        return 1
    else:
        return 0
