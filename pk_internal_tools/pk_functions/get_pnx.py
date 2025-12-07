




def get_pnx(pnx):
    """
    Path 객체 또는 문자열을 Path 객체로 반환합니다.
    
    Args:
        pnx: Path 객체 또는 문자열 경로
        
    Returns:
        Path: Path 객체
    """
    from pathlib import Path
    return Path(pnx)
