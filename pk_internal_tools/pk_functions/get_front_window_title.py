def get_front_window_title():
    import pygetwindow
    try:
        active_window = pygetwindow.getActiveWindow()
        if active_window:
            return active_window.title
        else:
            return None  # 활성화된 창이 없다면 None 반환
    except Exception as e:
        return f"Error: {str(e)}"
