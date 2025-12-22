from __future__ import annotations

import logging
from typing import Optional

from pk_internal_tools.pk_functions.alert_as_gui import alert_as_gui
from pk_internal_tools.pk_functions.ensure_paused import ensure_paused
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


def ensure_pause_or_alert(message: str, is_error: bool = False):
    """
    Pauses execution or shows a GUI alert based on QC_MODE.

    If QC_MODE is active, a GUI alert is displayed. Otherwise, the console
    execution is paused, waiting for user input.

    Args:
        message: The message to display or pause with.
        is_error: If True, indicates an error message for GUI alerts.
                  Currently, ensure_paused does not use this.
    """
    if QC_MODE.is_active:
        alert_as_gui(message, is_error=is_error)
    else:
        ensure_paused(message)
