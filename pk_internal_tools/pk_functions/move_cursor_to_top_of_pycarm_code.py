

def move_cursor_to_top_of_pycarm_code_like_human():
    from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed

    ensure_pressed("ctrl", "home")
    ensure_pressed("ctrl", "pgdn")
    ensure_pressed("ctrl", "end")
    ensure_pressed("ctrl", "home")


