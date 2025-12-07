"""단위 변환 함수들."""


def get_inch_from_cm(centimeter: float) -> float:
    """센티미터를 인치로 변환합니다.

    Args:
        centimeter: 센티미터 단위의 값입니다.

    Returns:
        인치로 변환된 값입니다.
    """
    return centimeter / 2.54


def get_cm_from_inch(inch: float) -> float:
    """인치를 센티미터로 변환합니다.

    Args:
        inch: 인치 단위의 값입니다.

    Returns:
        센티미터로 변환된 값입니다.
    """
    return inch * 2.54
