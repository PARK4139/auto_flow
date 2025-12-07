import logging
import webbrowser
from typing import Optional

from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken


def ensure_home_assistant_login_guided(ha_login_url: str) -> Optional[str]:
    """
    Host PC에서 Home Assistant 로그인/토큰 발급 과정을 GUI로 안내하고,
    사용자가 입력한 토큰 문자열을 반환합니다.
    GUI 사용이 불가능하면 None을 반환합니다.
    """

    try:
        import tkinter as tk
        from tkinter import ttk
    except Exception as gui_error:  # GUI 사용 불가
        logging.warning("GUI 안내를 사용할 수 없어 기본 모드로 진행합니다: %s", gui_error)
        try:
            webbrowser.open(ha_login_url, new=2)
        except Exception as open_error:
            logging.warning("브라우저 자동 실행 실패: %s", open_error)
        return None


    logging.info("Home Assistant 로그인 안내 GUI를 표시합니다.")
    try:
        webbrowser.open(ha_login_url, new=2)
    except Exception as open_error:
        logging.warning("브라우저 자동 실행 실패: %s", open_error)

    token_holder = {"value": None}
    root = tk.Tk()
    root.title("Home Assistant 로그인 안내")
    root.geometry("1520x1240")
    root.resizable(False, False)

    def bring_window_front():
        # n. prefer existing ensure_window_to_front helper (Windows)
        try:
            from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front

            if ensure_window_to_front(window_title_seg=root.title()):
                return
        except Exception as front_error:
            logging.debug("ensure_window_to_front 사용 실패: %s", front_error)

        # 2) generic Tk fallback
        try:
            root.lift()
            root.attributes("-topmost", True)
            root.after(1000, lambda: root.attributes("-topmost", False))
        except Exception as tk_front_error:
            logging.debug("Tk front fallback 실패: %s", tk_front_error)

    root.after(50, bring_window_front)

    main_frame = ttk.Frame(root, padding=16)
    main_frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(
        main_frame,
        text="Home Assistant Long-Lived Access Token 생성 절차",
        font=("Segoe UI", 12, "bold"),
    ).pack(anchor=tk.W, pady=(0, 8))

    instructions = [
        "1. 기본 브라우저가 자동으로 열립니다. 열리지 않으면 아래 버튼으로 수동으로 열어주세요.",
        "2. Home Assistant 초기 설정 화면에서 '나만의 스마트 홈 만들기' 버튼을 클릭합니다.",
        "3. Home Assistant 로그인 후 왼쪽 아래 프로필(사용자 이름)을 클릭합니다.",
        "4. 화면 맨 아래의 Long-Lived Access Tokens 섹션에서 CREATE TOKEN을 클릭합니다.",
        "5. 토큰 이름(예: pk_system)을 입력하고 생성 버튼을 누릅니다.",
        "6. 토큰 문자열이 한 번만 표시됩니다. 아래 입력창에 복사/붙여넣기 한 뒤 [토큰 저장] 버튼을 눌러주세요.",
        "7. 토큰은 안전한 곳에 보관하세요. 창을 닫으면 다시 확인할 수 없습니다.",
    ]

    # 각 줄을 1줄 단위로 ensure_spoken 호출
    # for instruction_line in instructions:
    #     ensure_spoken(instruction_line)

    text_frame = ttk.Frame(main_frame)
    text_frame.pack(fill=tk.X, pady=(0, 12))

    text_widget = tk.Text(
        text_frame,
        height=12,
        wrap=tk.WORD,
        relief=tk.GROOVE,
        borderwidth=2,
        font=("Segoe UI", 10),
    )
    text_widget.pack(fill=tk.X, expand=True)
    text_widget.insert(tk.END, "\n".join(instructions))
    text_widget.configure(state=tk.DISABLED)

    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=tk.X, pady=(0, 12))

    def open_url():
        try:
            webbrowser.open(ha_login_url, new=2)
        except Exception as open_error:
            logging.warning("브라우저 열기 실패: %s", open_error)

    def copy_url():
        root.clipboard_clear()
        root.clipboard_append(ha_login_url)
        root.update()  # clipboard 유지

    ttk.Button(button_frame, text="브라우저로 열기", command=open_url).pack(side=tk.LEFT, padx=(0, 8))
    ttk.Button(button_frame, text="URL 복사", command=copy_url).pack(side=tk.LEFT)

    ttk.Label(main_frame, text="생성된 Home Assistant 토큰을 아래에 입력하세요:", font=("Segoe UI", 10, "bold")).pack(
        anchor=tk.W
    )
    token_entry = ttk.Entry(main_frame, show="", width=60)
    token_entry.pack(fill=tk.X, pady=(4, 12))

    action_frame = ttk.Frame(main_frame)
    action_frame.pack(fill=tk.X, pady=(0, 8))

    def submit_and_close():
        value = token_entry.get().strip()
        if value:
            token_holder["value"] = value
        root.destroy()

    def cancel_and_close():
        token_holder["value"] = None
        root.destroy()

    ttk.Button(action_frame, text="토큰 저장", command=submit_and_close).pack(side=tk.LEFT, padx=(0, 8))
    ttk.Button(action_frame, text="나중에 입력", command=cancel_and_close).pack(side=tk.LEFT)

    ttk.Label(
        main_frame,
        text="※ 창을 닫으면 '나중에 입력'으로 간주됩니다.",
        font=("Segoe UI", 9),
        foreground="#666666",
    ).pack(anchor=tk.W)

    root.protocol("WM_DELETE_WINDOW", cancel_and_close)
    root.mainloop()

    return token_holder["value"]

