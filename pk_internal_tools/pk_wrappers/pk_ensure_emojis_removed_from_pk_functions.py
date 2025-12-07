if __name__ == "__main__":
    from pk_internal_tools.pk_functions.ensure_emojis_removed_from_pk_functions import ensure_emojis_removed_from_pk_functions
    import logging
    from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_window_title_replaced import ensure_pk_wrapper_starter_window_title_replaced

    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.ensure_pk_colorama_initialized_once import ensure_pk_colorama_initialized_once
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    import traceback

    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        ensure_window_title_replaced(get_nx(__file__))
        
        logging.debug("pk_functions 폴더에서 이모지 제거 작업을 시작합니다...")
        
        # 실제 이모지 제거 함수 호출
        ensure_emojis_removed_from_pk_functions()
        
        logging.debug("이모지 제거 작업이 완료되었습니다.")
        
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)