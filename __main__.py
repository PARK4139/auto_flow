try:
    import sys
    import traceback
    from af_internal_tools.functions.execute_auto_flow import ensure_custom_cli_started
    from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
    from pk_internal_tools.pk_functions.ensure_pk_log_initialized import ensure_pk_log_initialized
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_executed import ensure_pk_wrapper_starter_executed
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
except ImportError as e:
    print(f"오류: pk_system 모듈을 가져오는 데 실패했습니다. 경로 설정을 확인해주세요.")
    print(f"sys.path: {sys.path}")
    traceback.print_exc()

if __name__ == '__main__':
    try:
        ensure_pk_log_initialized(__file__)
        func_n = get_caller_name()
        auto_flow_mode = "auto_flow_mode",
        pk_mode = "pk_mode",

        if QC_MODE:
            wrapper_mode = ensure_value_completed(
                key_name='wrapper_mode',
                func_n=func_n,
                options=[
                    auto_flow_mode,
                    pk_mode,
                ],
            )
        else:
            wrapper_mode = auto_flow_mode

        if wrapper_mode == auto_flow_mode:
            while True:
                ensure_custom_cli_started()
                ensure_slept(milliseconds=50)
        else:
            while True:
                ensure_pk_wrapper_starter_executed()
                ensure_slept(milliseconds=50)
    except KeyboardInterrupt:
        print("업무자동화 래퍼가 사용자에 의해 중지되었습니다.")
    except Exception:
        ensure_debug_loged_verbose(traceback)
        print("오류가 발생했습니다. 로그 파일을 확인해주세요.")
