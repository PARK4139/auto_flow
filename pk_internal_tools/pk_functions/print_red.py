

from pk_internal_tools.pk_functions.print_text_via_colorama import print_text_via_colorama


def print_red(text, flush=True, line_feed_mode=1):
    print_text_via_colorama(text, 'RED', flush, line_feed_mode)
