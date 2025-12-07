def keyUp(key: str):
    import inspect
    import pyautogui
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    pyautogui.keyUp(key)
