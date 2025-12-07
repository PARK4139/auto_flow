def get_text_yellow(text: str) -> str:
    from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
    yellow_text = f"{PK_ANSI_COLOR_MAP["YELLOW"]}{text}{PK_ANSI_COLOR_MAP["RESET"]}"
    return yellow_text
