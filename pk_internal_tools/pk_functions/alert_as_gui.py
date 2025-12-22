import logging
import traceback
import tkinter as tk
from tkinter import messagebox
import threading
import sys

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
from pk_internal_tools.pk_functions.get_alert_as_gui_window_title import get_alert_as_gui_window_title
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name


def alert_as_gui(text):
    """
    Displays a simple GUI alert message.

    Args:
        text (str): The message to display in the alert box.
    """
    title = get_alert_as_gui_window_title()
    func_n = get_caller_name()

    try:
        # Check if a Tkinter root window is already active in the main thread
        # This is a heuristic and might not be foolproof
        is_main_thread = threading.current_thread() is threading.main_thread()
        has_toplevel_windows = False
        try:
            # Attempt to get default root, if it exists and is not destroyed
            if tk._default_root and tk._default_root.winfo_exists():
                has_toplevel_windows = True
        except Exception as e:
            pass # Ignore errors if _default_root is not set or destroyed


        if is_main_thread and not has_toplevel_windows:
            # If in main thread and no existing Tkinter app, create and destroy a new root
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo(title, text)
            root.destroy()
            logging.debug(f'{text} is alerted via {func_n} (new Tkinter instance)')
        elif is_main_thread and has_toplevel_windows:
            # If in main thread and Tkinter app is already running, just use messagebox
            messagebox.showinfo(title, text)
            logging.debug(f'{text} is alerted via {func_n} (existing Tkinter instance)')
        else:
            # If not in main thread, or a new Tkinter instance couldn't be safely created,
            # fallback to logging and print a warning for the user
            logging.warning("--- GUI Alert Fallback (Non-main thread or Tkinter error) ---")
            logging.warning(f"Could not display GUI alert for '{title}'. Logging content instead.")
            logging.warning(f"Text: {text}")
            logging.warning("---------------------------------------------------------")
            print(f"ALERT: {title} - {text}") # Ensure user sees the message
            # Optionally, re-raise if this is considered a critical error
            # raise
    except Exception as e:
        # Catch any other unexpected errors during Tkinter operation
        logging.error(f"Error displaying GUI alert (fallback to logging): {e}")
        logging.warning("--- GUI Alert Fallback ---")
        logging.warning(f"Could not display GUI alert for '{title}'. Logging content instead.")
        logging.warning(f"Text: {text}")
        logging.warning("--------------------------")
        print(f"ALERT: {title} - {text}") # Ensure user sees the message
        ensure_debugged_verbose(traceback, e)
