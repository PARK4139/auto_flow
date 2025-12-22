
if __name__ == '__main__':
    import traceback

    from pk_internal_tools.pk_functions.ensure_pk_wrapper_exception_routine_done import ensure_pk_wrapper_exception_routine_done
    from pk_internal_tools.pk_functions.kill_us_ime_keyboard import kill_us_ime_keyboard

    try:
        kill_us_ime_keyboard()
    except Exception as e:
        ensure_pk_wrapper_exception_routine_done(traced_file=__file__, traceback=traceback, e=e)
