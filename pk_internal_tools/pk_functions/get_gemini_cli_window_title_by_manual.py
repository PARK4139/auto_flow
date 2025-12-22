from pk_internal_tools.pk_functions.ensure_script_file_created import ensure_script_file_created
from pk_internal_tools.pk_functions.get_gemini_cli_expected_titles import get_gemini_cli_expected_titles
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_gemini_cli_window_title_by_manual(gemini_cli_expected_titles= None):
    import logging
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
    from pk_internal_tools.pk_functions.get_gemini_prompt_interface_title import get_pk_gemini_title

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed

    if gemini_cli_expected_titles is None:
        gemini_cli_expected_titles = get_gemini_cli_expected_titles()

    logging.debug("Automatic detection failed. Falling back to manual selection.")
    for option in gemini_cli_expected_titles:
        logging.debug(f"Attempting to bring window to front: {option}")
        ensure_window_to_front(option)
        logging.debug(f"Finished attempting to bring window to front: {option}")

    logging.debug(f"Attempting to bring orchestrator window to front: {get_pk_gemini_title()}")
    ensure_window_to_front(get_pk_gemini_title())
    logging.debug(f"Finished attempting to bring orchestrator window to front: {get_pk_gemini_title()}")

    key_name = "gemini_cli_window_title"
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    logging.debug(f"Calling ensure_value_completed with key_name={key_name}, func_n={func_n}, options={gemini_cli_expected_titles}")
    selected = ensure_value_completed(key_name=key_name, func_n=func_n, options=gemini_cli_expected_titles)
    logging.debug(f"ensure_value_completed returned: {selected}")
    gemini_cli_window_title = selected

    logging.debug(f'''gemini_cli_window_title={gemini_cli_window_title}''')
    logging.debug("Exiting get_gemini_cli_window_title function.")
    return gemini_cli_window_title





