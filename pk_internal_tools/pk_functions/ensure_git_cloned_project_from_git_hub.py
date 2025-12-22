from pathlib import Path

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_git_cloned_project_from_git_hub(*, branch_name, repository_url, checkout_path: Path):
    import logging

    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_functions.get_easy_speakable_text import get_easy_speakable_text
    from pk_internal_tools.pk_functions.get_nx import get_nx

    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed

    for std_out in ensure_command_executed(f'git clone -b {branch_name} {repository_url} {checkout_path}'):
        logging.debug(rf"std_out={std_out}")
    if checkout_path.exists():
        ensure_spoken(get_easy_speakable_text(f"{get_nx(checkout_path)} 로 깃 클론 완료"))
    return True
