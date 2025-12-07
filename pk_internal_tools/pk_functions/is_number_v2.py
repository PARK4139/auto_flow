import speech_recognition as sr
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style


def is_number_v2(prompt: str):
    try:
        float(prompt)  # 숫자 형태로 변환을 시도
        return 1
    except ValueError:
        return 0
