"""
get_pk_program_language는 더 이상 사용되지 않습니다.
get_pk_program_language를 사용하세요.

이 파일은 하위 호환성을 위해 유지되며, get_pk_program_language로 리다이렉트합니다.
"""

from pk_internal_tools.pk_functions.get_pk_program_language import get_pk_program_language


def get_pk_program_language():
    """
    하위 호환성을 위한 래퍼 함수
    
    Deprecated: get_pk_program_language를 직접 사용하세요.
    """
    return get_pk_program_language()
