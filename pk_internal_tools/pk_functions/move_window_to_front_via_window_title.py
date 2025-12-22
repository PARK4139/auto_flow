import logging
import win32gui
import win32con
import traceback

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose

def move_window_to_front_via_window_title(window_title: str) -> bool:
    """
    지정된 정확한 창 제목을 가진 창을 찾아 전면으로 이동시킵니다.
    최소화된 창도 복원하고 전면으로 가져옵니다. 단 1회 시도합니다.

    Args:
        window_title (str): 전면으로 가져올 창의 정확한 제목.

    Returns:
        bool: 창이 성공적으로 전면으로 이동되었으면 True, 아니면 False.
    """
    logging.info(f"창 '{window_title}'을(를) 전면으로 이동 시도합니다 (1회).")
    
    try:
        hwnd_found = win32gui.FindWindow(None, window_title)
        if hwnd_found:
            # 창이 최소화되어 있는지 확인하고 복원합니다.
            if win32gui.IsIconic(hwnd_found):
                win32gui.ShowWindow(hwnd_found, win32con.SW_RESTORE)
            
            # 창을 전면으로 가져옵니다.
            win32gui.SetForegroundWindow(hwnd_found)
            win32gui.BringWindowToTop(hwnd_found)
            
            # 실제로 전면으로 왔는지 확인
            if win32gui.GetForegroundWindow() == hwnd_found:
                logging.info(f"창 '{window_title}'이(가) 성공적으로 전면으로 이동했습니다.")
                return True
            else:
                logging.warning(f"창 '{window_title}'이(가) 전면으로 이동했지만, 현재 전면 창은 아닙니다.")
                return False
        else:
            logging.warning(f"창 '{window_title}'을(를) 찾을 수 없습니다.")
            return False
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
        logging.error(f"창 '{window_title}'을(를) 전면으로 이동하는 중 오류 발생: {e}")
        return False
