from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_window_resized_and_positioned_right_half():
    """
    Resizes the active window to occupy the right half of the primary monitor.

    This function is designed to be deterministic, avoiding the stateful behavior
    of the 'Win + Right' keyboard shortcut. It uses pygetwindow and screeninfo
    to calculate the exact position and size.
    """
    import logging
    import pygetwindow
    import screeninfo
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept

    try:
        # 1. Get the active window
        window = pygetwindow.getActiveWindow()
        if not window:
            logging.warning("No active window found to resize.")
            return

        # 2. If the window is maximized or minimized, restore it
        if window.isMaximized or window.isMinimized:
            window.restore()
            ensure_slept(0.1)  # Give time for the window to restore

        # 3. Get the primary monitor's geometry
        try:
            primary_monitor = [m for m in screeninfo.get_monitors() if m.is_primary][0]
        except IndexError:
            logging.error("Could not find the primary monitor.")
            return

        # 4. Calculate the target geometry for the right half
        target_width = primary_monitor.width // 2
        target_height = primary_monitor.height
        target_x = primary_monitor.x + (primary_monitor.width // 2) # Adjusted for right half
        target_y = primary_monitor.y

        # 5. Move and resize the window
        # For reliability, perform these actions separately.
        window.resizeTo(target_width, target_height)
        window.moveTo(target_x, target_y)

        logging.info(f"Window '{window.title}' was resized and moved to the right half of the primary screen.")

    except pygetwindow.PyGetWindowException as e:
        logging.error(f"An error occurred while managing the window: {e}")
    except Exception as e:
        import traceback
        logging.error(f"An unexpected error occurred: {e}\n{traceback.format_exc()}")
