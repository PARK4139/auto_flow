def close_pycharm_tab_like_human \
                ():
    from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    ensure_pressed("ctrl", "f4")
    ensure_slept(100)
