import textwrap

def compare_prices(A: dict, B: dict) -> str:
    """
    두 개의 값(value)을 비교하여, 어느 쪽이 얼마나 작은지 백분율로 계산하고 결과를 문자열로 반환합니다.

    Args:
        A (dict): 첫 번째 아이템. 예: {'name': '다이소 지퍼팩', 'value': 0.0057}
        B (dict): 두 번째 아이템. 예: {'name': 'a2z 지퍼팩', 'value': 0.01435}

    Returns:
        str: 비교 결과 문자열.
    """
    try:
        name_a = A['name']
        value_a = A['value']

        name_b = B['name']
        value_b = B['value']

        if value_a < value_b:
            smaller_name = name_a
            larger_name = name_b
            percentage_diff = (1 - (value_a / value_b)) * 100
        elif value_b < value_a:
            smaller_name = name_b
            larger_name = name_a
            percentage_diff = (1 - (value_b / value_a)) * 100
        else:
            return f"# 비교결과\n두 값 '{name_a}'과(와) '{name_b}'은(는) 동일합니다."

        output = f"""# 비교결과
{smaller_name} 가 {larger_name} 보다 약 {percentage_diff:.2f}% 작습니다."""

        return textwrap.dedent(output).strip()

    except (KeyError, TypeError, ValueError, ZeroDivisionError) as e:
        return f"값 비교 중 오류가 발생했습니다. 입력 형식을 확인해주세요. ({'name': str, 'value': float}}) - 오류: {e}"
