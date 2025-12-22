

def get_values_from_historical_database_routine_v1(db_id, key_hint, values_default):
    from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3
    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.get_list_deduplicated import get_list_deduplicated
    db = PkSqlite3()
    values_loaded = db.get_state_value(db_id=db_id)
    if QC_MODE:
        print(f'''values_default={values_default} ''')
        print(f'''type(values_default)={type(values_default)} ''')
    if isinstance(values_loaded, str):
        values_loaded = [values_loaded]
    if isinstance(values_default, str):
        values_default = [values_default]
    if values_default is None:
        values_default = []
    if values_loaded is None:
        values_loaded = []
    values_optional = values_default + values_loaded
    user_value = ensure_value_completed(key_name=key_hint, options=values_optional)
    user_value = user_value.strip()
    values_to_save = get_list_deduplicated([user_value] + values_loaded)
    db.set_values(db_id=db_id, values=values_to_save)
    return user_value


