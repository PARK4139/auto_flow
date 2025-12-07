from pk_internal_tools.pk_functions.ensure_pk_log_editable import ensure_pk_log_editable
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_routine_startup_enabled():
    from pk_internal_tools.pk_functions.ensure_guided_not_prepared_yet import ensure_not_prepared_yet_guided
    from pk_internal_tools.pk_functions.is_host_pk_asus import is_host_pk_asus
    from pk_internal_tools.pk_functions.is_host_pk_renova import is_host_pk_renova
    from pk_internal_tools.pk_functions.ensure_chatgpt_opened import ensure_chatgpt_opened
    from pk_internal_tools.pk_functions.ensure_cursor_enabled import ensure_cursor_enabled
    from pk_internal_tools.pk_functions.ensure_pk_repo_editable import ensure_pk_repo_editable
    from pk_internal_tools.pk_functions.ensure_pycharm_opened import ensure_pycharm_opened
    from pk_internal_tools.pk_functions.ensure_remote_pc_controllable_via_chrome_remote_desktop import ensure_remote_pc_controllable_via_chrome_remote_desktop
    from pk_internal_tools.pk_functions.ensure_vscode_enabled import ensure_vscode_enabled
    from pk_internal_tools.pk_functions.ensure_windows_minimized import ensure_windows_minimized

    if is_host_pk_renova():
        ensure_pk_repo_editable(__file__, repo_to_edit)
        ensure_remote_pc_controllable_via_chrome_remote_desktop()

    elif is_host_pk_asus():
        ensure_pk_repo_editable(__file__, repo_to_edit)
        ensure_pk_log_editable()

        ensure_cursor_enabled()
        ensure_vscode_enabled()
        ensure_chatgpt_opened()
        # ensure_chrome_opened()
        ensure_pycharm_opened()
        # ensure_slept(milliseconds=77)

        # ensure_pk_flow_executed_py_as_not_child_process()  # ensure_routine_startup_enabled() 내에서 pk_flow_assistance 실행 금지, circuler calling
        # ensure_pk_log_editable()
        # ensure_gemini_cli_executed()
        ensure_windows_minimized()
        # ensure_pk_wrapper_starter_executed_py_as_not_child_process()  # TODO : pk_system 을 백그라운드에서 단축키를 탐지하여 열도록 수정. 더 빨리 동작하게 하기 위함.

        # TODO ensure_process_control
        #   process수집 monitor and kill, play 기능
        #   등록된 프로세스이면서 죽은 프로세스는 색상이 회색으로 프로세스명 표현.
        #   등록된 프로세스이면서 살아있는 프로세스는 색상을 그린으로  프로세스명 표현.
        #   process를 번호 선택 옵션 -> selected -> kill 기능
        #   불필요한 프로그램 조사해서 여기에 등록하여 관리.
    else:
        ensure_not_prepared_yet_guided()
