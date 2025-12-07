if __name__ == "__main__":
    import traceback
    from pk_internal_tools.pk_functions.ensure_pk_necessary_pnxs_made import ensure_pk_necessary_pnxs_made
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root, d_pk_root_hidden, d_pk_databases, d_pk_cache, d_pk_history, d_pk_config, d_pk_tokens, d_pk_cookies, d_pk_sessions, d_pk_backups, d_macros, D_PK_WORKING
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        necessary_pnxs = [
            d_pk_root_hidden,
            d_pk_databases,
            d_pk_cache,
            d_pk_history,
            d_pk_config,
            d_pk_tokens,
            d_pk_cookies,
            d_pk_sessions,
            d_pk_backups,
            d_macros,
            D_PK_WORKING,
        ]
        ensure_pk_necessary_pnxs_made(necessary_pnxs)

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_system)
