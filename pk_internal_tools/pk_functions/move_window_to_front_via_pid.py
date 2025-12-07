import logging


def move_window_to_front_via_pid(pid):
    import subprocess  # Added for PowerShell

    import win32con
    import win32gui
    import psutil
    import win32api  # Added for Alt-key trick
    import pywintypes  # Added for Alt-key trick

    logging.debug(f"Attempting to move window to front for PID: {pid}")
    if not str(pid).isdigit():
        logging.debug(f"PID is not a digit: {pid}")
        return
    pid = int(pid)
    try:
        process = psutil.Process(pid)
        logging.debug(f"Process found: {process.name()}")
        if not (process.is_running() and process.status() != psutil.STATUS_ZOMBIE):
            logging.debug(f"Process is not running or is a zombie: {pid}")
            return

        # --- Get HWND from PID using PowerShell (most reliable method) ---
        ps_get_hwnd_cmd = f"(Get-Process -Id {pid}).MainWindowHandle"
        hwnd_str = subprocess.run(["powershell", "-Command", ps_get_hwnd_cmd], capture_output=True, text=True, check=True).stdout.strip()

        if not hwnd_str or hwnd_str == "0":  # 0 means no main window handle
            logging.debug(f"No main window handle found for PID {pid} via PowerShell.")
            return

        hwnd = int(hwnd_str)
        logging.debug(f"Found HWND {hwnd} for PID {pid} via PowerShell.")
        # --- End Get HWND from PID using PowerShell ---

        # --- Bring window to front using pywin32 (robust method) ---
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Ensure it's not minimized

            # Use the "Alt key" trick to bypass focus restrictions
            win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)
            win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)

            win32gui.SetForegroundWindow(hwnd)
            logging.debug(f"SetForegroundWindow with Alt-key trick attempted for HWND {hwnd}.")
        except pywintypes.error:
            logging.warning(f"SetForegroundWindow with Alt-key trick failed for HWND {hwnd}. Falling back.")
            win32gui.BringWindowToTop(hwnd)
            win32gui.ShowWindow(hwnd, win32con.SW_SHOW)  # Ensure it's visible
        except Exception as e:
            logging.warning(f"Unexpected error during foreground attempt for HWND {hwnd}: {e}")
            win32gui.BringWindowToTop(hwnd)
            win32gui.ShowWindow(hwnd, win32con.SW_SHOW)

        win32gui.BringWindowToTop(hwnd)  # Redundant but harmless, ensures it's on top
        logging.debug(f"Successfully attempted to move window to front for PID {pid} (HWND {hwnd}).")
        # --- End Bring window to front using pywin32 ---

    except psutil.NoSuchProcess:
        logging.debug(f"Invalid PID: {pid} (NoSuchProcess)")
    except Exception as e:
        logging.error(f"An unknown error occurred: {e}")
        import traceback
        ensure_debug_loged_verbose(traceback)
