def ensure_console_debuggable(ipdb=None):
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept

    if ipdb is None:
        ensure_slept(hours=1, mode_countdown=0)  # pk_option
    else:
        ipdb.set_trace()  # pk_option # pk_fail
