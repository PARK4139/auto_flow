from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pk_wrapper_starting_routine_done_without_pk_log_file_logging(*, traced_file, traceback):
    from pk_internal_tools.pk_functions.ensure_pk_system_log_initialized import ensure_pk_system_log_initialized
    from pk_internal_tools.pk_functions.ensure_window_resized_and_positioned_left_half import ensure_window_resized_and_positioned_left_half
    from pk_internal_tools.pk_functions.ensure_pk_colorama_initialized_once import ensure_pk_colorama_initialized_once
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_window_title_replaced import ensure_pk_wrapper_starter_window_title_replaced

    ensure_window_resized_and_positioned_left_half()  # -> succeeded
    # ensure_pressed("f11")  # -> succeeded

    ensure_pk_wrapper_starter_suicided(traced_file)
    ensure_pk_colorama_initialized_once()
    ensure_pk_wrapper_starter_window_title_replaced(traced_file)
    ensure_pk_system_log_initialized(traced_file, with_file_logging_mode=False)
