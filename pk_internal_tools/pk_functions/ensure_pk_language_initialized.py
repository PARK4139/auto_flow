"""
pk_system 언어 초기화 함수
circular import를 방지하기 위해 별도 함수로 분리
"""
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


def _map_language_code_to_full_name(lang_code: str) -> str:
    """
    언어 코드를 전체 이름으로 매핑
    
    Args:
        lang_code: "kr", "en", "korean", "english" 중 하나
        
    Returns:
        "korean" 또는 "english"
    """
    lang_lower = lang_code.lower() if lang_code else ""
    
    if lang_lower in ("kr", "korean", "ko"):
        return "korean"
    elif lang_lower in ("en", "english", "eng"):
        return "english"
    else:
        # 기본값
        return "english"


@ensure_seconds_measured
def ensure_pk_language_initialized():
    """
    pk_system 언어를 초기화하고 PkTexts에 설정합니다.
    첫 실행 시 언어를 선택하도록 안내합니다.
    """
    import logging
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    from pk_internal_tools.pk_functions.get_pk_language import get_pk_language
    
    try:
        lang_code = get_pk_language()
        lang_full = _map_language_code_to_full_name(lang_code)
        PkTexts.set_lang(lang_full)
        logging.debug(f"pk_system language initialized: {lang_full} (from code: {lang_code})")
    except Exception as e:
        logging.warning(f"언어 초기화 실패, 기본값(english) 사용: {e}")
        PkTexts.set_lang("english")







