from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pk_language_reset():
    import logging
    import traceback

    from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.reset_pk_language import reset_pk_language
    from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3

    try:
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        func_n = get_caller_name()
        db = PkSqlite3()

        reset_pk_language(db, func_n)

        key_name = "pk_language"
        selected = ensure_value_completed(key_name=key_name, func_n=func_n, options=["korean", "english"])
        pk_language = selected

        db.set_values(db_id=db.get_db_id(key_name, func_n), values=pk_language)
        pk_language = db.get_state_value(db_id=db.get_db_id(key_name, func_n))
        logging.debug(f'pk_language={pk_language}')
    except Exception as e:
        ensure_debugged_verbose(traceback=traceback, e=e)
