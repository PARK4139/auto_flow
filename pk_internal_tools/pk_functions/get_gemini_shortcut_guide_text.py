def get_gemini_shortcut_guide_text():
    """
    GEMINI SHORTCUT 가이드 텍스트를 파일에서 읽어옵니다.
    
    Returns:
        str: GEMINI SHORTCUT 가이드 텍스트
    """
    import textwrap
    from pathlib import Path
    from pk_internal_tools.pk_functions.get_str_from_f import get_str_from_f
    
    # 텍스트 파일 경로
    guide_file = Path(__file__).parent.parent.parent / "pk_external_tools" / "gemini_shortcut_guide.txt"
    
    # 파일에서 텍스트 읽기
    guide_text = get_str_from_f(f=guide_file)
    
    # textwrap.dedent 적용
    if guide_text:
        guide_text = textwrap.dedent(guide_text)
    
    return guide_text

