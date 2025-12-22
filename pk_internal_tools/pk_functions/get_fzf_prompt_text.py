from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def get_fzf_prompt_text():
    """
    fzf 프롬프트에 표시될 텍스트를 생성합니다.
    버전 정보는 pyproject.toml이 아닌 git describe를 통해 직접 가져와 항상 최신 상태를 유지합니다.
    """
    import logging
    # Lazy import as per project rules
    from pk_internal_tools.pk_functions.ensure_pk_system_version_updated import get_version_from_git
    from pk_internal_tools.pk_functions.get_project_name import get_project_name
    from pk_internal_tools.pk_functions.get_project_info_from_pyproject import get_project_info_from_pyproject
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    prompt_text = f"{PkTexts.COMMANDS}> "  # Default prompt
    
    project_info = get_project_info_from_pyproject()
    project_name = get_project_name(project_info) if project_info else "pk_system"
    
    # Get version directly from git for accuracy
    git_version = get_version_from_git()
    
    if git_version and git_version != "unknown":
        # The version from git might already have a 'v' prefix, e.g., v2025.12.7-dirty
        # So we just use it directly.
        prompt_text = f"{project_name} {git_version}> "
    else:
        # Fallback to pyproject.toml if git fails
        logging.warning("Git 버전을 가져올 수 없어 pyproject.toml의 버전으로 대체합니다.")
        if project_info:
            from pk_internal_tools.pk_functions.get_pk_version import get_pk_version
            project_version = get_pk_version(project_info)
            prompt_text = f"{project_name} v{project_version} (fallback)> "

    return prompt_text
