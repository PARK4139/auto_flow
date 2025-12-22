"""
pk_system wrapper 자동 설정 wrapper

이 wrapper는 pk_system wrapper를 자동으로 생성하고 설정합니다.
Win + 1 키로 빠르게 실행할 수 있도록 바로가기를 생성하고 작업표시줄에 고정합니다.
"""

if __name__ == "__main__":

    try:
        import traceback

        from pk_internal_tools.pk_functions.ensure_finally_routine_done import (
            ensure_finally_routine_done
        )
        from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import (
            ensure_pk_starting_routine_done
        )
        from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_shortcut_setup import ensure_pk_wrapper_starter_shortcut_setup
        from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT
        from pk_internal_tools.pk_functions.ensure_pk_wrapper_exception_routine_done import ensure_pk_wrapper_exception_routine_done

        ensure_pk_wrapper_starting_routine_done(traced_file=__file__, traceback=traceback)

        ensure_pk_wrapper_starter_shortcut_setup(
            create_shortcut=True,
            run_powershell_script=True,
            verbose=True
        )
    except Exception as e:
        ensure_pk_wrapper_exception_routine_done(traced_file=__file__, traceback=traceback, e=e)
    finally:
        ensure_pk_wrapper_finally_routine_done(traced_file=__file__, project_root_directory=D_PK_ROOT)
