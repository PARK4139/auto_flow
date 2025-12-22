def open_mouse_info():
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    # pyautogui.mouseInfo()
