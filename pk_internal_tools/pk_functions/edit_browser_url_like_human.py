def edit_browser_url_like_human():
    import random
    from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_typed import ensure_typed

    ensure_pressed("ctrl", "l")
    ensure_pressed("right")
    ensure_typed("/")
    ensure_slept(milliseconds=random.randint(a=12, b=23))
