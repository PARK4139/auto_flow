from enum import Enum


def print_text_via_colorama(text: str, colorama_code: str, flush, line_feed_mode=1):
    from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP

    color_code = PK_ANSI_COLOR_MAP.get(colorama_code, PK_ANSI_COLOR_MAP['RESET'])
    end_char = '' if line_feed_mode == 0 else '\n'
    print(f"{color_code}{text}", end=end_char, flush=flush)
