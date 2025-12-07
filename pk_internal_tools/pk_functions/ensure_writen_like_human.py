





def ensure_writen_like_human(text_working: str, interval=0.04):  # interval 낮을 수록 빠름 # cmd.exe 를 admin 으로 열면 클립보드가 막혀있음.
    import logging
    import inspect

    import pyautogui
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    pyautogui.write(text_working, interval=interval)  # 한글 미지원.
    logging.debug(rf"{text_working}")
