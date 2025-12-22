def reset_is_pk_initial_launched(db, key_hint1, func_n):
    """
    pk_system 초기 실행 상태를 리셋하는 함수
    
    Args:
        db: PkSqlite3 인스턴스
        key_hint1: 초기 실행 상태 키 힌트
        func_n: 호출자 함수명
    """
    db.set_values(db_id=db.get_db_id(key_hint1, func_n), values=True)
