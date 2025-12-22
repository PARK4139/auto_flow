def get_values_from_historical_database_routine_v2(db_id, key_hint, values_default, editable):
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3
    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.get_list_deduplicated import get_list_deduplicated

    def ensure_list(val):
        if val is None:
            return []
        if isinstance(val, str):
            return [val]
        return list(val)

    # Load from DB
    db = PkSqlite3()
    values_loaded = ensure_list(db.get_state_value(db_id=db_id))
    values_default = ensure_list(values_default)

    if editable:
        # TODO dbeaber 로 가능한지 가능하면 열기
        pass

    # Debug
    if QC_MODE:
        print(f"values_default={values_default} ")
        print(f"type(values_default)={type(values_default)} ")

    # Merge and ask user
    values_optional = values_default + values_loaded
    user_value = ensure_value_completed(key_name=key_hint, options=values_optional)
    user_value = user_value.strip()
    print(f'''type(user_value)={type(user_value)} ''')
    print(f'''user_value={user_value} ''')

    # Save and return
    values_to_save = get_list_deduplicated([user_value] + values_loaded)
    print(f'''values_to_save={values_to_save} ''')
    print(f'''type(values_to_save)={type(values_to_save)} ''')
    db.set_values(db_id=db_id, values=values_to_save)
    return user_value
