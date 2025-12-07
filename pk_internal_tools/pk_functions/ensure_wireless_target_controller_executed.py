from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_wireless_target_controller_executed():
    import logging
    import traceback
    from pk_internal_tools.pk_functions.ensure_console_paused import ensure_console_paused
    from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
    try:
        from pk_internal_tools.pk_functions.ensure_pk_xavier_terminal_opened_via_ssh_like_person import ensure_pk_xavier_terminal_opened_via_ssh_like_person
        from pk_internal_tools.pk_functions.ensure_pk_p110m_controlled_via_tapo_library import (
            ensure_pk_p110m_controlled_via_tapo_library,
        )
        from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured

        from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
        from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
        from pk_internal_tools.pk_objects.pk_operation_options import SetupOpsForPkWirelessTargetController
        from pk_internal_tools.pk_objects.pk_wireless_target_controller import PkWirelessTargetController
        from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
        import requests
        from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
        from pk_internal_tools.pk_functions.ensure_home_assistant_ready_on_target import ensure_home_assistant_ready_on_target
        from pk_internal_tools.pk_functions.ensure_home_assistant_onboarding_completed import ensure_home_assistant_onboarding_completed
        from pk_internal_tools.pk_functions.dom_snapshot_analyzer import (
            capture_dom_snapshot,
            analyze_buttons_for_keywords,
        )
        from pk_internal_tools.pk_objects.pk_identifier import PkDevice
        from pk_internal_tools.pk_objects.pk_p110m_controller import PkP110mController
        from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

        func_n = get_caller_name()
        logging.info(PK_UNDERLINE)
        logging.info(f"{PK_ANSI_COLOR_MAP['BRIGHT_CYAN']}무선 타겟 컨트롤러 실행 시작{PK_ANSI_COLOR_MAP['RESET']}")
        logging.info(PK_UNDERLINE)

        # Xavier controller를 한 번만 생성하여 재사용 (같은 세션 내에서)
        shared_controller = None
        controller_initialized = False

        # n. 무선 작업 목록 정의
        control_terminal_on_xavier = "CONTROL TERMINAL ON XAVIER"  # WIRELESS PROGRAMMING
        control_p110m_via_tapo_library_on_xavier = "CONTROL P110M VIA TAPO LIBRARY ON XAVIER"
        control_p110m_via_python_kasa_library_on_xavier = "CONTROL P110M VIA PYTHON-KASA LIBRARY(TAPO LOCAL API) ON XAVIER"
        control_p110m_via_ha_on_xavier = "CONTROL P110M VIA HOME ASSISTANT ON XAVIER"
        control_p110m_monitor_on_xavier = "CONTROL P110M MONITOR ON XAVIER"
        execute_pk_interesting_data_dashboard_and_control_sever_on_xavier = "EXECUTE PK INTERESTING DATA DASHBOARD AND CONTROL SEVER ON XAVIER"
        arduino_code_dev_env_on_xavier = "ONBOARD ARDUINO DEV ENVIRONMENT ON XAVIER"
        control_tv_server_on_xavier = "CONTROL TV SERVER ON XAVIER"
        execute_api_server_on_xavier = "EXECUTE API SERVER ON XAVIER"
        execute_kiri_server_on_xavier = "EXECUTE KIRI SERVER ON XAVIER"  # TBD : Xavier 와 PK_QCY_H3_ANC_HEADSET를 자동연결 via Bluetooth # Bluetooth USB dongle 별도 필요하여 고민 중, # TODO : 실시간 앵무새
        develop_arduino_ota_environment_on_xavier = "DEVELOP ARDUINO OTA ENVIRONMENT ON XAVIER"
        develop_arduino_code_on_xavier = "DEVELOP ARDUINO CODE ON XAVIER"  # WIRELESS PROGRAMMING
        control_wireless_target_via_chrome_remote_desktop_on_host = "CONTROL WIRELESS TARGET VIA CHROME REMOTE DESKTOP ON HOST"
        wireless_tasks = [
            control_tv_server_on_xavier,
            execute_api_server_on_xavier,
            execute_pk_interesting_data_dashboard_and_control_sever_on_xavier,  # 여기에 control_p110m_monitor_on_xavier 기능을 통합 pk p110m monitor health check 죽었으면, 죽은사유로깅 && 재실행
            arduino_code_dev_env_on_xavier,
            develop_arduino_code_on_xavier,
            develop_arduino_ota_environment_on_xavier,
            execute_kiri_server_on_xavier,
            # control_p110m_via_python_kasa_library_on_xavier, # control_p110m_via_tapo_library_on_xavier 로 대체 가능하여, 개발필요성 떨어져 임시주석
            # control_p110m_via_ha_on_xavier,  # control_p110m_via_tapo_library_on_xavier 로 대체 가능하여, 개발필요성 떨어져 임시주석, 개발필요시 주석해제 예정
            control_wireless_target_via_chrome_remote_desktop_on_host,  # succeeded, TODO pk_asus | pk_renova | pk_huvitz_gram 등등 fzf 로 선택하도록
            control_terminal_on_xavier,  # succeeded
            control_p110m_via_tapo_library_on_xavier,  # succeeded, 전화번호 말고 이메일형식으로 2차 인증없이
        ]
        history_reset = True

        # n. 사용자에게 작업 선택받기
        wireless_task = None
        while not wireless_task:
            logging.info("수행할 무선 제어 작업을 사용자에게 요청합니다.")

            # QC_MODE와 상관없이 동일한 fzf 호출 사용
            wireless_task = ensure_value_completed(
                key_name="wireless_task",
                func_n=func_n,
                options=wireless_tasks,
                guide_text="수행할 무선 제어 작업을 선택하세요:",
                history_reset=history_reset
            )

            # fzf에서 아무것도 선택하지 않으면 empty string('') 또는 '[]' 문자열이 반환될 수 있음
            if not wireless_task or wireless_task == '[]':
                wireless_task = None  # 루프를 다시 실행하기 위해 None으로 리셋
                logging.warning("아무 작업도 선택되지 않았습니다. 목록에서 작업을 선택해야 합니다. (종료: Ctrl+C)")
                # fzf가 즉시 닫힐 경우 무한 루프 방지를 위해 약간의 딜레이 추가
                from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
                ensure_slept(milliseconds=500)

            # pk_debug
            # ensure_console_paused()

        logging.info(f"선택된 작업: {wireless_task}")

        # n. 선택된 작업에 따라 로직 분기
        if wireless_task == control_terminal_on_xavier:
            ensure_pk_xavier_terminal_opened_via_ssh_like_person()

        if wireless_task == control_p110m_via_ha_on_xavier:
            logging.info(f"'{control_p110m_via_ha_on_xavier}' 작업을 시작합니다.")

            try:
                # 기존 controller 재사용 또는 새로 생성
                if shared_controller is None:
                    logging.info("Xavier 연결 생성 중...")
                    shared_controller = PkWirelessTargetController(identifier=PkDevice.jetson_agx_xavier, setup_op=SetupOpsForPkWirelessTargetController.TARGET)
                    controller_initialized = True
                else:
                    logging.info("✅ 기존 Xavier 연결 재사용")

                controller = shared_controller
                if not ensure_home_assistant_ready_on_target(controller):
                    logging.error("Home Assistant 환경을 준비하지 못했습니다. 작업을 종료합니다.")
                    return
                p110m_manager = PkP110mController(wireless_target_controller=controller)

                onboarding_done = ensure_home_assistant_onboarding_completed(
                    ha_url=p110m_manager.ha_url,
                    headless_mode=False,
                )
                if not onboarding_done:
                    logging.warning("Home Assistant 온보딩 자동화가 완료되지 않았습니다. 필요 시 브라우저에서 수동으로 진행하세요.")

                # 온보딩 완료 후 P110M 장치 추가 시도
                if onboarding_done:
                    from pk_internal_tools.pk_functions.ensure_ha_add_device_clicked import (
                        ensure_ha_add_to_home_assistant_button_clicked,
                        ensure_ha_add_device_clicked,
                    )
                    from pk_internal_tools.pk_functions.ha_selenium_driver_manager import (
                        get_ha_selenium_driver,
                    )
                    from selenium.webdriver.support.ui import WebDriverWait
                    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept

                    logging.info("P110M 장치 추가를 위해 둘러보기 페이지 확인 및 + 버튼 클릭을 시도합니다.")
                    try:
                        # 전역 드라이버 재사용 (온보딩에서 사용한 동일한 브라우저 세션)
                        driver = get_ha_selenium_driver(headless_mode=False)
                        wait = WebDriverWait(driver, 30)

                        # 현재 페이지 확인
                        from pk_internal_tools.pk_functions.ensure_home_assistant_onboarding_completed import (
                            _detect_current_page,
                        )
                        from pk_internal_tools.pk_functions.ensure_slept import ensure_slept

                        # 페이지 로딩 완료 대기
                        from selenium.webdriver.support import expected_conditions as EC
                        try:
                            WebDriverWait(driver, 10).until(
                                lambda d: d.execute_script("return document.readyState") == "complete"
                            )
                            logging.debug("페이지 로딩 완료 확인됨")
                        except Exception as e:
                            logging.debug("페이지 로딩 완료 대기 중 오류 (무시): %s", e)

                        ensure_slept(milliseconds=2000)  # 동적 콘텐츠 로딩 대기

                        # 현재 페이지 판별
                        detected_page = _detect_current_page(driver)
                        current_url = driver.current_url
                        logging.info("현재 페이지 판별 결과: %s (URL: %s)", detected_page, current_url)

                        # 둘러보기 페이지가 아니면 둘러보기 페이지로 이동 시도
                        if detected_page != "overview":
                            if detected_page == "auth":
                                logging.warning("인증 페이지로 리다이렉트되었습니다. 둘러보기 페이지로 이동을 시도합니다.")
                            elif detected_page == "login":
                                logging.warning("로그인 페이지입니다. 로그인을 먼저 수행해야 합니다.")
                            else:
                                logging.warning("둘러보기 페이지가 아닙니다. (판별 결과: %s) 둘러보기 페이지로 이동을 시도합니다.", detected_page)

                            # 둘러보기 페이지로 이동
                            overview_url = p110m_manager.ha_url.rstrip("/") + "/"
                            logging.info("둘러보기 페이지로 이동: %s", overview_url)
                            driver.get(overview_url)

                            # 페이지 로딩 대기
                            try:
                                WebDriverWait(driver, 10).until(
                                    lambda d: d.execute_script("return document.readyState") == "complete"
                                )
                            except Exception:
                                pass
                            ensure_slept(milliseconds=2000)

                            # 다시 페이지 판별
                            detected_page = _detect_current_page(driver)
                            logging.info("둘러보기 페이지 이동 후 판별 결과: %s", detected_page)

                        # 둘러보기 페이지 확인 후 + 버튼 클릭
                        # 주석처리: 장치 추가는 수동으로 수행
                        # if detected_page == "overview":
                        #     # lovelace/0 URL인 경우 실제 둘러보기 페이지(/)로 이동
                        #     if "/lovelace/0" in current_url:
                        #         logging.info("lovelace/0 페이지에서 실제 둘러보기 페이지(/)로 이동합니다.")
                        #         overview_url = p110m_manager.ha_url.rstrip("/") + "/"
                        #         driver.get(overview_url)
                        #         try:
                        #             WebDriverWait(driver, 10).until(
                        #                 lambda d: d.execute_script("return document.readyState") == "complete"
                        #             )
                        #         except Exception:
                        #             pass
                        #         ensure_slept(milliseconds=2000)
                        #         current_url = driver.current_url
                        #         logging.info("둘러보기 페이지로 이동 완료 (URL: %s)", current_url)
                        #
                        #     logging.info("둘러보기 페이지 확인됨. + 버튼 클릭을 시도합니다.")
                        #     # "Add to Home Assistant" 버튼 클릭
                        #     if ensure_ha_add_to_home_assistant_button_clicked(driver, wait):
                        #         ensure_slept(milliseconds=1000)  # 메뉴 표시 대기
                        #
                        #         # "Add device" 메뉴 항목 클릭
                        #         if ensure_ha_add_device_clicked(driver, wait):
                        #             ensure_slept(milliseconds=2000)  # 다음 페이지 로딩 대기
                        #
                        #             # 장치 검색 입력 필드에 "TP-Link" 입력
                        #             from pk_internal_tools.pk_functions.ensure_ha_add_device_clicked import (
                        #                 ensure_ha_device_search_input_filled,
                        #             )
                        #
                        #             if ensure_ha_device_search_input_filled(driver, wait, search_text="TP-Link"):
                        #                 ensure_slept(milliseconds=2000)  # 검색 결과 로딩 대기
                        #
                        #                 # "TP-Link" 통합 항목 클릭
                        #                 from pk_internal_tools.pk_functions.ensure_ha_add_device_clicked import (
                        #                     ensure_ha_integration_item_clicked,
                        #                 )
                        #
                        #                 if ensure_ha_integration_item_clicked(driver, wait, integration_name="TP-Link"):
                        #                     ensure_slept(milliseconds=2000)  # 다음 페이지 로딩 대기
                        #
                        #                     # "Tapo" 통합 항목 클릭
                        #                     if ensure_ha_integration_item_clicked(driver, wait, integration_name="Tapo"):
                        #                         logging.info("P110M 장치 추가 프로세스가 시작되었습니다. 'TP-Link' -> 'Tapo' 통합 선택 완료.")
                        #                         ensure_slept(milliseconds=2000)  # 다음 페이지 로딩 대기
                        #                     else:
                        #                         logging.warning("'Tapo' 통합 항목을 클릭하지 못했습니다.")
                        #                 else:
                        #                     logging.warning("'TP-Link' 통합 항목을 클릭하지 못했습니다.")
                        #             else:
                        #                 logging.warning("장치 검색 입력 필드에 'TP-Link'를 입력하지 못했습니다.")
                        #         else:
                        #             logging.warning("'Add device' 메뉴 항목을 클릭하지 못했습니다.")
                        #     else:
                        #         logging.warning("'Add to Home Assistant' 버튼을 클릭하지 못했습니다.")
                        # else:
                        #     logging.warning("둘러보기 페이지가 아닙니다. + 버튼 클릭을 건너뜁니다.")

                        logging.info("장치 추가는 수동으로 수행해주세요. 브라우저가 열려 있습니다.")

                        # 음성 안내
                        from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
                        ensure_spoken("둘러보기 페이지에 도달하였습니다. + 버튼을 눌러 장치를 추가해 주세요")

                        # 드라이버는 headless_mode가 아니면 열어둠 (디버깅용)
                        # headless_mode인 경우에만 닫음
                        # 여기서는 headless_mode=False이므로 열어둠
                    except Exception as add_device_exc:
                        logging.error("P110M 장치 추가 중 오류 발생: %s", add_device_exc, exc_info=True)

                logging.info("스마트 플러그에 수행할 액션을 사용자에게 요청합니다.")
                if QC_MODE:
                    # p110m_action = "on"
                    p110m_action = ensure_value_completed(
                        key_name="p110m_api_action",
                        func_n=func_n,
                        options=["on", "off", "toggle"],
                        guide_text="제어할 액션을 선택하세요:",
                        history_reset=history_reset
                    )
                else:
                    p110m_action = ensure_value_completed(
                        key_name="p110m_api_action",
                        func_n=func_n,
                        options=["on", "off", "toggle"],
                        guide_text="제어할 액션을 선택하세요:",
                        history_reset=history_reset
                    )

                if not p110m_action:
                    logging.warning("액션이 선택되지 않아 작업을 종료합니다.")
                    return

                # Get the entity_id from the user
                if QC_MODE:
                    entity_id = 'switch.tapo_p110m_plug'  # pk_option
                else:
                    entity_id = ensure_value_completed(
                        key_name="ha_entity_id_for_api",
                        func_n=func_n,
                        guide_text="제어할 스위치의 Entity ID를 입력하세요 (예: switch.tapo_p110m_plug):",
                        history_reset=history_reset
                    )

                if not entity_id:
                    logging.error("Entity ID가 입력되지 않아 작업을 종료합니다.")
                    return

                ha_token = None

                # n. Check HA_TOKEN on the target environment first
                try:
                    stdout, _, exit_status = controller.ensure_command_to_wireless_target(
                        cmd="printenv HA_TOKEN",
                        timeout_seconds=10,
                        use_sudo=False,
                    )
                    if exit_status == 0 and stdout:
                        remote_token = stdout[0].strip()
                        if remote_token:
                            ha_token = remote_token
                            logging.info("타겟 장치 환경 변수 'HA_TOKEN'을 사용합니다.")
                except Exception as e:
                    logging.warning("타겟 장치에서 HA_TOKEN 확인 중 오류: %s", e)

                def _diagnose_home_assistant_access(controller):
                    logging.info("Home Assistant 접속 전 진단을 수행합니다.")
                    diagnostics = [
                        ("Home Assistant 서비스 상태", "systemctl status home-assistant@homeassistant --no-pager", True),
                        ("로컬 HTTP 응답 확인", "curl -I http://localhost:8123 || true", False),
                        ("8123 포트 리스닝 확인", "ss -tln | grep 8123 || true", False),
                    ]
                    for desc, cmd, needs_sudo in diagnostics:
                        try:
                            logging.info("진단 항목: %s", desc)
                            stdout, stderr, exit_status = controller.ensure_command_to_wireless_target(
                                cmd=cmd,
                                timeout_seconds=20,
                                use_sudo=needs_sudo,
                            )
                            logging.info(
                                "  - exit_status: %s\n  - stdout: %s\n  - stderr: %s",
                                exit_status,
                                stdout if stdout else "<empty>",
                                stderr if stderr else "<empty>",
                            )
                        except Exception as diag_error:
                            logging.warning("진단 명령 실행 실패 (%s): %s", desc, diag_error)

                if not ha_token:
                    _diagnose_home_assistant_access(controller)
                    wireless_target_ip = getattr(controller.wireless_target, "ip", None) or getattr(controller.wireless_target, "hostname", None)
                    if wireless_target_ip:
                        try:
                            dom_url = f"http://{wireless_target_ip}:8123/onboarding.html"
                            logging.info("HA 토큰 수동 생성 안내를 위해 DOM을 캡처합니다: %s", dom_url)
                            response = requests.get(dom_url, timeout=15)
                            response.raise_for_status()
                            snapshot = capture_dom_snapshot(response.text, label="ha_login_prompt", prefix="ha_token_stop")
                            button_matches = analyze_buttons_for_keywords(snapshot.buttons)
                            logging.info(
                                "[HA_TOKEN_STOP] DOM 스냅샷=%s 버튼후보=%s",
                                snapshot.snapshot_path,
                                button_matches,
                            )
                        except Exception as dom_exc:
                            logging.warning("HA 로그인 페이지 DOM 캡처 실패: %s", dom_exc)
                    logging.info("HA_TOKEN 자동화 개발 지점에서 중단합니다. 브라우저에서 로그인/토큰을 생성한 뒤 다시 실행하세요.")
                    return

                # Call the control method, which now uses the FastAPI server
                success = p110m_manager.ensure_pk_p110m_controlled_on_target(
                    action=p110m_action,
                    entity_id=entity_id,
                    ha_token=ha_token
                )

                if success:
                    logging.info(f"Xavier API를 통해 '{entity_id}'에 '{p110m_action}' 액션을 성공적으로 요청했습니다.")
                else:
                    logging.error(f"Xavier API를 통한 '{entity_id}' 제어에 실패했습니다.")
            except Exception as e:
                logging.error(f"P110M 제어 작업 중 예외가 발생했습니다: {e}")
                ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=e)

        elif wireless_task == control_p110m_via_python_kasa_library_on_xavier:
            logging.info(f"'{control_p110m_via_python_kasa_library_on_xavier}' 작업을 시작합니다.")

            try:
                # python-kasa를 사용한 로컬 제어
                from pk_internal_tools.pk_functions.ensure_pk_p110m_controlled_via_python_kasa_library import (
                    ensure_pk_p110m_controlled_via_python_kasa_library,
                )

                # 액션 선택
                logging.info("스마트 플러그에 수행할 액션을 사용자에게 요청합니다.")
                if QC_MODE:
                    # p110m_action = "on"
                    p110m_action = ensure_value_completed(
                        key_name="p110m_tapo_local_action",
                        func_n=func_n,
                        options=["on", "off", "toggle", "info"],
                        guide_text="제어할 액션을 선택하세요:",
                        history_reset=history_reset
                    )
                else:
                    p110m_action = ensure_value_completed(
                        key_name="p110m_tapo_local_action",
                        func_n=func_n,
                        options=["on", "off", "toggle", "info"],
                        guide_text="제어할 액션을 선택하세요:",
                        history_reset=history_reset
                    )

                if not p110m_action:
                    logging.warning("액션이 선택되지 않아 작업을 종료합니다.")
                    return

                # P110M 제어 실행
                success = ensure_pk_p110m_controlled_via_python_kasa_library(
                    action=p110m_action,
                    discover=True,
                )

                if success:
                    logging.info(f"python-kasa를 통해 P110M '{p110m_action}' 액션을 성공적으로 수행했습니다.")
                else:
                    logging.error(f"python-kasa를 통한 P110M 제어에 실패했습니다.")

            except Exception as e:
                logging.error(f"P110M 제어 작업 중 예외가 발생했습니다: {e}")
                ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=e)

        elif wireless_task == control_p110m_via_tapo_library_on_xavier:
            logging.info(f"'{control_p110m_via_tapo_library_on_xavier}' 작업을 시작합니다.")

            try:
                # tapo 라이브러리를 사용한 로컬 제어

                # 액션 선택
                logging.info("스마트 플러그에 수행할 액션을 사용자에게 요청합니다.")
                if QC_MODE:
                    # p110m_action = "on"
                    p110m_action = ensure_value_completed(
                        key_name="p110m_tapo_library_action",
                        func_n=func_n,
                        options=["on", "off", "toggle", "info"],
                        guide_text="제어할 액션을 선택하세요:",
                        history_reset=history_reset
                    )
                else:
                    p110m_action = ensure_value_completed(
                        key_name="p110m_tapo_library_action",
                        func_n=func_n,
                        options=["on", "off", "toggle", "info"],
                        guide_text="제어할 액션을 선택하세요:",
                        history_reset=history_reset
                    )

                if not p110m_action:
                    logging.warning("액션이 선택되지 않아 작업을 종료합니다.")
                    return

                # P110M 제어 실행
                success = ensure_pk_p110m_controlled_via_tapo_library(action=p110m_action)

                if success:
                    logging.info(f"tapo 라이브러리를 통해 P110M '{p110m_action}' 액션을 성공적으로 수행했습니다.")
                else:
                    logging.error(f"tapo 라이브러리를 통한 P110M 제어에 실패했습니다.")

            except Exception as e:
                logging.error(f"P110M 제어 작업 중 예외가 발생했습니다: {e}")
                ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=e)

        elif wireless_task == control_p110m_monitor_on_xavier:
            logging.info(f"'{control_p110m_monitor_on_xavier}' 작업을 시작합니다.")

            try:
                # 모니터링 간격 선택
                logging.info("P110M 에너지 모니터링 간격을 선택하세요.")
                if QC_MODE:
                    monitor_interval = ensure_value_completed(
                        key_name="p110m_monitor_interval",
                        func_n=func_n,
                        options=["60", "300", "600", "1800"],
                        guide_text="모니터링 간격을 선택하세요 (초):",
                        history_reset=history_reset
                    )
                else:
                    monitor_interval = ensure_value_completed(
                        key_name="p110m_monitor_interval",
                        func_n=func_n,
                        options=["60", "300", "600", "1800"],
                        guide_text="모니터링 간격을 선택하세요 (초):",
                        history_reset=history_reset
                    )

                if not monitor_interval:
                    logging.warning("모니터링 간격이 선택되지 않아 작업을 종료합니다.")
                    return

                monitor_interval = int(monitor_interval)
                logging.info("Xavier에서 P110M 에너지 모니터링을 시작합니다 (간격: %d초)", monitor_interval)
                logging.info("에너지 데이터는 Xavier의 DB에 저장됩니다.")
                logging.info("모니터링을 중지하려면 Ctrl+C를 누르세요.")

                # Xavier에서 모니터링 스크립트 실행 (백그라운드)
                # 기존 controller 재사용 또는 새로 생성
                if shared_controller is None:
                    logging.info("Xavier 연결 생성 중...")
                    shared_controller = PkWirelessTargetController(identifier=PkDevice.jetson_agx_xavier, setup_op=SetupOpsForPkWirelessTargetController.TARGET)
                    controller_initialized = True
                else:
                    logging.info("✅ 기존 Xavier 연결 재사용")

                controller = shared_controller

                # Xavier에서 주기적으로 energy 액션을 실행하는 스크립트 생성 및 실행
                from pathlib import Path
                import tempfile
                import json
                from pk_internal_tools.pk_functions.get_str_from_f import get_str_from_f
                from pk_internal_tools.pk_objects.pk_directories import d_pk_external_tools

                # monitor_script 템플릿 파일에서 읽어오기
                monitor_script_template_file = d_pk_external_tools / "p110m_monitor_script_template.py"
                monitor_script_template = get_str_from_f(f=str(monitor_script_template_file))

                if not monitor_script_template:
                    logging.error("monitor_script 템플릿 파일을 읽을 수 없습니다: %s", monitor_script_template_file)
                    return False

                # monitor_interval 값으로 치환
                monitor_script = monitor_script_template.format(monitor_interval=monitor_interval)

                # 임시 스크립트 파일 생성
                with tempfile.NamedTemporaryFile(
                        mode="w",
                        delete=False,
                        suffix=".py",
                        encoding="utf-8",
                ) as temp_f:
                    temp_script_path = temp_f.name
                    temp_f.write(monitor_script)

                try:
                    # Xavier에 스크립트 전송
                    remote_script_path = "/tmp/ensure_pk_p110m_monitor_on_xavier.py"
                    logging.info("모니터링 스크립트를 Xavier에 전송 중...")
                    ok = controller.ensure_file_transferred_to_target(
                        temp_script_path,
                        remote_script_path,
                    )

                    if not ok:
                        logging.error("스크립트 전송 실패")
                        return False

                    # Xavier에서 모니터링 스크립트 실행 (백그라운드)
                    logging.info("Xavier에서 P110M 에너지 모니터링을 시작합니다...")
                    cmd = f"nohup python3 {remote_script_path} > /tmp/p110m_monitor.log 2>&1 &"
                    stdout, stderr, exit_code = controller.ensure_command_to_wireless_target(
                        cmd=cmd,
                        timeout_seconds=10,
                        use_sudo=False,
                    )

                    if exit_code == 0:
                        logging.info("✅ P110M 에너지 모니터링이 Xavier에서 시작되었습니다.")
                        logging.info("모니터링 로그 확인: ssh로 Xavier 접속 후 'tail -f /tmp/p110m_monitor.log'")
                        logging.info("모니터링 중지: Xavier에서 'pkill -f ensure_pk_p110m_monitor_on_xavier.py'")
                    else:
                        logging.error("모니터링 시작 실패")
                        if stderr:
                            for line in stderr:
                                logging.error("  %s", line)
                        return False

                finally:
                    import os
                    if temp_script_path and os.path.exists(temp_script_path):
                        try:
                            os.remove(temp_script_path)
                        except Exception:
                            pass

            except Exception as e:
                logging.error(f"P110M 모니터링 작업 중 예외가 발생했습니다: {e}")
                ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=e)

        elif wireless_task == execute_pk_interesting_data_dashboard_and_control_sever_on_xavier:
            logging.info(f"'{execute_pk_interesting_data_dashboard_and_control_sever_on_xavier}' 작업을 시작합니다.")

            try:
                from pk_internal_tools.pk_functions.ensure_multi_data_pk_dashboard_server_started_on_xavier import (
                    ensure_multi_data_pk_dashboard_server_started_on_xavier,
                )

                # 포트 선택
                logging.info("멀티 데이터 대시보드 서버 포트를 선택하세요.")
                if QC_MODE:
                    port_str = ensure_value_completed(
                        key_name="multi_data_dashboard_port",
                        func_n=func_n,
                        options=["8000", "8080", "8888"],
                        guide_text="멀티 데이터 대시보드 서버 포트를 선택하세요:",
                        history_reset=history_reset
                    )
                else:
                    port_str = ensure_value_completed(
                        key_name="multi_data_dashboard_port",
                        func_n=func_n,
                        options=["8000", "8080", "8888"],
                        guide_text="멀티 데이터 대시보드 서버 포트를 선택하세요:",
                        history_reset=history_reset
                    )

                if not port_str:
                    logging.warning("포트가 선택되지 않아 기본값 8000을 사용합니다.")
                    port_str = "8000"

                port = int(port_str)

                # 기존 controller 재사용 또는 새로 생성
                if shared_controller is None:
                    logging.info("Xavier 연결 생성 중...")
                    shared_controller = PkWirelessTargetController(identifier=PkDevice.jetson_agx_xavier, setup_op=SetupOpsForPkWirelessTargetController.TARGET)
                    controller_initialized = True
                else:
                    logging.info("✅ 기존 Xavier 연결 재사용")

                controller = shared_controller
                xavier_ip = getattr(controller.wireless_target, "ip", None) or getattr(controller.wireless_target, "hostname", None)

                # 멀티 데이터 대시보드 서버 시작
                success = ensure_multi_data_pk_dashboard_server_started_on_xavier(
                    host="0.0.0.0",
                    port=port,
                    xavier_ip=xavier_ip,
                )

                if success:
                    logging.info("✅ 멀티 데이터 대시보드 서버가 Xavier에서 시작되었습니다.")
                    logging.info("📊 접속 URL: http://%s:%d", xavier_ip, port)
                    logging.info("서버 로그 확인: ssh로 Xavier 접속 후 'tail -f /tmp/multi_data_pk_dashboard_server.log'")
                    logging.info("서버 중지: Xavier에서 'pkill -f ensure_multi_data_pk_dashboard_server_on_xavier.py'")
                else:
                    logging.error("멀티 데이터 대시보드 서버 시작 실패")

            except Exception as e:
                logging.error(f"멀티 데이터 대시보드 서버 시작 작업 중 예외가 발생했습니다: {e}")
                ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=e)

        elif wireless_task == arduino_code_dev_env_on_xavier:
            logging.info(f"'{arduino_code_dev_env_on_xavier}' 작업을 시작합니다.")

            try:
                from pk_internal_tools.pk_functions.ensure_arduino_dev_environment_onboarded_on_xavier import (
                    ensure_arduino_dev_environment_onboarded_on_xavier,
                )

                # 기존 controller 재사용 또는 새로 생성
                if shared_controller is None:
                    logging.info("Xavier 연결 생성 중...")
                    shared_controller = PkWirelessTargetController(identifier=PkDevice.jetson_agx_xavier, setup_op=SetupOpsForPkWirelessTargetController.TARGET)
                    controller_initialized = True
                else:
                    logging.info("✅ 기존 Xavier 연결 재사용")

                controller = shared_controller
                xavier_ip = getattr(controller.wireless_target, "ip", None) or getattr(controller.wireless_target, "hostname", None)
                xavier_user = getattr(controller.wireless_target, "user_n", None) or "pk"
                xavier_pw = getattr(controller.wireless_target, "pw", None)

                # Arduino 개발 환경 온보딩
                success = ensure_arduino_dev_environment_onboarded_on_xavier(
                    xavier_ip=xavier_ip,
                    xavier_user=xavier_user,
                    xavier_pw=xavier_pw,
                )

                if success:
                    logging.info("✅ Arduino 개발 환경이 Xavier에 온보딩되었습니다.")
                    logging.info("다음 단계를 따라 VSCode Remote SSH로 연결하세요:")
                    logging.info("1. VSCode에서 F1 > 'Remote-SSH: Connect to Host'")
                    logging.info("2. '%s@%s' 입력", xavier_user, xavier_ip)
                    logging.info("3. 연결 후 PlatformIO 확장 설치")
                    logging.info("4. 프로젝트 디렉토리: ~/arduino_projects")
                else:
                    logging.error("Arduino 개발 환경 온보딩 실패")

            except Exception as e:
                logging.error(f"Arduino 개발 환경 온보딩 작업 중 예외가 발생했습니다: {e}")
                ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=e)

        elif wireless_task == control_tv_server_on_xavier:
            logging.info(f"'{control_tv_server_on_xavier}' 작업을 시작합니다.")

            try:
                # 기존 controller 재사용 또는 새로 생성
                if shared_controller is None:
                    logging.info("Xavier 연결 생성 중...")
                    shared_controller = PkWirelessTargetController(identifier=PkDevice.jetson_agx_xavier, setup_op=SetupOpsForPkWirelessTargetController.TARGET)
                    controller_initialized = True
                else:
                    logging.info("✅ 기존 Xavier 연결 재사용")

                controller = shared_controller

                logging.info("Home Assistant 준비 상태를 확인합니다...")
                if not ensure_home_assistant_ready_on_target(controller):
                    logging.error("Home Assistant 환경을 준비하지 못했습니다. 작업을 종료합니다.")
                    return
                logging.info("✅ Home Assistant 준비 완료")

                from pk_internal_tools.pk_functions.ensure_tv_controlled_via_ha_on_xavier import PkTvController

                logging.info("TV 제어 컨트롤러를 초기화합니다...")
                tv_manager = PkTvController(wireless_target_controller=controller)
                logging.info("✅ TV 제어 컨트롤러 초기화 완료")

                logging.info("TV에 수행할 액션을 사용자에게 요청합니다.")
                if QC_MODE:
                    tv_action = ensure_value_completed(
                        key_name="tv_api_action",
                        func_n=func_n,
                        options=["on", "off", "toggle"],
                        guide_text="TV 제어 액션을 선택하세요:",
                        history_reset=history_reset
                    )
                else:
                    tv_action = ensure_value_completed(
                        key_name="tv_api_action",
                        func_n=func_n,
                        options=["on", "off", "toggle"],
                        guide_text="TV 제어 액션을 선택하세요:",
                        history_reset=history_reset
                    )

                if not tv_action:
                    logging.warning("액션이 선택되지 않아 작업을 종료합니다.")
                    return

                # Get the entity_id from the user
                if QC_MODE:
                    entity_id = 'media_player.lg_tv'  # pk_option
                else:
                    entity_id = ensure_value_completed(
                        key_name="ha_tv_entity_id_for_api",
                        func_n=func_n,
                        guide_text="제어할 TV의 Entity ID를 입력하세요 (예: media_player.lg_tv):",
                        history_reset=history_reset
                    )

                if not entity_id:
                    logging.error("Entity ID가 입력되지 않아 작업을 종료합니다.")
                    return

                ha_token = None

                # 1. Check HA_TOKEN on the target environment first
                try:
                    stdout, _, exit_status = controller.ensure_command_to_wireless_target(
                        cmd="printenv HA_TOKEN",
                        timeout_seconds=10,
                        use_sudo=False,
                    )
                    if exit_status == 0 and stdout:
                        remote_token = stdout[0].strip()
                        if remote_token:
                            ha_token = remote_token
                            logging.info("타겟 장치 환경 변수 'HA_TOKEN'을 사용합니다.")
                except Exception as e:
                    logging.warning("타겟 장치에서 HA_TOKEN 확인 중 오류: %s", e)

                # 2. If not found on target, check local environment variables
                if not ha_token:
                    try:
                        from pk_internal_tools.pk_functions.get_env_var_name_id import get_env_var_id
                        from pk_internal_tools.pk_functions.ensure_pk_env_file_setup import (
                            ensure_pk_env_file_setup,
                        )
                        from dotenv import get_key

                        env_path = ensure_pk_env_file_setup()
                        env_var_id = get_env_var_id("HA_TOKEN", func_n)

                        try:
                            ha_token = get_key(env_path, env_var_id)
                            if ha_token:
                                logging.info("로컬 환경변수 파일에서 'HA_TOKEN'을 찾았습니다.")
                        except Exception:
                            ha_token = None
                    except Exception as e:
                        logging.debug("로컬 환경변수에서 HA_TOKEN 확인 중 오류: %s", e)

                # 3. If still not found, try to get token via helper function
                if not ha_token:
                    try:
                        from pk_internal_tools.pk_functions.ensure_ha_token_obtained import (
                            ensure_ha_token_obtained_via_fzf,
                        )
                        from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

                        # Get HA URL for token generation
                        xavier_ip = getattr(controller.wireless_target, "ip", None) or getattr(controller.wireless_target, "hostname", None)
                        ha_url = f"http://{xavier_ip}:8123" if xavier_ip else "http://localhost:8123"

                        # Try to get token via fzf helper
                        ha_token = ensure_ha_token_obtained_via_fzf(ha_url=ha_url)
                    except Exception as e:
                        logging.debug("ensure_ha_token_obtained_via_fzf 사용 중 오류: %s", e)
                        ha_token = None

                # 4. If still not found, ask user to input directly
                if not ha_token:
                    import getpass
                    logging.info("HA_TOKEN을 찾을 수 없습니다. Home Assistant Long-Lived Access Token을 입력하세요.")
                    logging.info("토큰 생성 방법: Home Assistant > 프로필 > Long-Lived Access Tokens > CREATE TOKEN")
                    ha_token = getpass.getpass("HA_TOKEN: ")

                    if not ha_token or not ha_token.strip():
                        logging.warning("HA_TOKEN이 입력되지 않아 작업을 종료합니다.")
                        return

                    ha_token = ha_token.strip()
                    logging.info("입력받은 HA_TOKEN을 사용합니다.")

                # Call the control method
                logging.info(f"TV 제어 실행: action={tv_action}, entity_id={entity_id}")
                success = tv_manager.ensure_tv_controlled_on_target(
                    action=tv_action,
                    entity_id=entity_id,
                    ha_token=ha_token
                )

                if success:
                    logging.info(f"Xavier를 통해 '{entity_id}'에 '{tv_action}' 액션을 성공적으로 요청했습니다.")
                else:
                    logging.error(f"Xavier를 통한 '{entity_id}' 제어에 실패했습니다.")
                    logging.error("TV 제어 실패 원인을 확인하세요:")
                    logging.error("  1. Home Assistant에 TV가 등록되어 있는지 확인")
                    logging.error("  2. Entity ID가 정확한지 확인")
                    logging.error("  3. HA_TOKEN이 올바른지 확인")
                    logging.error("  4. Xavier에서 Home Assistant 접속 가능한지 확인")
            except Exception as e:
                logging.error(f"TV 제어 작업 중 예외가 발생했습니다: {e}")
                ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=e)

        elif wireless_task == execute_api_server_on_xavier:
            logging.info(f"'{execute_api_server_on_xavier}' 작업을 시작합니다.")

            try:
                from pk_internal_tools.pk_functions.ensure_api_server_started_on_xavier import (
                    ensure_api_server_started_on_xavier,
                )

                # 포트 선택
                logging.info("API 서버 포트를 선택하세요.")
                if QC_MODE:
                    port_str = ensure_value_completed(
                        key_name="api_server_port",
                        func_n=func_n,
                        options=["8000", "8080", "8888"],
                        guide_text="API 서버 포트를 선택하세요:",
                        history_reset=history_reset
                    )
                else:
                    port_str = ensure_value_completed(
                        key_name="api_server_port",
                        func_n=func_n,
                        options=["8000", "8080", "8888"],
                        guide_text="API 서버 포트를 선택하세요:",
                        history_reset=history_reset
                    )

                if not port_str:
                    logging.warning("포트가 선택되지 않아 기본값 8000을 사용합니다.")
                    port_str = "8000"

                port = int(port_str)

                # 기존 controller 재사용 또는 새로 생성
                if shared_controller is None:
                    logging.info("Xavier 연결 생성 중...")
                    shared_controller = PkWirelessTargetController(identifier=PkDevice.jetson_agx_xavier, setup_op=SetupOpsForPkWirelessTargetController.TARGET)
                    controller_initialized = True
                else:
                    logging.info("✅ 기존 Xavier 연결 재사용")

                controller = shared_controller
                xavier_ip = getattr(controller.wireless_target, "ip", None) or getattr(controller.wireless_target, "hostname", None)

                # API 서버 시작
                success = ensure_api_server_started_on_xavier(
                    host="0.0.0.0",
                    port=port,
                    xavier_ip=xavier_ip,
                )

                if success:
                    logging.info("✅ API 서버가 Xavier에서 시작되었습니다.")
                    logging.info("🌐 접속 URL: http://%s:%d", xavier_ip, port)
                    logging.info("📋 API 문서: http://%s:%d/docs", xavier_ip, port)
                    logging.info("서버 로그 확인: ssh로 Xavier 접속 후 'tail -f /tmp/pk_api_server.log'")
                    logging.info("서버 중지: Xavier에서 'pkill -f pk_api_server.py'")
                else:
                    logging.error("API 서버 시작 실패")

            except Exception as e:
                logging.error(f"API 서버 시작 작업 중 예외가 발생했습니다: {e}")
                ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=e)

        elif wireless_task == execute_kiri_server_on_xavier:
            logging.info(f"'{execute_kiri_server_on_xavier}' 작업을 시작합니다.")

            try:
                from pk_internal_tools.pk_functions.ensure_kiri_server_started_on_xavier import (
                    ensure_kiri_server_started_on_xavier,
                )

                # 기존 controller 재사용 또는 새로 생성
                if shared_controller is None:
                    logging.info("Xavier 연결 생성 중...")
                    shared_controller = PkWirelessTargetController(identifier=PkDevice.jetson_agx_xavier, setup_op=SetupOpsForPkWirelessTargetController.TARGET)
                    controller_initialized = True
                else:
                    logging.info("✅ 기존 Xavier 연결 재사용")

                controller = shared_controller
                xavier_ip = getattr(controller.wireless_target, "ip", None) or getattr(controller.wireless_target, "hostname", None)
                xavier_user = getattr(controller.wireless_target, "user_n", None) or "pk"
                xavier_pw = getattr(controller.wireless_target, "pw", None)

                # 마이크 확인 건너뛰기 옵션
                skip_mic_check = False
                if QC_MODE:
                    skip_mic_check_response = ensure_value_completed(
                        key_name="skip_mic_check",
                        func_n=func_n,
                        options=["no", "yes"],
                        guide_text="마이크 확인을 건너뛰시겠습니까? (yes/no):",
                        history_reset=history_reset
                    )
                    skip_mic_check = (skip_mic_check_response == "yes")
                else:
                    skip_mic_check_response = ensure_value_completed(
                        key_name="skip_mic_check",
                        func_n=func_n,
                        options=["no", "yes"],
                        guide_text="마이크 확인을 건너뛰시겠습니까? (yes/no):",
                        history_reset=history_reset
                    )
                    skip_mic_check = (skip_mic_check_response == "yes")

                # kiri 서버 시작
                success = ensure_kiri_server_started_on_xavier(
                    xavier_ip=xavier_ip,
                    xavier_user=xavier_user,
                    xavier_pw=xavier_pw,
                    skip_mic_check=skip_mic_check,
                )

                if success:
                    logging.info("✅ kiri 서버가 Xavier에서 시작되었습니다.")
                    logging.info("음성인식 기반 제어를 사용할 수 있습니다.")
                    logging.info("서버 로그 확인: ssh로 Xavier 접속 후 'tail -f /tmp/kiri_server.log'")
                    logging.info("서버 중지: Xavier에서 'pkill -f ensure_kiri_server_on_xavier.py'")
                else:
                    logging.error("kiri 서버 시작 실패")

            except Exception as e:
                logging.error(f"kiri 서버 시작 작업 중 예외가 발생했습니다: {e}")
                ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=e)

        elif wireless_task == develop_arduino_code_on_xavier:
            logging.info(f"'{develop_arduino_code_on_xavier}' 작업을 시작합니다.")

            try:
                from pk_internal_tools.pk_functions.ensure_development_code_uploaded_from_xavier_to_arduino_wireless import (
                    ensure_development_code_uploaded_from_xavier_to_arduino_wireless,
                )

                # 기존 controller 재사용 또는 새로 생성
                if shared_controller is None:
                    logging.info("Xavier 연결 생성 중...")
                    shared_controller = PkWirelessTargetController(identifier=PkDevice.jetson_agx_xavier, setup_op=SetupOpsForPkWirelessTargetController.TARGET)
                    controller_initialized = True
                else:
                    logging.info("✅ 기존 Xavier 연결 재사용")

                controller = shared_controller
                xavier_ip = getattr(controller.wireless_target, "ip", None) or getattr(controller.wireless_target, "hostname", None)
                xavier_user = getattr(controller.wireless_target, "user_n", None) or "pk"
                xavier_pw = getattr(controller.wireless_target, "pw", None)

                # Wireless 코드 업로드
                success = ensure_development_code_uploaded_from_xavier_to_arduino_wireless(
                    xavier_ip=xavier_ip,
                    xavier_user=xavier_user,
                    xavier_pw=xavier_pw,
                    esp8266_ip=None,  # 사용자 입력받기
                    project_path=None,  # 사용자 입력받기
                    ota_password=None,  # 사용자 입력받기
                )

                if success:
                    logging.info("✅ Wireless 코드 업로드 완료")
                else:
                    logging.error("Wireless 코드 업로드 실패")

            except Exception as e:
                logging.error(f"Wireless 코드 업로드 작업 중 예외가 발생했습니다: {e}")
                ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=e)

        elif wireless_task == develop_arduino_ota_environment_on_xavier:
            logging.info(f"'{develop_arduino_ota_environment_on_xavier}' 작업을 시작합니다.")

            try:
                from pk_internal_tools.pk_functions.ensure_arduino_ota_development_environment_on_xavier import (
                    ensure_arduino_ota_development_environment_on_xavier,
                )

                # 기존 controller 재사용 또는 새로 생성
                if shared_controller is None:
                    logging.info("Xavier 연결 생성 중...")
                    shared_controller = PkWirelessTargetController(identifier=PkDevice.jetson_agx_xavier, setup_op=SetupOpsForPkWirelessTargetController.TARGET)
                    controller_initialized = True
                else:
                    logging.info("✅ 기존 Xavier 연결 재사용")

                controller = shared_controller
                xavier_ip = getattr(controller.wireless_target, "ip", None) or getattr(controller.wireless_target, "hostname", None)
                xavier_user = getattr(controller.wireless_target, "user_n", None) or "pk"
                xavier_pw = getattr(controller.wireless_target, "pw", None)

                # Arduino OTA 개발 환경 설정
                success = ensure_arduino_ota_development_environment_on_xavier(
                    xavier_ip=xavier_ip,
                    xavier_user=xavier_user,
                    xavier_pw=xavier_pw,
                    esp8266_ip=None,  # 사용자 입력받기
                    esp32_ip=None,  # 사용자 입력받기
                    ota_password=None,  # 사용자 입력받기
                )

                if success:
                    logging.info("✅ Arduino OTA 개발 환경 설정 완료")
                    logging.info("다음 단계:")
                    logging.info("1. 'install OTA uploader agent on Arduino' 작업 실행 (wired 액션)")
                    logging.info("2. OTA 프로젝트 생성 및 업로드")
                else:
                    logging.error("Arduino OTA 개발 환경 설정 실패")

            except Exception as e:
                logging.error(f"Arduino OTA 개발 환경 설정 작업 중 예외가 발생했습니다: {e}")
                ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=e)

        elif wireless_task == control_wireless_target_via_chrome_remote_desktop_on_host:
            logging.info(f"'{control_wireless_target_via_chrome_remote_desktop_on_host}' 작업을 시작합니다.")

            try:
                from pk_internal_tools.pk_functions.ensure_remote_pc_controllable_via_chrome_remote_desktop import (
                    ensure_remote_pc_controllable_via_chrome_remote_desktop,
                )

                # Chrome Remote Desktop을 통해 무선 타겟 제어
                ensure_remote_pc_controllable_via_chrome_remote_desktop()

                logging.info("✅ Chrome Remote Desktop을 통해 무선 타겟 제어를 시작했습니다.")

            except Exception as e:
                logging.error(f"Chrome Remote Desktop을 통한 무선 타겟 제어 작업 중 예외가 발생했습니다: {e}")
                ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=e)

        else:
            logging.warning(f"알 수 없는 작업이 선택되었습니다: {wireless_task}")

        logging.info(PK_UNDERLINE)
        logging.info(f"{PK_ANSI_COLOR_MAP['BRIGHT_CYAN']}무선 타겟 컨트롤러 실행 종료{PK_ANSI_COLOR_MAP['RESET']}")
        logging.info(PK_UNDERLINE)
        return True
    except:
        ensure_debug_loged_verbose(traceback)
    finally:
        pass
