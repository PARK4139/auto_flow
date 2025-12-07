
def ensure_windows_killed_like_person():
    """
    Gets a list of open windows, lets the user select one or more via fzf,
    and kills the selected windows.
    """
    import subprocess
    import logging
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

    # PowerShell command to get non-empty window titles
    get_titles_cmd = 'powershell -Command "Get-Process | Where-Object { $_.MainWindowTitle -ne \'\' } | Select-Object -ExpandProperty MainWindowTitle"'
    
    try:
        # Execute the command to get window titles, ignoring potential encoding errors
        result = subprocess.run(get_titles_cmd, capture_output=True, text=True, shell=True, encoding='utf-8', errors='ignore')
        if result.returncode != 0:
            logging.error(f"Error getting window titles: {result.stderr}")
            return

        window_titles = sorted([title.strip() for title in result.stdout.strip().split('\n') if title.strip()])
        if not window_titles:
            logging.info("No windows with titles found.")
            return

        # Use fzf to select one or more windows (multi-selection enabled)
        func_n = get_caller_name()
        selected_windows = ensure_value_completed_2025_10_13_0000(
            key_name="windows_to_kill",
            func_n=func_n,
            options=window_titles,
            guide_text="Select window(s) to kill (use Tab to multi-select)",
            is_multi_select=True  # Enable multi-selection
        )

        if selected_windows:
            # If multi-select returns a list of strings
            if not isinstance(selected_windows, list):
                selected_windows = [selected_windows]

            for window_title in selected_windows:
                try:
                    # Command to kill the window by its title
                    kill_cmd_args = ['taskkill', '/F', '/FI', f'WINDOWTITLE eq {window_title}']
                    logging.info(f"Attempting to kill window: \"{window_title}\"" )
                    subprocess.run(kill_cmd_args, shell=True, check=True, capture_output=True, text=True)
                    logging.info(f"Successfully sent kill command for window: \"{window_title}\"" )
                except subprocess.CalledProcessError as e:
                    # taskkill often reports "process not found" if it was successful but the window title disappears fast
                    if "not found" in e.stderr:
                         logging.info(f"Window \"{window_title}\" likely closed successfully.")
                    else:
                        logging.warning(f"Could not kill '{window_title}'. It might have already been closed or require admin rights. Error: {e.stderr}")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)

if __name__ == '__main__':
    import traceback
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        ensure_windows_killed_like_person()
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
