from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured

@ensure_seconds_measured
def ensure_wired_target_controller_executed():
    """
    유선 타겟 컨트롤러를 실행하여 다양한 유선 작업을 수행합니다.
    
    지원하는 작업:
    - Jetpack 5.1.5 플래시
    - Xavier Wi-Fi 네트워크 목록 조회/연결
    - Arduino 개발 환경 설정 (유선/무선)
    - OTA 업로더 에이전트 설치
    - VSCode Live Share 서버/세션 시작
    
    Returns:
        bool: 작업 성공 여부
    """
    try:

        import logging
        import traceback
        from pk_internal_tools.pk_objects.pk_wired_target_controller import PkWiredTargetController
        from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
        from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
        from pk_internal_tools.pk_objects.pk_identifier import PkDevice
        from pk_internal_tools.pk_objects.pk_wireless_target_controller import SetupOpsForPkWirelessTargetController
        from pk_internal_tools.pk_functions.ensure_value_completed_2025_11_11 import ensure_value_completed_2025_11_11
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
        from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

        logging.info(PK_UNDERLINE)
        logging.info(f"{PK_ANSI_COLOR_MAP['BRIGHT_CYAN']}유선 타겟 컨트롤러 실행 시작{PK_ANSI_COLOR_MAP['RESET']}")
        logging.info(PK_UNDERLINE)

        func_n = get_caller_name()

        # 유선 작업 정의
        TASK_FLASH_TARGET = "flash Jetpack 5.1.5 on target (wired)"
        TASK_WIFI_LIST_XAVIER = "list Wi-Fi on Xavier (wired)"  # host_machine and Xavier connected by wired ethernet
        TASK_WIFI_CONNECT_XAVIER = "connect Wi-Fi on Xavier (wired)"  # host_machine and Xavier connected by wired ethernet
        TASK_ARDUINO_DEV_VIA_WIRED_XAVIER_WIRELESS_ARDUINO = "Arduino dev via wired Xavier wireless Arduino (wired)"  # pk_asus - wired - Xavier - wireless - Arduino
        TASK_ARDUINO_DEV_VIA_WIRED_XAVIER_WIRED_ARDUINO_NANO = "Arduino dev via wired Xavier wired Arduino Nano (wired)"  # Xavier - wired (USB) - Arduino Nano
        TASK_ARDUINO_WIRELESS_PROGRAMMING_DEV_ENV_SETUP = "Arduino wireless programming dev env setup (Wi-Fi↔UART bridge) (wired)"  # Wi-Fi↔UART bridge 기반 wireless 프로그래밍 개발 환경 구축
        TASK_INSTALL_OTA_UPLOADER_AGENT_ON_ARDUINO = "install OTA uploader agent on Arduino (wired)"  # 유선 연결을 초기 의존
        TASK_EXECUTE_LIVE_SHARE_SERVER_ON_XAVIER = "execute Live Share server on Xavier (wired)"  # VSCode Live Share 서버 설정 및 시작
        TASK_EXECUTE_LIVE_SHARE_SESSION_ON_HOST = "execute Live Share session on host (wired)"  # Host Machine에서 Live Share 세션 시작

        wired_tasks = [
            TASK_FLASH_TARGET, # 개발완료
            TASK_WIFI_LIST_XAVIER, # 개발완료
            TASK_WIFI_CONNECT_XAVIER, # 개발완료
            TASK_EXECUTE_LIVE_SHARE_SERVER_ON_XAVIER,
            TASK_EXECUTE_LIVE_SHARE_SESSION_ON_HOST,
            TASK_ARDUINO_DEV_VIA_WIRED_XAVIER_WIRELESS_ARDUINO,
            TASK_ARDUINO_DEV_VIA_WIRED_XAVIER_WIRED_ARDUINO_NANO,
            TASK_ARDUINO_WIRELESS_PROGRAMMING_DEV_ENV_SETUP,
            TASK_INSTALL_OTA_UPLOADER_AGENT_ON_ARDUINO,
        ]

        # 사용자에게 작업 선택받기
        logging.info("수행할 유선 제어 작업을 사용자에게 요청합니다.")
        if QC_MODE:
            wired_task = TASK_EXECUTE_LIVE_SHARE_SERVER_ON_XAVIER
            # wired_task = ensure_value_completed_2025_11_11(
            #     key_name="wired_task",
            #     func_n=func_n,
            #     options=wired_tasks,
            #     guide_text="유선 제어 작업을 선택하세요:",
            #     history_reset=True,
            # )
        else:

            wired_task = ensure_value_completed_2025_11_11(
                key_name="wired_task",
                func_n=func_n,
                options=wired_tasks,
                guide_text="유선 제어 작업을 선택하세요:",
                history_reset=True,
            )

        if not wired_task:
            logging.warning("선택된 작업이 없어 유선 타겟 컨트롤러 실행을 종료합니다.")
            return

        logging.info(f"선택된 작업: {wired_task}")

        # 선택된 작업에 따라 로직 분기
        if wired_task == TASK_FLASH_TARGET:
            logging.info(f"'{TASK_FLASH_TARGET}' 작업을 시작합니다.")
            tm = PkWiredTargetController(identifier=PkDevice.jetson_agx_xavier, setup_op=SetupOpsForPkWirelessTargetController.ALL)
            tm.ensure_wired_target_flashed()
            logging.info(f"'{TASK_FLASH_TARGET}' 작업이 완료되었습니다.")

        elif wired_task == TASK_WIFI_LIST_XAVIER:
            logging.info(f"'{TASK_WIFI_LIST_XAVIER}' 작업을 시작합니다.")

            try:
                from pk_internal_tools.pk_functions.ensure_pk_xavier_wifi_listed import (
                    ensure_pk_xavier_wifi_listed,
                    ensure_pk_xavier_wifi_status,
                )

                # 먼저 현재 Wi-Fi 연결 상태 확인
                logging.info("현재 Wi-Fi 연결 상태를 확인합니다...")
                status = ensure_pk_xavier_wifi_status()

                if status:
                    if status["connected"]:
                        logging.info("Wi-Fi 연결됨:")
                        logging.info(f"  인터페이스: {status['interface']}")
                        logging.info(f"  SSID: {status['ssid']}")
                        logging.info(f"  IP 주소: {status['ip_address']}")

                        # P110M과 같은 네트워크인지 확인
                        if status["ip_address"]:
                            ip_parts = status["ip_address"].split(".")
                            if len(ip_parts) == 4 and ip_parts[0] == "192" and ip_parts[1] == "168" and ip_parts[2] == "0":
                                logging.info("P110M과 같은 네트워크(192.168.0.x)에 연결되어 있습니다!")
                            else:
                                logging.warning("⚠️ P110M과 다른 네트워크에 연결되어 있습니다.")
                                logging.warning("  P110M은 192.168.0.x 네트워크에 있습니다.")
                    else:
                        logging.info(f"Wi-Fi 인터페이스({status['interface']})는 존재하지만 연결되어 있지 않습니다.")
                        logging.info("'Xavier Wi-Fi 네트워크 연결' 옵션을 사용하여 연결하세요.")
                else:
                    logging.warning("Wi-Fi 상태를 확인할 수 없습니다.")

                logging.info("")  # 빈 줄

                # Wi-Fi 네트워크 목록 조회
                logging.info("사용 가능한 Wi-Fi 네트워크 목록을 조회합니다...")
                wifi_networks = ensure_pk_xavier_wifi_listed()

                if wifi_networks:
                    logging.info(f"총 {len(wifi_networks)}개의 Wi-Fi 네트워크를 발견했습니다.")

                    # fzf로 선택 가능하도록 옵션 생성
                    from pk_internal_tools.pk_functions.ensure_values_completed_2025_10_23 import (
                        ensure_values_completed_2025_10_23,
                    )

                    options = []
                    for network in wifi_networks:
                        status_text = " [현재 연결됨]" if network["in_use"] else ""
                        option = f"{network['ssid']} (신호: {network['signal']}%, 보안: {network['security']}){status_text}"
                        options.append(option)

                    selected = ensure_values_completed_2025_10_23(
                        key_name="XAVIER_WIFI_NETWORK",
                        options=options,
                        multi_select=False,
                    )

                    if selected:
                        logging.info(f"선택된 Wi-Fi 네트워크: {selected}")
                else:
                    logging.warning("Wi-Fi 네트워크를 찾을 수 없습니다.")

            except Exception as e:
                logging.error(f"Wi-Fi 네트워크 조회 중 예외가 발생했습니다: {e}")
                ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=e)

        elif wired_task == TASK_WIFI_CONNECT_XAVIER:
            logging.info(f"'{TASK_WIFI_CONNECT_XAVIER}' 작업을 시작합니다.")

            try:
                from pk_internal_tools.pk_functions.ensure_pk_xavier_wifi_connected import (
                    ensure_pk_xavier_wifi_connected,
                )

                # 먼저 Wi-Fi 네트워크 목록 조회
                from pk_internal_tools.pk_functions.ensure_pk_xavier_wifi_listed import (
                    ensure_pk_xavier_wifi_listed,
                )

                logging.info("연결할 Wi-Fi 네트워크를 선택하기 위해 목록을 조회합니다...")
                wifi_networks = ensure_pk_xavier_wifi_listed()

                wifi_ssid = None
                if wifi_networks:
                    # fzf로 선택
                    from pk_internal_tools.pk_functions.ensure_values_completed_2025_10_23 import (
                        ensure_values_completed_2025_10_23,
                    )

                    options = []
                    for network in wifi_networks:
                        status = " [현재 연결됨]" if network["in_use"] else ""
                        option = f"{network['ssid']} (신호: {network['signal']}%, 보안: {network['security']}){status}"
                        options.append(option)

                    selected = ensure_values_completed_2025_10_23(
                        key_name="XAVIER_WIFI_NETWORK_TO_CONNECT",
                        options=options,
                        multi_select=False,
                    )

                    if selected and len(selected) > 0:
                        selected_str = selected[0]
                        wifi_ssid = selected_str.split()[0]
                    else:
                        wifi_ssid = None
                else:
                    logging.warning("Wi-Fi 네트워크를 찾을 수 없습니다.")

                # SSID를 직접 입력받기 (목록에서 선택하지 않은 경우)
                if not wifi_ssid:
                    from pk_internal_tools.pk_functions.ensure_env_var_completed_2025_11_24 import (
                        ensure_env_var_completed_2025_11_24,
                    )
                    wifi_ssid = ensure_env_var_completed_2025_11_24(
                        key_name="XAVIER_WIFI_SSID",
                        func_n=func_n,
                        guide_text="연결할 Wi-Fi 네트워크 이름(SSID)을 입력하세요:",
                    )

                if not wifi_ssid:
                    logging.warning("Wi-Fi SSID가 입력되지 않아 연결을 중단합니다.")
                    return

                # Wi-Fi 연결
                success = ensure_pk_xavier_wifi_connected(wifi_ssid=wifi_ssid)

                if success:
                    logging.info("Xavier Wi-Fi 연결 성공")
                else:
                    logging.error("❌ Xavier Wi-Fi 연결 실패")

            except Exception as e:
                logging.error(f"Wi-Fi 연결 중 예외가 발생했습니다: {e}")
                ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=e)

        elif wired_task == TASK_ARDUINO_DEV_VIA_WIRED_XAVIER_WIRELESS_ARDUINO:
            logging.info(f"'{TASK_ARDUINO_DEV_VIA_WIRED_XAVIER_WIRELESS_ARDUINO}' 작업을 시작합니다.")

            try:
                from pk_internal_tools.pk_functions.ensure_arduino_dev_via_wired_xavier_wireless_arduino import (
                    ensure_arduino_dev_via_wired_xavier_wireless_arduino,
                )

                # Xavier 연결 정보
                wired_controller = PkWiredTargetController(
                    identifier=PkDevice.jetson_agx_xavier,
                    setup_op=SetupOpsForPkWirelessTargetController.TARGET,
                )

                xavier_ip = getattr(wired_controller._target, "ip", None) or getattr(wired_controller._target, "hostname", None)
                xavier_user = getattr(wired_controller._target, "user_n", None) or "pk"
                xavier_pw = getattr(wired_controller._target, "pw", None)

                # Arduino Wi-Fi 설정 (선택사항)
                arduino_wifi_ssid = None
                arduino_wifi_password = None

                if QC_MODE:
                    # 테스트 모드에서는 기본값 사용
                    pass
                else:
                    # Arduino Wi-Fi 설정 입력받기 (선택사항)
                    setup_wifi = ensure_value_completed_2025_11_11(
                        key_name="setup_arduino_wifi",
                        func_n=func_n,
                        options=["yes", "no"],
                        guide_text="Arduino Wi-Fi 설정을 입력하시겠습니까? (yes/no):",
                        history_reset=True,
                    )

                    if setup_wifi == "yes":
                        arduino_wifi_ssid = ensure_value_completed_2025_11_11(
                            key_name="arduino_wifi_ssid",
                            func_n=func_n,
                            guide_text="Arduino가 연결할 Wi-Fi SSID를 입력하세요:",
                            history_reset=True,
                        )
                        if arduino_wifi_ssid:
                            arduino_wifi_password = ensure_value_completed_2025_11_11(
                                key_name="arduino_wifi_password",
                                func_n=func_n,
                                guide_text="Wi-Fi 비밀번호를 입력하세요 (선택사항):",
                                history_reset=True,
                            )

                # Arduino 개발 환경 설정
                success = ensure_arduino_dev_via_wired_xavier_wireless_arduino(
                    xavier_ip=xavier_ip,
                    xavier_user=xavier_user,
                    xavier_pw=xavier_pw,
                    arduino_wifi_ssid=arduino_wifi_ssid,
                    arduino_wifi_password=arduino_wifi_password,
                )

                if success:
                    logging.info("✅ Arduino 개발 환경 설정 완료")
                    logging.info("VSCode Remote-SSH로 Xavier에 연결하여 개발을 시작하세요.")
                else:
                    logging.error("❌ Arduino 개발 환경 설정 실패")

            except Exception as e:
                logging.error(f"Arduino 개발 환경 설정 중 예외가 발생했습니다: {e}")
                ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=e)

        elif wired_task == TASK_ARDUINO_DEV_VIA_WIRED_XAVIER_WIRED_ARDUINO_NANO:
            logging.info(f"'{TASK_ARDUINO_DEV_VIA_WIRED_XAVIER_WIRED_ARDUINO_NANO}' 작업을 시작합니다.")

            try:
                from pk_internal_tools.pk_functions.ensure_arduino_dev_via_wired_xavier_wired_arduino_nano import (
                    ensure_arduino_dev_via_wired_xavier_wired_arduino_nano,
                )

                # Xavier 연결 정보
                wired_controller = PkWiredTargetController(
                    identifier=PkDevice.jetson_agx_xavier,
                    setup_op=SetupOpsForPkWirelessTargetController.TARGET,
                )

                xavier_ip = getattr(wired_controller._target, "ip", None) or getattr(wired_controller._target, "hostname", None)
                xavier_user = getattr(wired_controller._target, "user_n", None) or "pk"
                xavier_pw = getattr(wired_controller._target, "pw", None)

                # Arduino Nano Wired 개발 환경 설정
                success = ensure_arduino_dev_via_wired_xavier_wired_arduino_nano(
                    xavier_ip=xavier_ip,
                    xavier_user=xavier_user,
                    xavier_pw=xavier_pw,
                )

                if success:
                    logging.info("✅ Arduino Nano Wired 개발 환경 설정 완료")
                    logging.info("USB 케이블로 Arduino Nano를 Xavier에 연결하고 VSCode Remote-SSH로 개발을 시작하세요.")
                else:
                    logging.error("❌ Arduino Nano Wired 개발 환경 설정 실패")

            except Exception as e:
                logging.error(f"Arduino Nano Wired 개발 환경 설정 중 예외가 발생했습니다: {e}")
                ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=e)

        elif wired_task == TASK_ARDUINO_WIRELESS_PROGRAMMING_DEV_ENV_SETUP:
            logging.info(f"'{TASK_ARDUINO_WIRELESS_PROGRAMMING_DEV_ENV_SETUP}' 작업을 시작합니다.")

            try:
                from pk_internal_tools.pk_functions.ensure_arduino_wireless_programming_dev_env_setup import (
                    ensure_arduino_wireless_programming_dev_env_setup,
                )

                # Xavier 연결 정보
                wired_controller = PkWiredTargetController(
                    identifier=PkDevice.jetson_agx_xavier,
                    setup_op=SetupOpsForPkWirelessTargetController.TARGET,
                )

                xavier_ip = getattr(wired_controller._target, "ip", None) or getattr(wired_controller._target, "hostname", None)
                xavier_user = getattr(wired_controller._target, "user_n", None) or "pk"
                xavier_pw = getattr(wired_controller._target, "pw", None)

                # 초기 유선 설정 건너뛰기 옵션
                skip_initial_setup = False
                if QC_MODE:
                    # 테스트 모드
                    pass
                else:
                    skip_response = ensure_value_completed_2025_11_11(
                        key_name="skip_initial_wired_setup",
                        func_n=func_n,
                        options=["no", "yes"],
                        guide_text="초기 유선 설정을 이미 완료하셨나요? (yes/no):",
                        history_reset=True,
                    )
                    skip_initial_setup = (skip_response == "yes")

                # Wireless 프로그래밍 개발 환경 구축
                success = ensure_arduino_wireless_programming_dev_env_setup(
                    xavier_ip=xavier_ip,
                    xavier_user=xavier_user,
                    xavier_pw=xavier_pw,
                    esp8266_ip=None,  # 사용자 입력받기
                    skip_initial_wired_setup=skip_initial_setup,
                )

                if success:
                    logging.info("✅ Wireless 프로그래밍 개발 환경 구축 완료")
                    logging.info("⚠️ 참고: Arduino Nano 스케치 업로드는 USB 케이블이 필요합니다.")
                    logging.info("시리얼 모니터는 무선으로 사용 가능합니다 (TCP/Telnet).")
                else:
                    logging.error("❌ Wireless 프로그래밍 개발 환경 구축 실패")

            except Exception as e:
                logging.error(f"Wireless 프로그래밍 개발 환경 구축 중 예외가 발생했습니다: {e}")
                ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=e)

        elif wired_task == TASK_INSTALL_OTA_UPLOADER_AGENT_ON_ARDUINO:
            logging.info(f"'{TASK_INSTALL_OTA_UPLOADER_AGENT_ON_ARDUINO}' 작업을 시작합니다.")

            try:
                from pk_internal_tools.pk_functions.ensure_ota_uploader_agent_installed_on_arduino import (
                    ensure_ota_uploader_agent_installed_on_arduino,
                )

                # Xavier 연결 정보
                wired_controller = PkWiredTargetController(
                    identifier=PkDevice.jetson_agx_xavier,
                    setup_op=SetupOpsForPkWirelessTargetController.TARGET,
                )

                xavier_ip = getattr(wired_controller._target, "ip", None) or getattr(wired_controller._target, "hostname", None)
                xavier_user = getattr(wired_controller._target, "user_n", None) or "pk"
                xavier_pw = getattr(wired_controller._target, "pw", None)

                # OTA 에이전트 설치
                success = ensure_ota_uploader_agent_installed_on_arduino(
                    xavier_ip=xavier_ip,
                    xavier_user=xavier_user,
                    xavier_pw=xavier_pw,
                    wifi_ssid=None,  # 사용자 입력받기
                    wifi_password=None,  # 사용자 입력받기
                    ota_password=None,  # 사용자 입력받기
                    serial_port=None,  # 자동 감지 또는 사용자 입력받기
                )

                if success:
                    logging.info("✅ OTA Uploader Agent 설치 가이드 완료")
                    logging.info("⚠️ 참고: 초기 설치 시 유선 연결이 필요합니다.")
                    logging.info("설정 완료 후에는 무선으로 스케치 업로드가 가능합니다.")
                else:
                    logging.error("❌ OTA Uploader Agent 설치 실패")

            except Exception as e:
                logging.error(f"OTA Uploader Agent 설치 중 예외가 발생했습니다: {e}")
                ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=e)

        elif wired_task == TASK_EXECUTE_LIVE_SHARE_SERVER_ON_XAVIER:
            logging.info(f"'{TASK_EXECUTE_LIVE_SHARE_SERVER_ON_XAVIER}' 작업을 시작합니다.")

            try:
                from pk_internal_tools.pk_functions.ensure_vscode_live_share_server_started_on_xavier import (
                    ensure_vscode_live_share_server_started_on_xavier,
                )

                # Xavier 연결 정보
                wired_controller = PkWiredTargetController(
                    identifier=PkDevice.jetson_agx_xavier,
                    setup_op=SetupOpsForPkWirelessTargetController.TARGET,
                )

                xavier_ip = getattr(wired_controller._target, "ip", None) or getattr(wired_controller._target, "hostname", None)
                xavier_user = getattr(wired_controller._target, "user_n", None) or "pk"
                xavier_pw = getattr(wired_controller._target, "pw", None)

                # VSCode Live Share 서버 설정
                success = ensure_vscode_live_share_server_started_on_xavier(
                    xavier_ip=xavier_ip,
                    xavier_user=xavier_user,
                    xavier_pw=xavier_pw,
                )

                if success:
                    logging.info("✅ VSCode Live Share 서버 설정 완료")
                    logging.info("Windows에서 VSCode Remote SSH로 Xavier에 연결하여 Live Share를 사용하세요.")
                else:
                    logging.error("❌ VSCode Live Share 서버 설정 실패")

            except Exception as e:
                logging.error(f"VSCode Live Share 서버 설정 중 예외가 발생했습니다: {e}")
                ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=e)

        elif wired_task == TASK_EXECUTE_LIVE_SHARE_SESSION_ON_HOST:
            logging.info(f"'{TASK_EXECUTE_LIVE_SHARE_SESSION_ON_HOST}' 작업을 시작합니다.")

            try:
                from pk_internal_tools.pk_functions.ensure_vscode_live_share_session_started_on_host import (
                    ensure_vscode_live_share_session_started_on_host,
                )

                # Xavier 연결 정보
                wired_controller = PkWiredTargetController(
                    identifier=PkDevice.jetson_agx_xavier,
                    setup_op=SetupOpsForPkWirelessTargetController.TARGET,
                )

                xavier_host = getattr(wired_controller._target, "hostname", None) or "xavier"

                # 프로젝트 경로 입력받기 (선택사항)
                project_path = None
                if not QC_MODE:
                    project_path = ensure_value_completed_2025_11_11(
                        key_name="xavier_project_path",
                        func_n=func_n,
                        guide_text="Xavier의 프로젝트 경로를 입력하세요 (예: /home/pk/projects/my_project, Enter로 건너뛰기):",
                        history_reset=True,
                    )
                    if not project_path or project_path.strip() == "":
                        project_path = None

                # Live Share 세션 시작
                live_share_url = ensure_vscode_live_share_session_started_on_host(
                    xavier_host=xavier_host,
                    project_path=project_path,
                    auto_copy_url=True,
                )

                if live_share_url:
                    logging.info("✅ Live Share 세션 시작 성공")
                    logging.info(f"Live Share URL: {live_share_url}")
                    logging.info("이 URL을 게스트와 공유하여 협업을 시작하세요.")
                else:
                    logging.info("ℹ️ Live Share 세션 시작 가이드를 제공했습니다.")
                    logging.info("VSCode에서 Live Share 세션을 수동으로 시작한 후,")
                    logging.info("URL 링크를 게스트와 공유하세요.")

            except Exception as e:
                logging.error(f"Live Share 세션 시작 중 예외가 발생했습니다: {e}")
                ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=e)

        logging.info(PK_UNDERLINE)
        logging.info(f"{PK_ANSI_COLOR_MAP['BRIGHT_CYAN']}유선 타겟 컨트롤러 실행 종료{PK_ANSI_COLOR_MAP['RESET']}")
        logging.info(PK_UNDERLINE)
        return True
    except:
        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
        import traceback
        ensure_debug_loged_verbose(traceback)
    finally:
        logging.info(PK_UNDERLINE)
        logging.info(f"{PK_ANSI_COLOR_MAP['BRIGHT_CYAN']}유선 타겟 컨트롤러 실행 종료{PK_ANSI_COLOR_MAP['RESET']}")
        logging.info(PK_UNDERLINE)
