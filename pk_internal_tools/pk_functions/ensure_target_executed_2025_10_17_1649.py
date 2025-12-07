from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_target_executed_2025_10_17_1649(editor, target, mode="sync"):
    import logging
    from pathlib import Path

    from pk_internal_tools.pk_functions.ensure_window_resized_and_positioned_left_half import ensure_window_resized_and_positioned_left_half
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.get_execute_cmd_with_brakets import get_text_chain
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.is_window_opened_via_window_title import is_window_opened_via_window_title

    for _ in [editor, target]:
        _ = Path(_)
        if not _.exists():
            logging.debug(rf"{_} is not existing")
            return
    if not is_window_opened_via_window_title(get_nx(target)):
        ensure_command_executed(cmd=f'start "" {get_text_chain(editor, target)}', mode=mode)
    ensure_window_resized_and_positioned_left_half()
    # ensure_window_to_front(get_nx(target))
    # ensure_pressed("win", "up")
    # ensure_pressed("f11")
