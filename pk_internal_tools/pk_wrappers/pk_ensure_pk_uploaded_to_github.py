import traceback

from pk_internal_tools.pk_functions.assist_to_upload_pnx_to_git import assist_to_upload_pnx_to_git
from pk_internal_tools.pk_functions.ensure_pk_colorama_initialized_once import ensure_pk_colorama_initialized_once
from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_functions.get_pk_token import get_pk_token
from pk_internal_tools.pk_objects.pk_directories import D_PK_DATA
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root


if __name__ == "__main__":
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:

        git_repo_url = get_pk_token(f_token=rf"{D_PK_DATA}/pk_token_pk_github_repo_url.toml", text_plain="")
        d_working = d_pk_root
        branch_n = 'dev'
        assist_to_upload_pnx_to_git(d_working=d_working, git_repo_url=git_repo_url, branch_n=branch_n)

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
