

def get_pnx_unix_style(pnx):
    """
    경로를 Unix 스타일로 변환하는 함수
    - Path 객체와 문자열 모두 처리 가능
    
    Args:
        pnx: Path 객체 또는 문자열 경로
        
    Returns:
        str: Unix 스타일 경로 문자열
    """
    from pathlib import Path
    
    # Path 객체인 경우 문자열로 변환
    if isinstance(pnx, Path):
        path_str = str(pnx)
    else:
        path_str = str(pnx)
    
    # Windows 백슬래시를 Unix 슬래시로 변환
    path_str = path_str.replace("\\", "/")
    return path_str.strip()
