from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pk_p110m_off():
    """
        TODO: Write docstring for ensure_pk_p110m_off.
    """
    try:
        import logging
        import traceback
        from pk_internal_tools.pk_functions.ensure_paused import ensure_paused
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        from pk_internal_tools.pk_functions.ensure_remote_target_terminal_opened_via_ssh_like_person import ensure_remote_target_terminal_opened_via_ssh_like_person
        from pk_internal_tools.pk_functions.ensure_pk_p110m_controlled_via_tapo_library import (
            ensure_pk_p110m_controlled_via_tapo_library,
        )
        from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured

        from pk_internal_tools.pk_functions.ensure_pk_wrapper_exception_routine_done import ensure_pk_wrapper_exception_routine_done
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        from pk_internal_tools.pk_objects.pk_colors import PkColors
        from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE
        from pk_internal_tools.pk_objects.pk_modes import PkModesForDemo
        from pk_internal_tools.pk_objects.pk_remote_target_controller import PkRemoteTargetEngine
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
        logging.info(f"{PkColors.BRIGHT_CYAN}무선 타겟 컨트롤러 실행 시작{PkColors.RESET}")
        logging.info(PK_UNDERLINE)

        # Xavier controller를 한 번만 생성하여 재사용 (같은 세션 내에서)
        shared_controller = None
        controller_initialized = False

        # n. 무선 작업 목록 정의
        control_p110m_via_tapo_library_on_remote_target = "CONTROL P110M VIA TAPO LIBRARY ON XAVIER"
        history_reset = True
        remote_task = control_p110m_via_tapo_library_on_remote_target
        try:

            # 액션 선택
            logging.info("스마트 플러그에 수행할 액션을 사용자에게 요청합니다.")
            if QC_MODE:
                p110m_action = "off" # "on", "off", "toggle", "info"
            else:
                p110m_action = "off"

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
            ensure_pk_wrapper_exception_routine_done(traced_file=__file__, traceback=traceback, e=e)


        else:
            logging.warning(f"알 수 없는 작업이 선택되었습니다: {remote_task}")

        logging.info(PK_UNDERLINE)
        logging.info(f"{PkColors.BRIGHT_CYAN}무선 타겟 컨트롤러 실행 종료{PkColors.RESET}")
        logging.info(PK_UNDERLINE)
        return True

        return True
    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
