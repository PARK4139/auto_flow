def ensure_wsl_pk_distro_enabled():
    """
    1. WSL_PK_DISTRO_N이 이미 설치되어 있으면 건너뜀
    2. DEFAULT_DISTRO가 설치 안 됐으면 install
    3. DEFAULT_DISTRO export -> unregister -> import as WSL_PK_DISTRO_N
    4. 성공 시 tar 파일 삭제
    """
    from pk_internal_tools.pk_functions.ensure_command_executed_with_splited_arg import ensure_command_executed_with_splited_arg
    from pk_internal_tools.pk_functions.get_wsl_distro_name_installable import get_wsl_distro_name_installable
    from pk_internal_tools.pk_functions.print_red import print_red
    from pk_internal_tools.pk_objects.pk_etc import WSL_PK_DISTRO_N
    from pathlib import Path
    import logging
    from pk_internal_tools.pk_objects.pk_directories import D_DOWNLOADS
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    # 설정 기본값
    # DEFAULT_DISTRO = "Ubuntu"
    DEFAULT_DISTRO = "Ubuntu-24.04"
    # DEFAULT_DISTRO = "Ubuntu-18.04"
    logging.debug(f"DEFAULT_DISTRO={DEFAULT_DISTRO}{' %%%FOO%%%' if QC_MODE else ''}")

    wsl_distro_name_enabled = get_wsl_distro_name_installable(cmd="wsl -l -v")
    logging.debug(f'''wsl_distro_name_enabled={wsl_distro_name_enabled} ''')
    # n. 이미 WSL_PK_DISTRO_N 확인
    if WSL_PK_DISTRO_N or rf'* {WSL_PK_DISTRO_N}' == wsl_distro_name_enabled:
        logging.debug(f"'{WSL_PK_DISTRO_N}' 배포판이 이미 설치되어 있습니다. 설치를 건너뜁니다.")
        return True

    # 2) DEFAULT_DISTRO 설치 여부
    if DEFAULT_DISTRO not in wsl_distro_name_enabled:
        wsl_distro_name_installable_from_online = get_wsl_distro_name_installable(cmd="wsl --list --online")
        logging.debug(f'''wsl_distro_name_installable_from_online={wsl_distro_name_installable_from_online} ''')
        if DEFAULT_DISTRO not in wsl_distro_name_installable_from_online:
            print_red(f"'{DEFAULT_DISTRO}' 배포판을 online 목록에서 찾을 수 없습니다.")
            return False
        else:
            logging.debug(f"'{DEFAULT_DISTRO}' 배포판을 online 목록에서 찾았습니다.")
        logging.debug(f"'{DEFAULT_DISTRO}' 배포판을 설치합니다...")
        try:
            ensure_command_executed_with_splited_arg(["wsl", "--install", "-d", DEFAULT_DISTRO])
        except Exception as e:
            print_red(f"설치 명령 실패: {e}")
            return False
    else:
        logging.debug(f"'{DEFAULT_DISTRO}' 배포판이 이미 설치되어 있습니다.")

    # 3) export, unregister, import
    tar_path = Path.cwd() / f"{DEFAULT_DISTRO}.tar"  # 임시 export 파일 경로
    install_path = Path(D_DOWNLOADS) / WSL_PK_DISTRO_N  # import 설치 디렉토리
    try:
        logging.debug(f"'{DEFAULT_DISTRO}' 배포판을 '{tar_path}'로 export합니다.")
        ensure_command_executed_with_splited_arg(["wsl", "--export", DEFAULT_DISTRO, str(tar_path)])

        logging.debug(f"'{DEFAULT_DISTRO}' 배포판을 unregister 합니다.")
        ensure_command_executed_with_splited_arg(["wsl", "--unregister", DEFAULT_DISTRO])

        logging.debug(f"'{tar_path}'를 '{install_path}'에 import하여 '{WSL_PK_DISTRO_N}'으로 등록합니다.")
        install_path.mkdir(parents=True, exist_ok=True)
        ensure_command_executed_with_splited_arg(["wsl", "--import", WSL_PK_DISTRO_N, str(install_path), str(tar_path)])
    except Exception as e:
        print_red(f"export/import 중 오류: {e}")
        return False

    # 4) 등록 확인 및 tar 파일 삭제
    wsl_distro_name_enabled_after = get_wsl_distro_name_installable(cmd="wsl -l -v")
    logging.debug(f'''wsl_distro_name_enabled_after={wsl_distro_name_enabled_after} ''')
    if WSL_PK_DISTRO_N or rf'* {WSL_PK_DISTRO_N}' in wsl_distro_name_enabled_after:
        logging.debug(f"'{WSL_PK_DISTRO_N}' 배포판이 정상적으로 import되었습니다.")
        if tar_path.exists():
            logging.debug(f"'{tar_path}' 파일을 삭제합니다.")
            tar_path.unlink()
        return True
    else:
        logging.debug("import 후에도 배포판을 확인할 수 없습니다.")
        return False
