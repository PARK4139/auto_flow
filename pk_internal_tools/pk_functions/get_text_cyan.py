
def get_text_cyan(text):
    from pk_internal_tools.pk_objects.pk_colors import PkColors
    cyan_text = f"{PkColors.CYAN}{text}{PkColors.RESET}"
    return cyan_text
