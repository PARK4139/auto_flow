from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_objects.pk_ttl_cache_manager import ensure_pk_ttl_cached


@ensure_seconds_measured
@ensure_pk_ttl_cached(ttl_seconds=60 * 1 * 1, maxsize=10)
def get_pk_program_language():
    """
    pk_system 프로그램 언어를 반환하는 함수
    
    Returns:
        str: "kr" 또는 "en" (기본값: "english" on error)
    """
    import logging
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    
    try:
        if QC_MODE:
            return "korean"
        
        from pk_internal_tools.pk_functions.get_file_id import get_file_id
        from pk_internal_tools.pk_functions.get_values_from_historical_file_routine import get_values_from_historical_file_routine
        from pk_internal_tools.pk_functions.get_values_from_historical_database_routine import get_values_from_historical_database_routine
        from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        
        func_n = get_caller_name()
        db = PkSqlite3()
        
        key_hint1 = "is_pk_initial_launched"
        is_pk_initial_launched = db.get_values_2025(db_id=db.get_db_id(key_hint1, func_n))
        if is_pk_initial_launched is None:
            is_pk_initial_launched = True
            logging.debug(f"is_pk_initial_launched={is_pk_initial_launched}")
            if QC_MODE:
                logging.debug(f"type={type(is_pk_initial_launched)}")
                logging.debug(f"is_pk_initial_launched is True={is_pk_initial_launched is True}")
        
        key_name = "pk_program_language"
        if is_pk_initial_launched is True:
            logging.debug("pk system First launch detected")
            pk_program_language = get_values_from_historical_file_routine(
                file_id=get_file_id(key_name, func_n),
                key_hint=key_name,
                options=["kr", "en"],
                editable=True
            )
            db.set_values(db_id=db.get_db_id(key_name, func_n), values=pk_program_language)
            db.set_values(db_id=db.get_db_id(key_hint1, func_n), values=False)
        else:
            logging.debug("Subsequent launch")
            pk_program_language = db.get_values_2025(db_id=db.get_db_id(key_name, func_n))
            
            if pk_program_language is None:
                logging.debug(f"{key_name} is missing. Re-configuring...")
                pk_program_language = get_values_from_historical_database_routine(
                    db_id=db.get_db_id(key_name, func_n),
                    key_hint=f"{key_name}=",
                    values_default=["kr", "en"]
                )
                db.set_values(db_id=db.get_db_id(key_name, func_n), values=pk_program_language)
        
        logging.debug(f"{func_n} {key_name} = {pk_program_language}")
        return pk_program_language
    except Exception as e:
        logging.warning(f"get_pk_program_language 오류: {e}")
        return "english"
