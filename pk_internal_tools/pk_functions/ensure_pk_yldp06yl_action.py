from typing import Optional

from pk_internal_tools.pk_functions.ensure_pk_yldp06yl_controlled_via_yeelight_library import ensure_pk_yldp06yl_controlled_via_yeelight_library
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pk_yldp06yl_action(
        action: str,
        rgb: Optional[tuple[int, int, int]] = None,
        brightness: Optional[int] = None,
        color_temp: Optional[int] = None,
):
    """
    Control Yeelight YLDP06YL (or compatible) with specified action and parameters.
    """
    import logging
    import traceback

    from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
    from pk_internal_tools.pk_objects.pk_colors import PkColors
    from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE

    try:
        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}Yeelight YLDP06YL control start - Action: {action}{PkColors.RESET}")
        logging.info(PK_UNDERLINE)

        success = ensure_pk_yldp06yl_controlled_via_yeelight_library(
            action=action,
            rgb=rgb,
            brightness=brightness,
            color_temp=color_temp,
        )

        if success:
            logging.info(f"Yeelight '{action}' action succeeded.")
        else:
            logging.error(f"Yeelight '{action}' action failed.")

        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}Yeelight YLDP06YL control end - Action: {action}{PkColors.RESET}")
        logging.info(PK_UNDERLINE)

    except Exception as e:
        logging.error(f"Error in ensure_pk_yldp06yl_action: {e}")
        ensure_debugged_verbose(traceback, e)
