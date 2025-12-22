import logging
import traceback

from pk_internal_tools.pk_functions.alert_as_gui import alert_as_gui
from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_pk_system_log_editable import ensure_pk_system_log_editable
from pk_internal_tools.pk_functions.ensure_text_saved_to_clipboard import ensure_text_saved_to_clipboard


# @ensure_seconds_measured
def ensure_remote_target_debugged(error_text):
    """
        TODO: Write docstring for ensure_remote_target_debugged.
    """
    try:
        logging.error(error_text)
        ensure_text_saved_to_clipboard(error_text)
        ensure_pk_system_log_editable()
        alert_as_gui(error_text)
        return True
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
