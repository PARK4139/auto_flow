import traceback
from textwrap import dedent

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose


# @ensure_seconds_measured
def get_ensure_value_complete_shortcut_guide_text(multi_select):
    """
    Return shortcut guide text with normalized indentation.
    """
    try:
        import textwrap

        if multi_select:
            text = dedent("""
                CTRL-K: remove 커서의 뒤
                CTRL-U: remove 커서의 앞
                CTRL-A: move cursor to forward of line
                CTRL-E: move cursor to backword of line
                ALT-B: move cursor to forward by word
                ALT-F: move cursor to backword by word
                ALT-A: SELECT All TOGGLE
            """).strip()
        else:
            text = dedent("""
                CTRL-K: remove 커서의 뒤
                CTRL-U: remove 커서의 앞
                CTRL-A: move cursor to forward of line
                CTRL-E: move cursor to backword of line
                ALT-B: move cursor to forward by word
                ALT-F: move cursor to backword by word
            """).strip()

        return text

    except Exception as e:
        ensure_debugged_verbose(traceback, e=e)
        return ""
