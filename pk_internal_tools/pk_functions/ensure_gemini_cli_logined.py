from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


# @ensure_seconds_measured
def ensure_gemini_cli_logined():
    try:
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

        from pk_internal_tools.pk_functions.ensure_mouse_clicked_by_coordination_history import ensure_mouse_clicked_by_coordination_history
        from pk_internal_tools.pk_functions.ensure_slept_by_following_history import ensure_slept_by_following_history
        from pk_internal_tools.pk_functions.is_pc_remote_controlled_by_renova import is_pc_remote_controlled_by_renova

        history_reset = True
        history_reset_renova = False

        func_n = get_caller_name()

        if is_pc_remote_controlled_by_renova():
            key_name = "사용자 후보계정 사용 for renova"
            ensure_mouse_clicked_by_coordination_history(key_name=key_name, func_n=func_n, history_reset=history_reset_renova)
        else:
            key_name = "사용자 후보계정 사용"
            ensure_mouse_clicked_by_coordination_history(key_name=key_name, func_n=func_n, history_reset=history_reset)
        ensure_slept_by_following_history(key_name=key_name, func_n=func_n, history_reset=history_reset)

        if is_pc_remote_controlled_by_renova():
            key_name = "로그인 for renova"
            ensure_mouse_clicked_by_coordination_history(key_name=key_name, func_n=func_n, history_reset=history_reset_renova)
        else:
            key_name = "로그인"
            ensure_mouse_clicked_by_coordination_history(key_name=key_name, func_n=func_n, history_reset=history_reset)
        return True
    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
