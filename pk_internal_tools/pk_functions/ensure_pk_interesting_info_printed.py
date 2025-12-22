def ensure_pk_interesting_info_printed():
    import logging
    from datetime import datetime
    from pk_internal_tools.pk_functions.ensure_all_import_script_printed import ensure_all_import_script_printed
    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.ensure_wifi_pw_printed_fixed import ensure_wifi_pw_printed_fixed
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_functions.get_connected_drives_info import get_connected_drives_info
    from pk_internal_tools.pk_functions.get_location_and_weather_from_web import get_location_and_weather_from_web
    from pk_internal_tools.pk_functions.get_os_n import get_os_n
    from pk_internal_tools.pk_functions.get_pk_screen_info import get_pk_screen_info
    from pk_internal_tools.pk_functions.get_process_infos import get_process_infos
    from pk_internal_tools.pk_functions.get_project_info_from_pyproject import get_project_info_from_pyproject
    from pk_internal_tools.pk_functions.get_tasklist_with_pid import get_tasklist_with_pid
    from pk_internal_tools.pk_functions.get_window_titles import get_window_titles
    from pk_internal_tools.pk_objects.pk_colors import PkColors
    from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
    from pk_internal_tools.pk_objects.pk_modes import PkModesForGetPkInterestingInfo
    # 1. Get options for fzf
    options = [member.name.lower() for member in PkModesForGetPkInterestingInfo if member.name not in ["NONE", "ALL", "DEFAULT"]]

    # 2. Use fzf to get user selection
    func_n = get_caller_name()
    selected_option_str = ensure_value_completed(
        key_name="pk_interesting_info_selection",
        func_n=func_n,
        options=sorted(options),
        guide_text="Select the information you want to print:"
    )

    if not selected_option_str:
        logging.warning("No option selected.")
        return

    # 3. Convert string back to enum member
    try:
        info_type = PkModesForGetPkInterestingInfo[selected_option_str.upper()]
    except KeyError:
        logging.error(f"Invalid option selected: {selected_option_str}")
        return

    # 4. Print the selected information
    logging.info(PK_UNDERLINE)
    logging.info(f"{PkColors.BRIGHT_CYAN}Info: {info_type.name}{PkColors.RESET}")
    logging.info(PK_UNDERLINE)

    if info_type & PkModesForGetPkInterestingInfo.CONNECTED_DRIVES:
        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}Connected Drives Info:{PkColors.RESET}")
        info = get_connected_drives_info()
        logging.info(info)
        logging.info(PK_UNDERLINE)

    if info_type & PkModesForGetPkInterestingInfo.SCREEN:
        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}Screen Info:{PkColors.RESET}")
        info = get_pk_screen_info()
        logging.info(info)
        logging.info(PK_UNDERLINE)

    if info_type & PkModesForGetPkInterestingInfo.PROJECT:
        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}Project Info:{PkColors.RESET}")

        # Lazy import for get_version_from_git
        from pk_internal_tools.pk_functions.ensure_pk_system_version_updated import get_version_from_git
        from pk_internal_tools.pk_functions.get_project_name import get_project_name
        from pk_internal_tools.pk_functions.get_pk_version import get_pk_version

        project_info = get_project_info_from_pyproject()

        if project_info:
            project_name = get_project_name(project_info)
            project_version_pyproject = get_pk_version(project_info)
            logging.info(f"Project Name: {project_name}")
            logging.info(f"Version (from pyproject.toml): {project_version_pyproject}")
        else:
            logging.warning("Could not retrieve project info from pyproject.toml.")

        git_version = get_version_from_git()
        if git_version != "unknown":
            logging.info(f"Project Version (from Git): {git_version}")
        else:
            logging.warning("Could not retrieve project version from Git.")

        logging.info(PK_UNDERLINE)

    if info_type & PkModesForGetPkInterestingInfo.LOCATION_WEATHER:
        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}Location and Weather Info:{PkColors.RESET}")
        loc, wet = get_location_and_weather_from_web()
        if loc:
            logging.info(f"Location: {loc}")
            logging.info(f"Weather: {wet}")
        logging.info(PK_UNDERLINE)

    if info_type & PkModesForGetPkInterestingInfo.DATE:
        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}Date Info:{PkColors.RESET}")
        # This function should probably print the date, not call ensure_pk_interesting_infos_printed() again
        # For now, I'll print the current date
        logging.info(f"Current Date: {datetime.now().strftime('%Y년 %m월 %d일')}")
        logging.info(PK_UNDERLINE)

    if info_type & PkModesForGetPkInterestingInfo.OS:
        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}OS Info:{PkColors.RESET}")
        os_n = get_os_n()
        logging.info(f"OS: {os_n}")
        logging.info(PK_UNDERLINE)

    if info_type & PkModesForGetPkInterestingInfo.WINDOW_TITLES:
        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}Window Titles:{PkColors.RESET}")
        for window_title in get_window_titles():
            logging.info(f"Window Title: {window_title}")
        logging.info(PK_UNDERLINE)

    if info_type & PkModesForGetPkInterestingInfo.PROCESSES:
        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}Processes Info:{PkColors.RESET}")
        for process_name in get_process_infos():
            logging.info(f"Process Name: {process_name}")
        logging.info(PK_UNDERLINE)

    if info_type & PkModesForGetPkInterestingInfo.TASKLIST:
        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}Task List Info:{PkColors.RESET}")
        for task in get_tasklist_with_pid():
            logging.info(f"Task: {task}")
        logging.info(PK_UNDERLINE)

    if info_type & PkModesForGetPkInterestingInfo.WIFI:
        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}WiFi Info:{PkColors.RESET}")
        wifi_name, wifi_pw = ensure_wifi_pw_printed_fixed()
        logging.info(f'WiFi Name: {wifi_name}')
        logging.info(f'WiFi Password: {wifi_pw}')
        logging.info(PK_UNDERLINE)

    if info_type & PkModesForGetPkInterestingInfo.PYTHON_IMPORTS:
        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}Python Imports:{PkColors.RESET}")
        ensure_all_import_script_printed()
        logging.info(PK_UNDERLINE)

    if info_type & PkModesForGetPkInterestingInfo.HELP:
        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}Help Information:{PkColors.RESET}")
        _print_help()
        logging.info(PK_UNDERLINE)

    # For STOCK, the rich table is printed in get_pk_interesting_infos (plural)
    # So we don't need to print it here again.


def _print_help():
    import logging
    from pk_internal_tools.pk_objects.pk_colors import PkColors
    from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
    from pk_internal_tools.pk_objects.pk_modes import PkModesForGetPkInterestingInfo
    logging.info(PK_UNDERLINE)
    logging.info(f"{PkColors.BRIGHT_CYAN}Available Info Types:{PkColors.RESET}")
    options = [member.name.lower() for member in PkModesForGetPkInterestingInfo if member.name not in ["NONE", "ALL", "DEFAULT"]]
    for option in sorted(options):
        logging.info(f"{option}")  # Use a bullet point for options
    logging.info(PK_UNDERLINE)
