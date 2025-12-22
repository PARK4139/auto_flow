import logging
from pathlib import Path
import time
import importlib

from pk_internal_tools.pk_objects.pk_file_change_handler import FileChangeHandler
from pk_internal_tools.pk_functions.ensure_slept import ensure_slept


def get_files_changed_from_directories_interested(d_interested_list, monitoring_interval=0.2, time_limit=None,
                                                  change_cnt_limit=None):
    """
    Monitors a list of directories for file changes and returns a list of changed files.
    """
    
    # Using lazy import for watchdog as it might not be always used.
    observers = importlib.import_module("watchdog.observers")
    Observer = observers.Observer
    
    d_interested_list = [Path(d) for d in d_interested_list]

    event_handler = FileChangeHandler(change_cnt_limit)
    observer = Observer()

    for d in d_interested_list:
        observer.schedule(event_handler, d, recursive=True)

    logging.debug(
        f"[DETECT F_CHANGED LOOP STARTED] monitoring_interval={monitoring_interval}, len(d_interested_list)={len(d_interested_list)}"
    )

    observer.start()
    start_time = time.time()

    try:
        # The loop continues until the time limit is reached, a keyboard interrupt occurs,
        # or the change limit is reached (handled within FileChangeHandler).
        while True:
            if time_limit is not None and (time.time() - start_time > time_limit):
                logging.debug("Time limit reached. Stopping monitoring.")
                break
            # The change count limit is handled by a StopIteration exception within the event handler
            ensure_slept(seconds=monitoring_interval)
    except StopIteration:
        # This is triggered by the handler if change_cnt_limit is met.
        logging.debug("Change count limit reached. Stopping monitoring.")
        pass
    except KeyboardInterrupt:
        logging.debug("KeyboardInterrupt received. Stopping monitoring.")

    observer.stop()
    observer.join()
    logging.debug("File monitoring observer stopped.")

    return event_handler.f_changed_list
