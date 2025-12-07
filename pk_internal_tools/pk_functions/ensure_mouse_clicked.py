"""
좌표 기반 마우스 클릭 함수
"""

import logging

import pyautogui

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_mouse_clicked(x: int, y: int, button='left', clicks=1, interval=0.0, duration=0.0, restore_origin_location=False):
    """
    지정된 좌표에서 마우스 클릭을 수행합니다.

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
        # 현재 마우스 위치 저장
        current_x, current_y = pyautogui.position()

        # 지정된 좌표로 마우스 이동 및 클릭
        pyautogui.moveTo(x, y, duration=duration)
        pyautogui.click(button=button, clicks=clicks, interval=interval)

        # 원래 위치로 마우스 복원
        if restore_origin_location:
            pyautogui.moveTo(current_x, current_y, duration=0.1)

        logging.debug(f"좌표 ({x}, {y})에서 {button} 버튼 클릭 완료")
        return True

    except Exception as e:
        logging.error(f"좌표 ({x}, {y})에서 클릭 실패: {e}")
        return False


@ensure_seconds_measured
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
