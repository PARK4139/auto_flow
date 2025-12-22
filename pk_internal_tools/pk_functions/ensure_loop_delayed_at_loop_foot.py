def ensure_loop_delayed_at_loop_foot(loop_cnt, mode_level, milliseconds_limit=10000):
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept

    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    if mode_level == 1:  # strict level
        if QC_MODE:
            ensure_paused()
    if mode_level == 2:
        print(rf"[{PkTexts.WAITING}] {milliseconds_limit}{PkTexts.MILLISECONDS}")
        ensure_slept(milliseconds=milliseconds_limit)
    if mode_level == 3:  # natural operation
        if loop_cnt == 1:
            ensure_paused()
