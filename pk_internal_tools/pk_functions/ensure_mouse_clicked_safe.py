import traceback
from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose

def ensure_mouse_clicked_safe(x: int, y: int, button='left', clicks=1, interval=0.0, duration=0.0):
    """
    안전한 좌표 기반 마우스 클릭 함수 (화면 경계 확인)
    
    Args:
        x (int): 클릭할 X 좌표
        y (int): 클릭할 Y 좌표
        button (str): 클릭할 마우스 버튼 ('left', 'right', 'middle')
        clicks (int): 클릭 횟수
        interval (float): 연속 클릭 간의 간격 (초)
        duration (float): 마우스 이동 시간 (초)
    
    Returns:
        bool: 클릭 성공 여부
    """
    try:
        # 화면 크기 확인
        screen_width, screen_height = pyautogui.size()

        # 좌표가 화면 범위 내에 있는지 확인
        if x < 0 or x >= screen_width or y < 0 or y >= screen_height:
            logging.warning(f"좌표 ({x}, {y})가 화면 범위를 벗어남. 화면 크기: {screen_width}x{screen_height}")
            return False

        return ensure_mouse_clicked(x, y, button, clicks, interval, duration)

    except Exception as e:
        logging.error(f"안전한 클릭 실행 중 오류: {e}")
        return False