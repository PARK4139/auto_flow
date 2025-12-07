import logging

if __name__ == "__main__":
    import traceback
    from pk_internal_tools.pk_functions.ensure_guided_not_prepared_yet import ensure_not_prepared_yet_guided
    from pk_internal_tools.pk_functions.ensure_os_locked_at_sleeping_time import ensure_os_locked_at_sleeping_time

    from pk_internal_tools.pk_functions import get_pk_time_2025_10_20_1159
    from pk_internal_tools.pk_functions.ensure_pk_colorama_initialized_once import ensure_pk_colorama_initialized_once
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_input_preprocessed import ensure_input_preprocessed
    from pk_internal_tools.pk_functions.ensure_pnx_backed_up import ensure_pnx_backed_up
    from pk_internal_tools.pk_functions.get_pk_token import get_pk_token
    from pk_internal_tools.pk_functions.is_anyang_house_pc import is_host_pk_asus
    from pk_internal_tools.pk_functions.is_day import is_day
    from pk_internal_tools.pk_functions.is_internet_connected_2025_10_21 import is_internet_connected_2025_10_21
    from pk_internal_tools.pk_functions.push_pnx_to_github import push_pnx_to_github
    from pk_internal_tools.pk_objects.pk_directories import D_PK_DATA
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root, D_ARCHIVED

    ensure_pk_colorama_initialized_once()
    try:
        if is_host_pk_asus():

            # backup to local
            if is_day(dd=15):
                pnx_working = d_pk_root
                ensure_pnx_backed_up(pnx_working=pnx_working, d_dst=D_ARCHIVED)

            # puload to github
            if is_internet_connected_2025_10_21():
                git_repo_url = get_pk_token(f_token=rf"{D_PK_DATA}/pk_token_pk_github_repo_url.toml", text_plain="")
                commit_msg = ensure_input_preprocessed(text_working=f"commit_msg=", upper_seconds_limit=30, return_default=f"feat: auto pushed by pk_system at {get_pk_time_2025_10_20_1159("%Y-%m-%d %H:%M")}")
                push_pnx_to_github(d_working=d_pk_root, commit_msg=commit_msg, branch_n='dev')
            else:
                logging.debug("Push failed: No internet connection")

            # ensure_os_shutdown() # pk_option
            ensure_os_locked_at_sleeping_time()  # pk_option


        else:
            ensure_not_prepared_yet_guided()


    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
