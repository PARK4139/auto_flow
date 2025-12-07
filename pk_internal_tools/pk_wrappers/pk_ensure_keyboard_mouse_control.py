import tkinter as tk
from pynput import keyboard, mouse
import threading
import time

class KeyboardMouseController:
    def __init__(self):
        self.mouse_controller = mouse.Controller()
        self.backtick_pressed = False
        self.move_step = 1  # Default move step is 1 pixel
        self.mode_map = {'2': 10, '3': 100, '4': 1}

    def show_help_window(self):
        """단축키 도움말을 보여주는 GUI 창을 10초 동안 표시합니다."""
        help_text = textwrap.dedent("""
            ` (백틱) 키와 함께 사용하는 단축키:
            ------------------------------------
            - 이동:
                - ` + ↑, ↓, ←, → : 마우스 커서 이동

            - 이동 단위 변경:
                - ` + 2 : 10픽셀 단위로 변경
                - ` + 3 : 100픽셀 단위로 변경
                - ` + 4 : 1픽셀 단위로 변경 (기본값)

            - 클릭:
                - ` + Enter : 마우스 왼쪽 클릭
                - ` + Space : 마우스 오른쪽 클릭

            - 도움말:
                - ` + 1 : 이 도움말 창 다시 열기
            ------------------------------------
            이 창은 10초 후에 자동으로 닫힙니다.
            """)

        def create_window():
            root = tk.Tk()
            root.title("키보드 마우스 조작 단축키")
            root.attributes("-topmost", True) # 항상 위에 표시
            label = tk.Label(root, text=help_text, justify=tk.LEFT, padx=20, pady=20, font=("Malgun Gothic", 10))
            label.pack()
            
            # 10초 후 창 닫기
            root.after(10000, root.destroy)
            root.mainloop()

        # GUI는 별도 스레드에서 실행하여 키보드 리스너를 막지 않도록 함
        threading.Thread(target=create_window, daemon=True).start()

    def on_press(self, key):
        try:
            if key == keyboard.KeyCode.from_char('`'):
                self.backtick_pressed = True
                return

            if self.backtick_pressed:
                # 방향키로 마우스 이동
                if key in [keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right]:
                    x, y = 0, 0
                    if key == keyboard.Key.up:
                        y = -self.move_step
                    elif key == keyboard.Key.down:
                        y = self.move_step
                    elif key == keyboard.Key.left:
                        x = -self.move_step
                    elif key == keyboard.Key.right:
                        x = self.move_step
                    self.mouse_controller.move(x, y)
                
                # 문자 키 처리
                elif hasattr(key, 'char'):
                    # 모드 변경
                    if key.char in self.mode_map:
                        self.move_step = self.mode_map[key.char]
                        print(f"이동 단위가 {self.move_step}픽셀로 변경되었습니다.")
                    # 도움말 창
                    elif key.char == '1':
                        self.show_help_window()
                
                # 특수 키 처리 (클릭)
                elif key == keyboard.Key.enter:
                    self.mouse_controller.click(mouse.Button.left)
                    print("마우스 왼쪽 클릭")
                elif key == keyboard.Key.space:
                    self.mouse_controller.click(mouse.Button.right)
                    print("마우스 오른쪽 클릭")

        except Exception as e:
            print(f"오류 발생: {e}")

    def on_release(self, key):
        if key == keyboard.KeyCode.from_char('`'):
            self.backtick_pressed = False

    def start(self):
        print("키보드 마우스 제어 프로그램을 시작합니다.")
        print("` + 1 키를 눌러 언제든지 단축키를 확인할 수 있습니다.")
        self.show_help_window() # 시작 시 도움말 창 표시
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

if __name__ == '__main__':
    import textwrap
    controller = KeyboardMouseController()
    controller.start()
