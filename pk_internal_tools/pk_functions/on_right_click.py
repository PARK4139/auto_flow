

import logging


def on_right_click(x, y, button, pressed):
    from pynput import mouse
    if pressed and button == mouse.Button.right:
        click_detected = True  # 클릭 감지 상태 업데이트
        logging.debug("마우스 우클릭 감지됨!")
        return 0  # 마우스 왼쪽 클릭 감지되면 Listener 종료
