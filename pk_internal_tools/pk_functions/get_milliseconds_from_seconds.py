"""
초를 밀리초로 변환하는 함수

초 값을 밀리초 단위로 변환하여 반환합니다.
"""


def get_milliseconds_from_seconds(seconds: float) -> float:
    """
    초를 밀리초로 변환합니다.
    
    Args:
        seconds: 변환할 초 값
        
    Returns:
        float: 밀리초 단위로 변환된 값
        
    Example:
        >>> get_milliseconds_from_seconds(1.5)
        1500.0
        >>> get_milliseconds_from_seconds(0.5)
        500.0
    """
    return seconds * 1000.0
