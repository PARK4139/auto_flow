

def get_cmd_to_autorun():
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Command Processor") as key:
            value, _ = winreg.QueryValueEx(key, "Autorun")
            return value
    except FileNotFoundError:
        return None
