def get_current_mouse_abs_info():
    import inspect
    import pyautogui
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    coordination = pyautogui.position()
    coordination = str(coordination)
    coordination = coordination.replace("Point(x=", "")
    coordination = coordination.replace("y=", "")
    coordination = coordination.replace(")", "")
    coordination = coordination.replace(" ", "")
    x = coordination.split(",")[0]
    y = coordination.split(",")[1]
    return x, y
