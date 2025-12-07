

def get_value_splited_integer_part_and_decimal_part_from_(value):  # 큰단위로 단위변환 시 숫자는 작아지니 숫자가 작아지도록 약속된 숫자를 곱하면 된다.
    import math
    decimal_part, integer_part = math.modf(value)
    decimal_part = abs(decimal_part)  # 음수 부호 remove
    return [integer_part, decimal_part]
