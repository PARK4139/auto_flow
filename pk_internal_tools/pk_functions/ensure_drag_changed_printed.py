from pk_internal_tools.pk_functions.get_text_dragged import get_text_dragged
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def get_list_striped_element(working_list, mode='rstrip'):
    """Strip each line in the list based on the mode."""
    if mode == 'rstrip':
        return [line.rstrip() for line in working_list if line.strip()]
    elif mode == 'strip':
        return [line.strip() for line in working_list if line.strip()]
    return working_list


def ensure_drag_changed_printed ():
    from pynput import mouse

    class DragTracker:
        def __init__(self):
            self.is_left_pressed = False               # 현재 마우스 왼쪽 버튼이 눌렸는지
            self.has_moved_while_pressed = False       # 눌린 상태에서 마우스를 이동했는지
            self.start_listener()
            logging.debug("Tracking mouse drag events...")

        def start_listener(self):
            with mouse.Listener(
                on_click=self.on_click,
                on_move=self.on_move,
            ) as listener:
                listener.join()

        def on_click(self, x, y, button, pressed):
            if button == mouse.Button.left:
                if pressed:
                    self.is_left_pressed = True
                    self.has_moved_while_pressed = False  # 시작 시 초기화
                else:
                    if self.is_left_pressed and self.has_moved_while_pressed:
                        #  드래그 완료 시점
                        # dragged_text = get_txt_dragged()
                        dragged_text = get_text_dragged()
                        if dragged_text.strip():
                            lines = dragged_text.split("\n")
                            stripped_lines = get_list_striped_element(lines, mode='rstrip')
                            for line in stripped_lines:
                                logging.debug(                        f'''[dragged_text_layer] {line}  '''
                                )
                            print("" * 3)
                    self.is_left_pressed = False
                    self.has_moved_while_pressed = False

        def on_move(self, x, y):
            if self.is_left_pressed:
                self.has_moved_while_pressed = True

    DragTracker()
