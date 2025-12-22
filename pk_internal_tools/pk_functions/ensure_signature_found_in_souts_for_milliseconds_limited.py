# @ensure_seconds_measured
def ensure_signature_found_in_souts_for_milliseconds_limited(cmd: str, signature: str, milliseconds_limited, encoding='utf-8'):
    import logging
    import time
    import traceback

    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose

    try:
        time_s = time.time()
        is_found = False
        while True:
            if is_found:
                break
            sout, _ = ensure_command_executed(cmd=cmd, encoding=encoding)
            lines = sout
            for line in lines:
                if signature in line:
                    is_found = True
                    continue
            ensure_slept(milliseconds=77)
            if (time.time() - time_s) * 1000 > milliseconds_limited:
                logging.warning(f'Timed out after {milliseconds_limited} milliseconds')
                return False
        if is_found:
            return True

    except Exception as e:
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
