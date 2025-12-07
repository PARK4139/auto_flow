def ensure_applications_killed_like_person(__file__):
    import logging
    import pyautogui
    import pygetwindow
    import time

    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
    from pk_internal_tools.pk_functions.get_current_console_title import get_current_console_title
    from pk_internal_tools.pk_functions.get_nx import get_nx

    # user protection code
    # logging.debug("WARNING: This script will attempt to close ALL open windows.")
    # logging.debug("You have 5 seconds to cancel by pressing Ctrl+C.")
    # try:
    #     for i in range(5, 0, -1):
    #         sys.stdout.write(f"Closing in {i} seconds... \r")
    #         sys.stdout.flush()
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     logging.debug("Operation cancelled by user.")
    #     return

    ensure_window_to_front(get_nx(__file__))
    current_terminal_console_title = get_current_console_title()
    ensure_window_to_front(current_terminal_console_title)

    all_windows = pygetwindow.getAllWindows()

    for window in all_windows:
        try:
            if not window.title:
                continue
            else:
                logging.warning(f"window.title={window.title}")

            if window.title == current_terminal_console_title:
                continue

            if window.isMinimized:
                window.restore()

            window.activate()
            time.sleep(0.2)

            active_window = pygetwindow.getActiveWindow()
            # 현재 터미널 창은 닫지 않도록 다시 한번 확인
            if window.title == current_terminal_console_title:
                logging.debug(f"Skipping current terminal window: {window.title}")
                continue

            if active_window and active_window._hWnd == window._hWnd:
                logging.warning(f"Attempting to close: {window.title}")
                # ensure_console_paused()
                pyautogui.hotkey('alt', 'f4')
                time.sleep(0.3)
                pyautogui.press('left')
                time.sleep(0.1)
                pyautogui.press('enter')
                time.sleep(0.5)
                time.sleep(0.5)  # 충분한 대기 시간
            else:
                logging.debug(f"Could not activate window: {window.title}. Skipping.")

        except pygetwindow.PyGetWindowException as e:
            logging.debug(f"Could not process window '{window.title}': {e}. It might have been closed already.")
        except Exception as e:
            logging.debug(f"An unexpected error occurred while processing window '{window.title}': {e}")

    logging.debug("All applications have been processed.")
