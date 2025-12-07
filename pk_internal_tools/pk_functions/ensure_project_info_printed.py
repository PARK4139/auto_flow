from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_project_info_printed():
    import sys
    from pk_internal_tools.pk_functions import ensure_console_cleared
    from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
    from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
    from pk_internal_tools.pk_functions.get_project_info_from_pyproject import get_project_info_from_pyproject

    ensure_console_cleared()
    project_info = get_project_info_from_pyproject()

    print(f"{PK_ANSI_COLOR_MAP['BRIGHT_MAGENTA']}{PK_UNDERLINE}\n" \
          f"Project Information\n" \
          f"{project_info}{PK_ANSI_COLOR_MAP['RESET']}")
