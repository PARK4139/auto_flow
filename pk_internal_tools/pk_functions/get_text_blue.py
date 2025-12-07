def get_text_blue(text: str) -> str:
    from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
    blue_text = f"{PK_ANSI_COLOR_MAP["BLUE"]}{text}{PK_ANSI_COLOR_MAP["RESET"]}"
    return blue_text
