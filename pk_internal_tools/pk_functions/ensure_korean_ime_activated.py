import logging
import traceback
import win32api
import win32con
import win32gui
import win32process
from typing import Optional

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.ensure_pk_wrapper_starting_routine_done import ensure_pk_wrapper_starting_routine_done

# 한국어 IME의 HKL (Keyboard Layout Handle) 값
# 일반적으로 0x0412 또는 0xE0200412 가 사용됨.
# 0x0412는 한국어 기본 레이아웃, 0xE0200412는 MS-IME의 특정 버전을 나타낼 수 있음.
# 여기서는 일반적인 한국어 HKL을 사용합니다.
KOREAN_IME_HKL = 0x4120412  # 한국어 (대한민국) (Microsoft IME HKL)

def ensure_korean_ime_activated(hwnd: Optional[int] = None) -> bool:
    """
    현재 활성화된 창의 입력 언어가 한국어가 아니면 한국어로 강제 전환합니다.
    Args:
        hwnd (Optional[int]): IME 상태를 확인할 윈도우 핸들. None이면 현재 포커스된 윈도우를 사용합니다.
    Returns:
        bool: 한국어 IME가 활성화되었으면 True, 아니면 False.
    """


    func_n = get_caller_name()
    try:
        if hwnd is None:
            # 현재 포커스된 윈도우의 핸들을 가져옵니다.
            hwnd = win32gui.GetForegroundWindow()

        if hwnd == 0:
            logging.debug(f"{func_n}: No foreground window found.")
            return False

        # 현재 윈도우의 스레드 ID와 프로세스 ID를 가져옵니다.
        thread_id, process_id = win32process.GetWindowThreadProcessId(hwnd)

        # 현재 스레드의 키보드 레이아웃을 가져옵니다.
        current_hkl = win32api.GetKeyboardLayout(thread_id)
        logging.debug(f"{func_n}: Current HKL before switch attempt: {hex(current_hkl)}.")

        # 한국어 IME가 아니면 한국어로 전환
        if current_hkl != KOREAN_IME_HKL:
            logging.info(f"{func_n}: Detected non-Korean IME (current HKL: {hex(current_hkl)}). Attempting to switch to Korean IME (HKL: {hex(KOREAN_IME_HKL)}) for window {hwnd}.")

            try:
                # LoadKeyboardLayout을 통해 "00000412" (한국어)를 로드하고 활성화 시도.
                # KLF_ACTIVATE 플래그를 사용하면 로드와 동시에 활성화됩니다.
                loaded_hkl = win32api.LoadKeyboardLayout("00000412", win32con.KLF_ACTIVATE)
                logging.info(f"{func_n}: LoadKeyboardLayout returned HKL {hex(loaded_hkl)}.")

                # 추가: 로드된 HKL을 현재 윈도우에 강제로 적용
                win32api.SendMessage(hwnd, win32con.WM_INPUTLANGCHANGEREQUEST, 0, loaded_hkl)

                # LoadKeyboardLayout이 성공적으로 한국어 HKL을 로드하고 활성화했는지 확인
                # 즉시 GetKeyboardLayout으로 현재 스레드의 HKL을 다시 확인하여 실제 적용 여부를 판단합니다.
                current_hkl_after_load = win32api.GetKeyboardLayout(thread_id)
                logging.debug(f"{func_n}: Current HKL after LoadKeyboardLayout: {hex(current_hkl_after_load)}.")

                if current_hkl_after_load == KOREAN_IME_HKL:
                    logging.info(f"{func_n}: Successfully loaded and activated Korean IME for window {hwnd}.")
                    return True
                else:
                    logging.warning(f"{func_n}: Korean IME is still not active after LoadKeyboardLayout. (Current HKL: {hex(current_hkl_after_load)}, Expected: {hex(KOREAN_IME_HKL)}).")
                    return False
            except Exception as load_e:
                logging.error(f"{func_n}: Error during LoadKeyboardLayout: {load_e}", exc_info=True)
                return False
        else:
            logging.debug(f"{func_n}: Korean IME is already active (HKL: {hex(current_hkl)}) for window {hwnd}.")
            return True
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
        logging.error(f"{func_n}: Error checking/switching IME: {e}", exc_info=True)
        return False

