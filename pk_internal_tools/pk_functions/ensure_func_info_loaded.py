from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3


def ensure_func_info_loaded(func_n):
    """
    함수 정보를 데이터베이스에서 로드합니다.
    데이터가 없으면 기본값을 반환합니다.
    """
    pk_db = PkSqlite3()
    db_id = f"values_via_{func_n}"
    func_data = pk_db.get_state_value(db_id=db_id)
    
    # None인 경우 기본 구조 반환
    if func_data is None:
        func_data = {
            "title": f"Unknown Function: {func_n}",
            "description": f"No information available for {func_n}",
            "func_n": func_n
        }
    
    # dict가 아닌 경우에도 안전하게 처리
    if not isinstance(func_data, dict):
        func_data = {
            "title": str(func_data) if func_data is not None else f"Unknown Function: {func_n}",
            "description": f"Raw data: {func_data}",
            "func_n": func_n
        }
    
    # title 키가 없으면 추가
    if "title" not in func_data:
        func_data["title"] = f"Function: {func_n}"
    
    return func_data
