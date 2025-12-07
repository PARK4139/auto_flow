

def get_pnx_windows_style(pnx) -> str:
    """
    경로를 Windows 스타일로 변환하는 함수
    - 문자열과 Path 객체 모두 처리 가능
    """
    import re
    from pathlib import Path
    
    # Path 객체인 경우 문자열로 변환
    if isinstance(pnx, Path):
        path = str(pnx)
    else:
        path = str(pnx)
    
    path = path.replace('//', '/')
    path = re.sub(
        r'^/mnt/([A-Za-z])/',
        lambda m: f"{m.group(1).upper()}:/",
        path
    )
    return path.replace('/', '\\')
