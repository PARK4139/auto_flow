def ensure_str_writen_to_f(text: str, f, mode: str = "a", encoding=None) -> None:
    from enum import Enum

    from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
    from pk_internal_tools.pk_objects.pk_encodings import PkEncoding

    encoding: Enum
    encoding = encoding or PkEncoding.UTF8  # None 또는 False 인 경우 Encoding.UTF8를 할당 (**"단축 평가(short-circuit evaluation)를 활용한 기본값 할당"**)
    ensure_pnx_made(f, mode='f')
    f = str(f)
    with open(file=f, mode=mode, encoding=encoding.value) as file:
        file.write(text)
