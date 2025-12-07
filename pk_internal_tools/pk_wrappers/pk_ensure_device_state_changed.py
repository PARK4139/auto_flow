

if __name__ == "__main__":
    from pk_internal_tools.pk_functions.ensure_console_cleared import ensure_console_cleared
    import logging
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    import keyboard
    logging.debug(f'''detect hotkey %%%FOO%%%''')
    while 1:
        ensure_console_cleared()
        if keyboard.is_pressed('ctrl') and keyboard.is_pressed('alt') and keyboard.is_pressed('`'):
            logging.debug("ctrl + alt + 1 pressed")
            continue
        if keyboard.is_pressed('alt') and keyboard.is_pressed('1'):
            logging.debug("alt + 1 pressed")
            continue
        if keyboard.is_pressed('esc'):
            logging.debug("esc pressed")
        ensure_slept(milliseconds=100)
        # ensure_slept(milliseconds=10)
