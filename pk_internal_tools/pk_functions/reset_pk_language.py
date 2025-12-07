

def reset_pk_language(db, func_n):
    key_name = "is_pk_initial_launched"
    db.reset_values(db_id=db.get_db_id(key_name, func_n))
    key_name = "pk_language"
    db.reset_values(db_id=db.get_db_id(key_name, func_n))


