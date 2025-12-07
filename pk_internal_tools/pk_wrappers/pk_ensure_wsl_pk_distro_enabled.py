if __name__ == "__main__":

    import traceback
    from pk_internal_tools.pk_functions.ensure_pk_colorama_initialized_once import ensure_pk_colorama_initialized_once
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_wsl_pk_distro_enabled import ensure_wsl_pk_distro_enabled
    from pk_internal_tools.pk_objects.pk_directories  import d_pk_root
    

    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:

        if not ensure_wsl_pk_distro_enabled():
            raise RuntimeError("WSL 배포판 설치/이름 변경에 실패했습니다.")
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
