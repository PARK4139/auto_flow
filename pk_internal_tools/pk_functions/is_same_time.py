




from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


def is_same_time(time1, time2):
    time2.strftime(rf'%Y-%m-%d %H:%M:%S')
    if QC_MODE:
        print(rf'time1 : {time1} , time2 : {time2}')
    if time1 == time2:
        return 1
    else:
        return 0
