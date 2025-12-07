
def get_text_cyan(text):
    from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
    cyan_text = f"{PK_ANSI_COLOR_MAP['CYAN']}{text}{PK_ANSI_COLOR_MAP['RESET']}"
    return cyan_text
