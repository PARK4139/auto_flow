if __name__ == "__main__":
    import traceback

    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:

        import logging
        import traceback

        from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken, ensure_value_completed_2025_10_12_0000
        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
        from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
        from pk_internal_tools.pk_functions.ensure_python_file_unused_clean import ensure_python_file_unused_clean
        from pk_internal_tools.pk_functions.get_easy_speakable_text import get_easy_speakable_text
        from pk_internal_tools.pk_objects.pk_texts import PkTexts
        from pk_internal_tools.pk_objects.pk_directories import d_pk_wrappers, d_pk_root
        from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


        @ensure_seconds_measured
        def _ensure_python_file_unused_clean_pk_project_self():
            # TODO  entrypoints 사용자 입력처리 필요.
            try:

                question = f'사용하지 않는 프로젝트 내의 파이썬 파일을 dry run 으로 출력할까요?'
                ensure_spoken(get_easy_speakable_text(question))
                ok = ensure_value_completed_2025_10_12_0000(key_hint=rf"{question}=", values=[PkTexts.YES, PkTexts.NO])
                if ok != PkTexts.YES:
                    ensure_pk_wrapper_starter_suicided(__file__)

                ok = ensure_python_file_unused_clean(
                    project_root=d_pk_root,
                    entrypoints=[
                        d_pk_wrappers / "pk_ensure_pk_enabled.py",
                        d_pk_wrappers / "hello_world.py",
                    ],
                    execute=False,  # DRY-RUN
                    trash=True,  # if execute=True, try moving to trash
                    prune_empty_dirs_flag=True,  # remove empty dirs afterward
                    safe_filter=True,  # keep skipping venv/.git/tests/etc.
                    extra_keep=[  # whitelist
                        "scripts/*.py"
                        "*pyproject.py"
                    ],
                )
                logging.debug(rf"ok={ok}")

                question = f'정말로, 사용하지 않는 프로젝트 내의 파이썬 파일을 지울까요'
                ensure_spoken(get_easy_speakable_text(question))
                ok = ensure_value_completed_2025_10_12_0000(key_hint=rf"{question}=", values=[PkTexts.YES, PkTexts.NO])
                if ok != PkTexts.YES:
                    ensure_pk_wrapper_starter_suicided(__file__)

                ok = ensure_python_file_unused_clean(
                    project_root=d_pk_root,
                    entrypoints=[
                        d_pk_wrappers / "pk_ensure_pk_enabled.py",
                        d_pk_wrappers / "hello_world.py",
                    ],
                    execute=False,
                    # execute=True,
                    trash=True,
                    prune_empty_dirs_flag=True,
                    safe_filter=True,
                    extra_keep=[
                        "scripts/*.py"
                        "*pyproject.py"
                    ],
                )
                logging.debug(rf"ok={ok}")

                return True
            except:
                ensure_debug_loged_verbose(traceback)
            finally:
                pass

        _ensure_python_file_unused_clean_pk_project_self()

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
