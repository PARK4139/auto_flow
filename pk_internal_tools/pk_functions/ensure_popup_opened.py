def ensure_popup_opened(message: str, timeout: int = 20) -> bool:
    """
    GUI 팝업을 화면에 출력하고 사용자의 YES/NO 선택을 받습니다.
    지정된 시간 내에 응답이 없으면 자동으로 닫히고 False를 반환합니다.

    Args:
        message (str): 팝업에 표시할 메시지.
        timeout (int): 팝업이 자동으로 닫히기까지의 시간 (초). 기본값은 20초.

    Returns:
        bool: 사용자가 YES를 선택하면 True, NO를 선택하면 False.
              타임아웃되거나 팝업이 강제로 닫히면 False.
    """
    # lazy import로 순환 import 문제 해결
    try:
        import tkinter as tk
        from tkinter import ttk
    except ImportError:
        print("tkinter 모듈을 찾을 수 없습니다. GUI 팝업을 표시할 수 없습니다.")
        return False

    root = tk.Tk()
    root.withdraw()  # 메인 윈도우를 숨깁니다.

    # 팝업 윈도우 생성
    popup = tk.Toplevel(root)
    popup.title("확인")
    popup.transient(root)  # 부모 윈도우에 종속
    popup.grab_set()  # 팝업이 최상위에 있도록 설정
    popup.resizable(False, False)

    # 결과 저장 변수
    result = False
    user_responded = False

    def on_yes():
        nonlocal result, user_responded
        result = True
        user_responded = True
        popup.destroy()

    def on_no():
        nonlocal result, user_responded
        result = False
        user_responded = True
        popup.destroy()

    def on_timeout():
        nonlocal user_responded
        if not user_responded:
            user_responded = True # Prevent further actions if already timed out
            popup.destroy()

    # 메시지 라벨
    label = ttk.Label(popup, text=message, wraplength=300, justify="center")
    label.pack(padx=20, pady=20)

    # 버튼 프레임
    button_frame = ttk.Frame(popup)
    button_frame.pack(pady=10)

    yes_button = ttk.Button(button_frame, text="YES", command=on_yes)
    yes_button.pack(side="left", padx=5)

    no_button = ttk.Button(button_frame, text="NO", command=on_no)
    no_button.pack(side="right", padx=5)

    # 윈도우 중앙 정렬
    popup.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() // 2) - (popup.winfo_width() // 2)
    y = root.winfo_y() + (root.winfo_height() // 2) - (popup.winfo_height() // 2)
    popup.geometry(f" +{x}+{y}")

    # 타임아웃 설정 (밀리초 단위)
    popup.after(timeout * 1000, on_timeout)

    # 팝업 윈도우가 닫힐 때까지 대기
    root.wait_window(popup)

    return result


if __name__ == "__main__":
    # 예시 사용법
    print("20초 타임아웃 팝업 테스트 (응답 없으면 False):")
    result_timeout = ensure_popup_opened("20초 안에 응답해주세요. (타임아웃 테스트)", timeout=20)
    if result_timeout:
        print("사용자가 YES를 선택했습니다.")
    else:
        print("사용자가 NO를 선택했거나 타임아웃되었습니다.")

    print("5초 타임아웃 팝업 테스트 (응답 없으면 False):")
    result_short_timeout = ensure_popup_opened("5초 안에 응답해주세요. (짧은 타임아웃 테스트)", timeout=5)
    if result_short_timeout:
        print("사용자가 YES를 선택했습니다.")
    else:
        print("사용자가 NO를 선택했거나 타임아웃되었습니다.")

    print("일반 팝업 테스트 (타임아웃 없음):")
    result_normal = ensure_popup_opened("작업을 계속하시겠습니까? (일반 테스트)", timeout=0) # timeout=0은 타임아웃 기능을 비활성화
    if result_normal:
        print("사용자가 YES를 선택했습니다.")
    else:
        print("사용자가 NO를 선택했습니다.")
