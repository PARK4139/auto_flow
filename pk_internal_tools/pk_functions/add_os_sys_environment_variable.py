import logging


def add_os_sys_environment_variable(environment_variable_name: str, environment_variable_value: str):
    import inspect
    import sys

    """시스템 환경변수 path 업데이트"""
    # lazy import로 순환 import 문제 해결
    try:
        from pk_internal_tools.pk_functions.ensure_get_caller_name import get_caller_name
    except ImportError:
        # fallback: Define a dummy function or raise an error if it's critical
        def get_caller_name():
            raise RuntimeError("get_caller_name could not be imported.")
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    logging.debug("테스트가 필요한 함수를 적용하였습니다")
    logging.debug("기대한 결과가 나오지 않을 수 있습니다")
    logging.debug("업데이트 전 시스템 환경변수")
    for i in sys.path:
        logging.debug(i)
    sys.path.insert(0, environment_variable_value)
    sys.path.append(environment_variable_value)
    logging.debug("업데이트 전 시스템 환경변수")
    for i in sys.path:
        logging.debug(i)
