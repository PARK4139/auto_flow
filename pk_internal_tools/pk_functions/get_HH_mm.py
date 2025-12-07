def get_HH_mm():
    from datetime import datetime
    now = datetime.now()
    try:
        from pk_internal_tools.pk_functions.get_pk_time_2025_10_20_1200 import get_pk_time_2025_10_20_1200
        HH_mm = get_pk_time_2025_10_20_1200("%H:%M")
    except:
        HH_mm = now.strftime("%H:%M")
    return HH_mm


