if __name__ == "__main__":
    import traceback

    from pk_internal_tools.pk_functions.ensure_pk_colorama_initialized_once import ensure_pk_colorama_initialized_once
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_process_killed_by_pid import ensure_process_killed_by_pid
    from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_window_title_replaced import ensure_pk_wrapper_starter_window_title_replaced

    from pk_internal_tools.pk_functions.get_file_id import get_file_id
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.get_values_from_historical_file_routine import get_values_from_historical_file_routine
    from pk_internal_tools.pk_objects.pk_directories  import d_pk_root


    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        ensure_window_title_replaced(get_nx(__file__))

        # 파일명에서 함수명 추출
        import os

        file_name = os.path.basename(__file__)
        func_n = file_name.replace('.py', '')

        key_name = "pid"
        pid = get_values_from_historical_file_routine(
            file_id=get_file_id(key_name, func_n),
            key_hint=f'{key_name}=',
            options=[],
            editable=True
        )

        # PID를 정수로 변환
        try:
            pid = int(pid)
            ensure_process_killed_by_pid(pid=pid)
        except ValueError:
            print(f"❌ 유효하지 않은 PID입니다: {pid}")

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
        import traceback
