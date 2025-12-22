def classify_pnxs_between_smallest_pnxs_biggest_pnxs():
    import logging

    from pk_internal_tools.pk_functions.get_target_megabite import get_target_megabite
    from pk_internal_tools.pk_objects.pk_etc import BIGGEST_PNXS, SMALLEST_PNXS
    from pk_internal_tools.pk_objects.pk_directories import D_HOME

    logging.debug(f'백업할 f들의 크기를 분류합니다.')
    pnxs = [
        rf"{D_HOME}\Desktop\services\helper-from-youtube-url-to-webm",
        rf"{D_HOME}\Desktop\services",
    ]
    logging.debug(f'biggest_pnxs(300 메가 초과), smallest_pnxs(300 메가 이하) 분류 시도')
    for target in pnxs:
        target_size_megabite = get_target_megabite(target.strip())
        print(target_size_megabite)
        if target_size_megabite <= 300:
            SMALLEST_PNXS.append(target.strip())

        elif 300 < target_size_megabite:
            BIGGEST_PNXS.append(target.strip())
        else:
            logging.debug(f'{target.strip()}pass')

    logging.debug(f'smallest_target 출력')
    # pnxs 에서 biggest_pnxs 과 일치하는 것을 소거 시도
    smallest_pnxs = [i for i in pnxs if i not in BIGGEST_PNXS]
    for target in SMALLEST_PNXS:
        print(target)

    logging.debug(f'biggest_target 출력')
    for target in BIGGEST_PNXS:
        print(target)
    pass
