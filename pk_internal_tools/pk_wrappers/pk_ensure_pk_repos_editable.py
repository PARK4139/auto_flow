import traceback

from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_objects.pk_directories import D_PK_MEMO_REPO, D_AUTO_FLOW_REPO
from pk_internal_tools.pk_objects.pk_directories import d_pk_root

if __name__ == "__main__":
    try:
        import traceback

        from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
        from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
        from pk_internal_tools.pk_functions.ensure_pk_colorama_initialized_once import ensure_pk_colorama_initialized_once
        from pk_internal_tools.pk_functions.ensure_pk_log_initialized import ensure_pk_log_initialized
        from pk_internal_tools.pk_functions.ensure_pk_repo_editable import ensure_pk_repo_editable
        from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
        from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_window_title_replaced import ensure_pk_wrapper_starter_window_title_replaced
        from pk_internal_tools.pk_functions.get_window_title_temp_identified import get_window_title_temp_identified
        from pk_internal_tools.pk_objects.pk_directories import d_pk_root
        from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done

        ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)

        repos_to_edit = [d_pk_root, D_PK_MEMO_REPO, D_AUTO_FLOW_REPO]
        for repo in repos_to_edit:
            ensure_pk_repo_editable(__file__, repo_to_edit=repo)

        ensure_pk_wrapper_starter_suicided(__file__)
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
