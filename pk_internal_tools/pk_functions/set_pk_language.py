"""
pk_system 언어 변경 함수
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
        return "english"


def _map_full_name_to_language_code(lang_full: str) -> str:
    """
    전체 언어 이름을 코드로 매핑
    
    Args:
        lang_full: "korean" 또는 "english"
        
    Returns:
        "kr" 또는 "en"
    """
    lang_lower = lang_full.lower() if lang_full else ""
    
    if lang_lower == "korean":
        return "kr"
    elif lang_lower == "english":
        return "en"
    else:
        return "en"


@ensure_seconds_measured
def set_pk_language(language: str = None):
    """
    pk_system 언어를 변경하고 PkTexts에 설정합니다.
    
    Args:
        language: "kr", "en", "korean", "english" 중 하나. None이면 사용자에게 선택 요청
        
    Returns:
        str: 설정된 언어 ("korean" 또는 "english")
    """
    import logging
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_functions.get_file_id import get_file_id
    from pk_internal_tools.pk_functions.get_values_from_historical_file_routine import get_values_from_historical_file_routine
    
    try:
        func_n = get_caller_name()
        db = PkSqlite3()
        key_name = "pk_language"
        
        # 언어 선택
        if language is None:
            # 사용자에게 선택 요청
            selected_code = get_values_from_historical_file_routine(
                file_id=get_file_id(key_name, func_n),
                key_hint=f"{key_name}=",
                options=["kr", "en"],
                editable=True
            )
        else:
            # 제공된 언어를 코드로 변환
            lang_lower = language.lower()
            if lang_lower in ("kr", "korean", "ko"):
                selected_code = "kr"
            elif lang_lower in ("en", "english", "eng"):
                selected_code = "en"
            else:
                # 이미 코드일 수 있음
                selected_code = language
        
        # DB에 저장
        db.set_values(db_id=db.get_db_id(key_name, func_n), values=selected_code)
        
        # PkTexts에 설정
        lang_full = _map_language_code_to_full_name(selected_code)
        PkTexts.set_lang(lang_full)
        
        logging.debug(f"pk_system language changed to: {lang_full} (code: {selected_code})")
        return lang_full
        
    except Exception as e:
        logging.warning(f"언어 변경 실패: {e}")
        PkTexts.set_lang("english")
        return "english"

