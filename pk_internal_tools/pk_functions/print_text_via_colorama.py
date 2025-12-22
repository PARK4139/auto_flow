from enum import Enum


def print_text_via_colorama(text: str, colorama_code: str, flush, line_feed_mode=1):
    from pk_internal_tools.pk_objects.pk_colors import PkColors

    color_code = getattr(PkColors, colorama_code.upper(), PkColors.RESET)
    end_char = '' if line_feed_mode == 0 else '\n'
    print(f"{color_code}{text}", end=end_char, flush=flush)
