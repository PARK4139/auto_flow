if __name__ == "__main__":
    try:
        from pk_internal_tools.pk_functions.ensure_lta_from_pk_qc_mode_toml_toggled import ensure_lta_from_pk_qc_mode_toml_toggled
        from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
        from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
        from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
        from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
        from pk_internal_tools.pk_functions.ensure_pk_colorama_initialized_once import ensure_pk_colorama_initialized_once
        from pk_internal_tools.pk_objects.pk_directories import d_pk_root

        import traceback
        from colorama import init as pk_colorama_init

        ensure_pk_colorama_initialized_once()
        ensure_lta_from_pk_qc_mode_toml_toggled()

        
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        # QC_MODE 토글은 단순 설정 변경이므로 console_log_block_mode=False로 설정
        # 창이 닫히지 않도록 함
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root, console_log_block_mode=False)
