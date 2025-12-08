# 내부 레포에서 사용: pk_system.pk_internal_tools import
# 외부 레포에서 사용: pk_system.pk_internal_tools import (패키지 설치 후)
import logging

try:
    # 외부 레포: 패키지로 설치된 경우
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
    from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
    from pk_internal_tools.pk_functions.ensure_env_var_completed_2025_11_24 import ensure_env_var_completed_2025_11_24
    from pk_internal_tools.pk_functions.ensure_pk_log_initialized import ensure_pk_log_initialized
    from pk_internal_tools.pk_functions.ensure_window_resized_and_positioned_left_half import ensure_window_resized_and_positioned_left_half
    from pk_internal_tools.pk_functions.ensure_window_to_front import ensure_window_to_front
    from pk_internal_tools.pk_functions.ensure_windows_deduplicated import ensure_windows_deduplicated
    from pk_internal_tools.pk_functions.ensure_windows_killed_like_human_by_window_title import ensure_windows_killed_like_human_by_window_title
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_functions.get_current_console_title import get_current_console_title
    from pk_internal_tools.pk_functions.get_gemini_installer_title import get_gemini_installer_title
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.get_project_name import get_project_name
    from pk_internal_tools.pk_functions.get_window_title_temp import get_window_title_temp
    from pk_internal_tools.pk_functions.get_window_title_temp_for_cmd_exe import get_window_title_temp_for_cmd_exe
    from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
    from pk_internal_tools.pk_objects.pk_operation_options import SetupOpsForPkEnsurePkSystemStarted
    from pk_internal_tools.pk_functions.ensure_pk_colorama_initialized_once import ensure_pk_colorama_initialized_once
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_started import ensure_pk_wrapper_started
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_suicided import ensure_pk_wrapper_suicided
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_window_title_replaced import ensure_pk_wrapper_window_title_replaced
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
except ImportError:
    logging.error("pk_import_error")


def _move_window_right_side():
    # import는 파일 상단에서 이미 처리됨
    ensure_pressed("win", "left")
    ensure_pressed("win", "right")


if __name__ == '__main__':
    try:
        # src-layout 전환 후 간소화된 초기화
        is_already_started = False
        filename = get_nx(__file__)

        # src-layout 주의: __file__은 src/pk_system/pk_internal_tools/pk_wrappers/xxx.py
        # filename은 "pk_ensure_pk_wrapper_started.py"

        # 디버깅을 위해 QC_MODE 모드 비활성화 (임시)
        if QC_MODE:
            # mode = SetupOpsForPkEnsurePkSystemStarted.AS_FAST_MODE
            mode = SetupOpsForPkEnsurePkSystemStarted.AS_CONVENIENCE_MODE

            if is_window_opened(window_title_seg=filename):
                ensure_window_to_front(window_title_seg=filename)  # 기존 사용 -> venv 활성화 시간초기 1회 -> uv python 실행초기 1회로 제한
                # _move_window_right_side()

            func_n = get_caller_name()
            if mode == SetupOpsForPkEnsurePkSystemStarted.AS_CONVENIENCE_MODE:

                if is_window_opened(window_title_seg=filename):
                    ensure_pk_wrapper_suicided(get_current_console_title())  # -> 인스턴스 1개만 유지 -> 속도개선 필요 시 -> 코드주석 -> 속도 개선기대 가능

                ensure_pk_log_initialized(__file__)  # code for pk_ensure_pk_wrapper_started.py debugging, should be annotated for operation mode
                ensure_pk_colorama_initialized_once()
                # ensure_pressed("f11") # -> window title 안보임 -> 창 식별불가
                ensure_window_resized_and_positioned_left_half()
                # ensure_pressed("esc")

                # ensure_windows_deduplicated()  # TODO 개선여지 있어보임.

                # pk_* -> ensure_windows_killed_like_human_by_window_title #위험한 코드 유의하여 사용
                key_name = 'USERNAME'
                USERNAME = ensure_env_var_completed_2025_11_24(key_name=key_name, func_n=func_n)
                USERNAME = USERNAME.strip()
                windows_useless = [
                    rf"cmd",
                    rf"cmd.exe",
                    rf"C:\WINDOWS\system32\cmd.exe",
                    "pk_launcher (3)",
                    rf"pk@pk: /mnt/c/Users/{USERNAME}/Downloads/pk_system",
                    rf"pk@pk: /mnt/c/Users/{USERNAME} ",
                    rf"pk@pk: /mnt/c/Users/{USERNAME}",
                    get_window_title_temp(),
                    get_window_title_temp_for_cmd_exe(),
                    get_gemini_installer_title(),
                    # get_current_console_title(), # -> 인스턴스 1개만 유지
                ]
                for window_useless in windows_useless:
                    ensure_windows_killed_like_human_by_window_title(window_title=window_useless)
                ensure_pk_wrapper_window_title_replaced(__file__)

            elif mode == SetupOpsForPkEnsurePkSystemStarted.AS_FAST_MODE:
                ensure_pk_wrapper_window_title_replaced(__file__)

            _move_window_right_side()
        else:
            # src-layout 전환 후: window title 관련 문제 방지를 위해 임시 비활성화
            # project_name = get_project_name()
            # ensure_pk_wrapper_suicided(project_name)
            # ensure_pk_wrapper_window_title_replaced(project_name)
            pass

        # ensure_pk_wrapper_started()  # -> slow # 개선목표 :  venv 활성화 시간, start/cmd/uv python 실행시간  감소 (원인분석결과 시간성능저하 주원인)
        # TODO : hotreloader 로 ensure_pk_wrapper_started() 를 계속 띄우면 어떤가?
        while 1:
            ensure_pk_wrapper_started()
            # ensure_slept(seconds=1)
            # ensure_slept(milliseconds=22)
            ensure_slept(milliseconds=2)
        #  TODO : skim/fzy 으로 포팅 후 성능비교
        #  TODO : python3.14 이상으로 마이그레이션 후 성능비교
    except Exception as e:
        import traceback
        from pk_internal_tools.pk_functions.ensure_console_paused import ensure_console_paused

        # 프로젝트 규칙에 따라 ensure_debug_loged_verbose 사용
        # traceback 모듈 객체를 전달 (함수 내부에서 traceback.format_exc() 호출)
        ensure_debug_loged_verbose(traceback)

        # 사용자 입력 대기 (콘솔이 바로 닫히지 않도록)
        # 프로젝트 규칙에 따라 ensure_console_paused 사용
        ensure_console_paused("계속하려면 Enter를 누르세요...")
