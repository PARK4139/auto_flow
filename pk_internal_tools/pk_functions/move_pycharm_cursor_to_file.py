def move_pycharm_cursor_to_file(__file__):
    import logging
    import logging
    import os
    from pk_internal_tools.pk_functions.ensure_text_saved_to_clipboard import ensure_text_saved_to_clipboard

    from pk_internal_tools.pk_functions.open_pycharm_parrete import open_pycharm_parrete_like_human
    from pk_internal_tools.pk_functions.paste_and_enter import paste_and_enter_like_human
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    file_name_to_dst = os.path.basename(__file__)
    ensure_text_saved_to_clipboard(file_name_to_dst)
    ensure_slept(100)
    open_pycharm_parrete_like_human()
    ensure_slept(500)
    paste_and_enter_like_human()
    logging.debug(f"[{PkTexts.MOVED}] {file_name_to_dst}")
