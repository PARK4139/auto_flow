def get_current_interval(pk_db, func_n, INTERVAL_ORIGIN):
    from pk_internal_tools.pk_functions.get_db_id import get_db_id

    values = pk_db.get_state_value(db_id=get_db_id(key_name="speed_control_interval_ms", func_n=func_n))
    if values:
        try:
            return int(values[0])
        except:
            pass
    return INTERVAL_ORIGIN
