import logging

from pk_internal_tools.pk_objects.pk_directories import d_pk_root_hidden
from pk_internal_tools.pk_functions.ensure_text_saved_to_clipboard import ensure_text_saved_to_clipboard
from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.get_pk_token import get_pk_token
from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE

if __name__ == "__main__":
    try:
        import traceback

        github_pat = get_pk_token(f_token=f'{d_pk_root_hidden}/pk_token_github_pat.toml', text_plain='')
        ensure_text_saved_to_clipboard(github_pat)
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)

    finally:
        # ensure_finally_routine_done(traced_file=__file__, d_pk_system=d_pk_system)
        logging.debug(f'{PK_UNDERLINE}')
        # logging.debug(f'{'{PkTexts.TRY_GUIDE}'} {script_to_run_python_program_in_venv}')
        logging.debug(f'{PK_UNDERLINE}')
