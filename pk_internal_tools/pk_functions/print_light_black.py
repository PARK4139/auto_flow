def print_light_black(prompt, flush=True, line_feed_mode=1):
    from pk_internal_tools.pk_functions.print_text_via_colorama import print_text_via_colorama
    print_text_via_colorama(prompt, 'BRIGHT_BLACK', flush, line_feed_mode)
