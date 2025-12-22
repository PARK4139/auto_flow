from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.get_window_title_temp_for_cmd_exe import get_window_title_temp_for_cmd_exe


@ensure_seconds_measured
def ensure_command_executed_like_human(cmd) -> None:
    # todo : return 할수 있도록 할수 있을까?
    from pk_internal_tools.pk_functions.run_cmd_exe import _PkModes

    from pk_internal_tools.pk_functions.run_cmd_exe import ensure_cmd_exe_executed
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person import \
        ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person
    from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front

    # ensure_window_title_replaced(custom_title)

    custom_title = get_window_title_temp_for_cmd_exe()
    ensure_cmd_exe_executed(setup_op=_PkModes.CUSTOM_TITLE, custom_title=custom_title)
    ensure_slept(milliseconds=77)

    ensure_window_to_front(window_title_seg=custom_title)
    ensure_slept(milliseconds=77)

    ensure_text_saved_to_clipboard_and_pasted_with_keeping_clipboard_like_person_like_person(text=cmd)
    ensure_slept(milliseconds=77)
    ensure_pressed("enter")
