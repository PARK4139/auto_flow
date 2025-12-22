from pk_internal_tools.pk_functions.get_alert_as_gui_window_title import get_alert_as_gui_window_title


def ensure_alert_as_gui_auto_close(text: str, timeout_seconds: int = 5):
    """
    Displays a GUI alert message that automatically closes after a specified timeout.
    This function uses tkinter.Toplevel for customizability, including auto-closing.

    Args:
        text (str): The message to display in the alert box.
        modal_title (str): The title of the alert box window.
        timeout_seconds (int): The number of seconds after which the alert will automatically close.
                               If 0 or less, the alert will behave like a standard alert_as_gui (manual close required).
    """
    import logging
    import tkinter as tk
    import traceback
    from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

    func_n = get_caller_name()
    modal_title: str = get_alert_as_gui_window_title()
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        dialog = tk.Toplevel(root)
        dialog.title(modal_title)

        # Use a Text widget to allow selection
        text_widget = tk.Text(dialog, wrap="word", height=10, width=60)
        text_widget.pack(padx=10, pady=10)
        text_widget.insert("1.0", text)
        text_widget.config(state="disabled")  # Make it read-only but still copyable

        # Add an OK button only if no timeout is set, or for manual closing before timeout
        if timeout_seconds <= 0:
            ok_button = tk.Button(dialog, text="OK", command=dialog.destroy, width=10)
            ok_button.pack(pady=5)
        else:
            # Display a countdown for auto-closing
            countdown_label = tk.Label(dialog, text=f"닫힘까지 {timeout_seconds}초", font=("Helvetica", 10))
            countdown_label.pack(pady=5)

            def update_countdown(current_time):
                if current_time > 0:
                    countdown_label.config(text=f"닫힘까지 {current_time}초")
                    dialog.after(1000, update_countdown, current_time - 1)
                else:
                    dialog.destroy()  # Close the dialog when countdown finishes

            dialog.after(1000, update_countdown, timeout_seconds - 1)  # Start countdown after 1 second

        # --- Center the dialog on the screen ---
        dialog.update_idletasks()

        # Get screen width and height
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()

        # Get dialog width and height
        dialog_width = dialog.winfo_width()
        dialog_height = dialog.winfo_height()

        # Calculate position
        x = (screen_width // 2) - (dialog_width // 2)
        y = (screen_height // 2) - (dialog_height // 2)

        dialog.geometry(f'{dialog_width}x{dialog_height}+{x}+{y}')

        # --- Make it modal ---
        dialog.transient(root)  # Keep the dialog on top of the root window
        dialog.grab_set()  # Direct all events to this dialog
        root.wait_window(dialog)  # Wait until the dialog is closed (manually or by timeout)

        logging.debug("ensure_alert_as_gui_auto_close: root.wait_window(dialog) returned.")
        root.destroy()
        logging.debug(f'"{text[:30]}..." was alerted via {func_n}')

    except Exception as e:
        # Fallback to logging if GUI fails for any reason
        logging.warning("--- GUI Alert Fallback ---")
        logging.warning(f"Could not display GUI alert. Logging content instead.")
        logging.warning(f"model title: {modal_title}")
        logging.warning(f"Text: {text}")
        logging.warning("--------------------------")

        # Also log the detailed exception for debugging purposes
        ensure_debugged_verbose(traceback, e)
