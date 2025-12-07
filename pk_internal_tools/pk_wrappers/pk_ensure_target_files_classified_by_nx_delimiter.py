if __name__ == '__main__':
    try:
        import traceback

        pk_assist_to_ensure_target_files_classified_by_nx_delimiter()

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__,traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_system=d_pk_system)
