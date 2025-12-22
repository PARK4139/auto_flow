


def paste_and_enter_like_human():
    from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    ensure_pressed("ctrl+v")
    ensure_slept(200)
    ensure_pressed("enter")
    # ensure_slept(500)


