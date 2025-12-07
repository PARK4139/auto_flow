"""
실행 후 클릭까지의 시간을 밀리초로 측정하는 함수

함수 실행 시점부터 마우스 클릭이 발생할 때까지의 경과 시간을
밀리초 단위로 반환합니다.
"""

import logging
import time
from typing import Optional


def ensure_milliseconds_until_click_measured(
    button: str = "left",
    timeout: Optional[float] = None,
) -> Optional[float]:
    """
    실행 후 클릭까지의 시간을 밀리초로 측정하여 반환합니다.

    함수 실행 시점부터 마우스 클릭이 발생할 때까지의 경과 시간을
    밀리초 단위로 반환합니다.

    Args:
        button: 감지할 마우스 버튼 ("left", "right", "middle"). 기본값: "left"
        timeout: 최대 대기 시간(초). None이면 무제한 대기. 기본값: None

    Returns:
        float: 클릭까지 경과한 시간(밀리초). 타임아웃 또는 오류 발생 시 None

    Example:
        >>> elapsed_ms = ensure_milliseconds_until_click_measured()
        >>> if elapsed_ms is not None:
        ...     print(f"클릭까지 {elapsed_ms:.2f}ms 경과")
    """
    from pynput import mouse
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_functions.get_easy_speakable_text import get_easy_speakable_text

    start_time = time.perf_counter()
    clicked = False
    elapsed_milliseconds: Optional[float] = None

    def on_click(x, y, button_clicked, pressed):
        nonlocal clicked, elapsed_milliseconds

        if not pressed:
            return

        # 버튼 타입 확인
        button_matched = False
        if button == "left" and button_clicked == mouse.Button.left:
            button_matched = True
        elif button == "right" and button_clicked == mouse.Button.right:
            button_matched = True
        elif button == "middle" and button_clicked == mouse.Button.middle:
            button_matched = True

        if button_matched:
            end_time = time.perf_counter()
            elapsed_seconds = end_time - start_time
            elapsed_milliseconds = elapsed_seconds * 1000
            clicked = True
            logging.debug(f"마우스 {button} 클릭 감지: ({x}, {y}). 경과 시간: {elapsed_milliseconds:.2f}ms")
            ensure_spoken(get_easy_speakable_text(f"마우스 {button} 클릭 감지: ({x}, {y}). 경과 시간: {elapsed_milliseconds:.2f}ms"))
            return False  # Stop listener

    try:
        logging.debug(f"클릭 시간 측정 시작 (버튼: {button}, 타임아웃: {timeout}초)")
        ensure_spoken(get_easy_speakable_text(f"클릭 시간 측정 시작 (버튼: {button}, 타임아웃: {timeout}초)"))

        with mouse.Listener(on_click=on_click) as listener:
            if timeout is not None:
                # 타임아웃이 있는 경우
                listener.join(timeout=timeout)
                if not clicked:
                    logging.debug(f"타임아웃 발생: {timeout}초 내에 클릭이 감지되지 않았습니다.")
                    ensure_spoken(get_easy_speakable_text(f"타임아웃 발생: {timeout}초 내에 클릭이 감지되지 않았습니다."))
                    return None
            else:
                # 타임아웃이 없는 경우 (무제한 대기)
                listener.join()

        if clicked and elapsed_milliseconds is not None:
            logging.debug(f"측정 완료: {elapsed_milliseconds:.2f}ms")
            ensure_spoken(get_easy_speakable_text(f"측정 완료: {elapsed_milliseconds:.2f}ms"))
            return elapsed_milliseconds
        else:
            logging.warning("클릭이 감지되지 않았습니다.")
            return None
            
    except Exception as e:
        logging.error(f"클릭 시간 측정 중 오류 발생: {e}", exc_info=True)
        return None

