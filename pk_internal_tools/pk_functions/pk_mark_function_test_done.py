# @ensure_seconds_measured
def pk_mark_function_test_done(func):
    """
        "동작검증 테스트 완료" 명시용 데코레이터
        해당 데코레이터가 붙지 않은 "동작검증 테스트 미완료" 함수로 간주
    """
    return func



# @ensure_seconds_measured
def pk_mark_function_test_todo(func):
    """
        "추후 동작검증 테스트 필요" 명시용 데코레이터
    """
    return func


