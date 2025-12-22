from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_condition_choosen(is_condition, positive_return, negative_return):
    # TODO : 검증
    try:
        if is_condition:
            return positive_return
        else:
            return negative_return
    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
