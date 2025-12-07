def ensure_window_moved_to_front_like_person():
    import subprocess
    import logging
    import time
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    try:
        from pk_internal_tools.pk_functions.ensure_get_current_console_title import get_current_console_title
    except ImportError:
        logging.warning("Could not import get_current_console_title. Please ensure it is available.")

    func_n = get_caller_name()
    get_titles_cmd = 'powershell -Command "Get-Process | Where-Object { $_.MainWindowTitle -ne \'\' } | Select-Object -ExpandProperty MainWindowTitle"'

    # Setup an extensible list of window titles to exclude
    exclusion_list = []
    try:
        current_console_title = get_current_console_title()
        if current_console_title:
            exclusion_list.append(current_console_title)
    except Exception as e:
        logging.warning(f"Could not get current console title to exclude it: {e}")
    # To add more exclusions, simply append to the list:
    # exclusion_list.append("Another Title to Exclude")
    try:
        result = subprocess.run(get_titles_cmd, capture_output=True, text=True, shell=True, encoding='utf-8', errors='ignore')
        if result.returncode != 0:
            logging.error(f"Error getting window titles: {result.stderr}")
            return

        window_titles = sorted([title.strip() for title in result.stdout.strip().split('\n') if title.strip()])

        # Filter the list to exclude specified titles
        filtered_titles = [title for title in window_titles if title not in exclusion_list]

        if not filtered_titles:
            logging.info("No windows with titles found to display. Retrying in a moment...")
            time.sleep(1)
            return

        selected_window = ensure_value_completed_2025_10_13_0000(
            key_name="window_moved_to_front_looped",
            func_n=func_n,
            options=filtered_titles,  # Use the filtered list
            guide_text="Select a window to bring to the front (ESC to exit)",
            history_reset=True,
        )

        # Exit condition: user cancelled fzf
        if not selected_window:
            logging.info("No window selected. Exiting.")
            return

        try:
            # PowerShell requires single quotes in the title to be escaped by doubling them
            safe_title = selected_window.replace("'", "''")

            # PowerShell command to activate the window using the ComObject
            activate_cmd = f"$wshell = New-Object -ComObject wscript.shell; $wshell.AppActivate('{safe_title}')"
            full_cmd = ["powershell", "-Command", activate_cmd]

            logging.info(f"Attempting to bring window to front: \"{selected_window}\"")
            subprocess.run(full_cmd, check=True, capture_output=True, text=True)
            logging.info(f"Successfully sent activation command for window: \"{selected_window}\"")

        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to bring window '{selected_window}' to front. It might have been closed. Error: {e.stderr}")

    except Exception as e:
        logging.error(f"An unexpected error occurred in the main loop: {e}", exc_info=True)
