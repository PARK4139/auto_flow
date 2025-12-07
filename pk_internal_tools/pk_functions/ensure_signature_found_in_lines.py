from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_signature_found_in_lines(signature: str, lines, milliseconds_limited=5):
    import time
    import traceback

    import logging

    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose

    try:
        time_s = time.time()
        is_found = False
        while True:
            if is_found:
                break
            for line in lines:
                if signature in line:
                    is_found = True
                    continue
            ensure_slept(milliseconds=77)
            if time.time() - time_s > milliseconds_limited:
                logging.warning(f'Timed out after {milliseconds_limited} milliseconds')
                return False
        if is_found:
            return True

    except:
        ensure_debug_loged_verbose(traceback)
    finally:
        pass
