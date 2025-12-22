def get_nx(pnx):
    """
    Path 객체 또는 문자열에서 파일명(확장자 포함)을 반환합니다.
    
    Args:
        pnx: Path 객체, 문자열 경로, 또는 경로 리스트
        
    Returns:
        str: 파일명 (확장자 포함)
    """
    from pathlib import Path

    if pnx is None:
        return ""
    
    # 리스트인 경우 첫 번째 요소 사용
    if isinstance(pnx, list):
        if len(pnx) > 0:
            pnx = pnx[0]
        else:
            return ""
    
    # Path 객체로 변환
    path = Path(pnx)
    return path.name