def get_text_yellow(text: str) -> str:
    from pk_internal_tools.pk_objects.pk_colors import PkColors
    yellow_text = f"{PkColors.YELLOW}{text}{PkColors.RESET}"
    return yellow_text
