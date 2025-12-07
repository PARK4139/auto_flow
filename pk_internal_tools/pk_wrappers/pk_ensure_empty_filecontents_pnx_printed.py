from pk_internal_tools.pk_functions.ensure_empty_filecontents_pnx_printed import ensure_empty_filecontents_pnx_printed

if __name__ == "__main__":
    import traceback
    from pk_internal_tools.pk_functions.ensure_window_title_replaced import ensure_window_title_replaced
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_window_title_replaced import ensure_pk_wrapper_starter_window_title_replaced

    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_functions.ensure_pk_colorama_initialized_once import ensure_pk_colorama_initialized_once
    from pk_internal_tools.pk_objects.pk_directories  import d_pk_root

    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        ensure_window_title_replaced(get_nx(__file__))


        root = d_pk_root
        empty_files = ensure_empty_filecontents_pnx_printed(
            root_dir=root,
            allowed_extensions=(".py", ".txt", ".md", ".json", ".csv")
        )

        if empty_files:
            print("실질적으로 내용이 없는 파일 목록:")
            for f in empty_files:
                print(f" - {f}")
        else:
            print("내용이 비어 있는 파일이 없습니다.")

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)