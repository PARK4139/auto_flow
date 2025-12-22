from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3


def ensure_func_info_saved(func_n, func_data):
    pk_db = PkSqlite3()
    db_id = f"values_via_{func_n}"
    pk_db.reset_values(db_id=db_id)
    pk_db.set_values(db_id=db_id, values=func_data)
    return func_data
