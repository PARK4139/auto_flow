def get_text_blue(text: str) -> str:
    from pk_internal_tools.pk_objects.pk_colors import PkColors
    blue_text = f"{PkColors.BLUE}{text}{PkColors.RESET}"
    return blue_text
