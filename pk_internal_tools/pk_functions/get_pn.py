

def get_pn(pnx):
    """
    Path 객체 또는 문자열에서 디렉토리 경로 + 파일명(확장자 제외)을 반환합니다.
    
    Args:
        pnx: Path 객체 또는 문자열 경로
        
    Returns:
        Path: 부모 디렉토리 / 파일명(확장자 제외) 경로
    """
    from pathlib import Path
    path = Path(pnx)
    return path.parent / path.stem
