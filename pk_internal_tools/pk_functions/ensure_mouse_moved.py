from pynput import mouse
import time
import logging

def ensure_mouse_moved(x: int, y: int, duration: float = 1.0):
    """
    마우스 커서를 지정된 좌표로 이동시킵니다.
    Args:
        x (int): 이동할 X 좌표.
        y (int): 이동할 Y 좌표.
        duration (float): 이동에 걸릴 시간 (초). 기본값은 1.0초입니다.
    """
    logging.debug(f"마우스 커서를 ({x}, {y})로 {duration}초 동안 이동합니다.")
    controller = mouse.Controller()
    start_x, start_y = controller.position
    
    steps = int(duration * 50) # 50 steps per second for smooth movement
    if steps == 0:
        steps = 1

    for i in range(steps + 1):
        t = i / steps
        current_x = int(start_x + (x - start_x) * t)
        current_y = int(start_y + (y - start_y) * t)
        controller.position = (current_x, current_y)
        time.sleep(duration / steps)
    
    logging.debug(f"마우스 커서 이동 완료: ({x}, {y})")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.debug("마우스 이동 테스트 시작 (5초 후 마우스가 이동합니다)... ")
    time.sleep(5)
    ensure_mouse_moved(500, 500, duration=2) # Move to 500, 500 over 2 seconds
    logging.debug("마우스 이동 테스트 완료.")