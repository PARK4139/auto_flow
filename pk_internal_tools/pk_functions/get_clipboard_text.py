def get_clipboard_text():
    return get_clipboard_text_v2()

def get_clipboard_text_v2():
    try:
        import logging
        import logging
        import win32clipboard
        import win32con

        win32clipboard.OpenClipboard()
        try:
            if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
                data = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
                return data if data is not None else ""
            else:
                return ""  # no text on clipboard (could be image/file list, etc.)
        finally:
            win32clipboard.CloseClipboard()
    except Exception as e:
        logging.warning(f"클립보드 읽기 실패: {e}")
        return None



def get_clipboard_text_v1():
    try:
        import subprocess
        result = subprocess.run(
            ["powershell", "-command", "Get-Clipboard"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"[ERROR] 클립보드 읽기 실패: {e}"


