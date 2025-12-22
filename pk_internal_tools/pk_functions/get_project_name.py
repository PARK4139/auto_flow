from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_project_name(project_info=None):
    from pk_internal_tools.pk_functions.get_project_info_from_pyproject import get_project_info_from_pyproject
    if project_info is None:
        project_info = get_project_info_from_pyproject()

    project_name = None
    if project_info and hasattr(project_info, "data"):
        project_name = project_info.data.get("name")

    return project_name or "unknown"
