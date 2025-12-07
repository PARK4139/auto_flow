if __name__ == "__main__":
    import logging
    import traceback

    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
    from pk_internal_tools.pk_functions.ensure_pk_wrappers_killed import ensure_pk_wrappers_killed
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.set_pk_language import set_pk_language
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        # 언어 변경 (사용자에게 선택 요청)
        lang = set_pk_language(language=None)
        ensure_spoken(f"언어가 {lang}로 변경되었습니다" if lang == "korean" else f"Language changed to {lang}")
        logging.debug(f"language changed to: {lang}")
        ensure_spoken(f'', wait=True)
        ensure_pk_wrapper_starter_suicided(__file__)

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)







