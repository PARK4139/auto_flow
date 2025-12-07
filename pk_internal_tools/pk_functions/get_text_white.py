
def get_text_white(text):
    from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
    white_text = f"{PK_ANSI_COLOR_MAP['WHITE']}{text}{PK_ANSI_COLOR_MAP['RESET']}"
    return white_text
