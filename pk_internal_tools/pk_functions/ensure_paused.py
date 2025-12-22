def ensure_paused(text=None):
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_functions.alert_as_gui import alert_as_gui

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    # logging.debug(PK_UNDERLINE)

    if text is None:
        if QC_MODE:
            text = f"paused by {func_n}()"
        else:
            text = f"continue:enter"

    if QC_MODE:
        alert_as_gui(text=text)
        # input(f"{PkColors.TC_ORANGE_TONE1}{text}{PkColors.RESET}")
    else:
        alert_as_gui(text=text)
        # input(f"{PkColors.TC_ORANGE_TONE1}{text}{PkColors.RESET}")
