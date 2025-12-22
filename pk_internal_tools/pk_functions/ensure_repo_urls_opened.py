import traceback

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_values_completed import ensure_values_completed
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_objects.pk_urls import URL_GIT_HUB_PK_SYSTEM_GIT, URL_GIT_HUB_AUTO_FLOW_GIT


@ensure_seconds_measured
def ensure_repo_urls_opened():
    """
        TODO: Write docstring for ensure_repo_urls_opened.
    """
    try:
        func_n = get_caller_name()
        repo_urls = [
            URL_GIT_HUB_PK_SYSTEM_GIT,
            URL_GIT_HUB_AUTO_FLOW_GIT,
        ]
        repo_urls_to_open = ensure_values_completed(
            key_name="repo_urls_to_open",
            options=repo_urls,
            func_n=func_n,
            history_reset=True,
        )
        for repo_url in repo_urls_to_open:
            ensure_pnx_opened_by_ext(repo_url)

        return True
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
