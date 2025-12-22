import logging
import subprocess
import sys

def ensure_function_executed_in_new_process(module_path: str, function_name: str, keep_open: bool = False):
    """
    지정된 함수를 새로운 콘솔의 별도 파이썬 프로세스에서 실행합니다.

    :param module_path: 함수가 포함된 모듈의 전체 경로 (e.g., "pk_internal_tools.pk_functions.my_module")
    :param function_name: 실행할 함수의 이름
    :param keep_open: True일 경우, 실행 후에도 콘솔 창을 열어 둡니다.
    """
    command_string = f"from {module_path} import {function_name}; {function_name}()"
    
    if keep_open and sys.platform == "win32":
        command = ["cmd", "/k", sys.executable, "-c", command_string]
    else:
        command = [sys.executable, "-c", command_string]

    try:
        subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
        logging.info(f"새 콘솔에서 '{function_name}' 함수를 시작했습니다.")
    except Exception as e:
        logging.error(f"'{function_name}' 함수를 새 프로세스에서 시작 중 오류 발생: {e}")
