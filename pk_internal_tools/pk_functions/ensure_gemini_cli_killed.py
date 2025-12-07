from pk_internal_tools.pk_functions.get_gemini_cli_window_title_by_auto import get_gemini_cli_window_title_by_auto
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_gemini_cli_killed(gemini_cli_window_title=None):
    from pk_internal_tools.pk_functions.ensure_windows_killed_like_human_by_window_title import ensure_windows_killed_like_human_by_window_title
    if gemini_cli_window_title is None:
        gemini_cli_window_title = get_gemini_cli_window_title_by_auto()
    if gemini_cli_window_title is not None:
        ensure_windows_killed_like_human_by_window_title(gemini_cli_window_title)
