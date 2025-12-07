from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pk_interesting_infos_printed():
    import logging

    from pk_internal_tools.pk_functions.get_pk_interesting_infos import get_pk_interesting_infos
    from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE

    # if QC_MODE:
    #     connected_drives_info = get_connected_drives_info()
    #     logging.debug(connected_drives_info.__repr__())
    #
    #     screen_info = get_pk_screen_info()
    #     logging.debug(screen_info.__repr__())
    #
    #     project_info = get_project_info_from_pyproject()
    #     logging.debug(project_info.__repr__())

    # logging.info(PK_UNDERLINE)
    # logging.info(f"{ANSI_COLOR_MAP['BRIGHT_CYAN']}날짜, 요일, 시간만 음성 출력 (테스트){ANSI_COLOR_MAP['RESET']}")
    # ensure_pk_interesting_infos_spoken(flags=SetupOpsForGetPkInterestingInfo.DATE | SetupOpsForGetPkInterestingInfo.TIME | SetupOpsForGetPkInterestingInfo.DAY_OF_WEEK)

    # logging.info(rf"{PK_UNDERLINE_HALF} wsl info")
    # wsl_distro_names_installed = get_wsl_distro_names_installed()
    # logging.info(rf"wsl_distro_names_installed={wsl_distro_names_installed}")
    # for wsl_distro_name in wsl_distro_names_installed:
    #     ensure_wsl_ip_printed(wsl_distro_name=wsl_distro_name)

    # logging.info(PK_UNDERLINE)
    # logging.info(f"{ANSI_COLOR_MAP['BRIGHT_CYAN']}특정 위치 기반 날씨 검색 (테스트){ANSI_COLOR_MAP['RESET']}")
    # loc, wet = get_location_and_weather_from_web(location="강남역")
    # if loc:
    #     logging.info(f"위치: {loc}")
    #     logging.info(f"날씨: {wet}")

    logging.info(PK_UNDERLINE)
    pk_interesting_infos = get_pk_interesting_infos()
    logging.info(pk_interesting_infos)