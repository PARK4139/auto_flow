if __name__ == "__main__":
    import logging
    import traceback

    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root_hidden, D_PK_CLONE, d_pk_wrappers, d_pk_internal_tools, d_pk_external_tools, D_PK_FUNCTIONS, d_pk_external_tools, d_pk_external_tools, d_pk_tests, D_PK_OBJECTS, D_PK_wrappers, d_pk_info, d_pk_cache
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root

    from pk_internal_tools.pk_functions.ensure_project_published import ensure_project_published

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:
        d_destination = D_PK_CLONE
        d_base_project = d_pk_root
        F_GITIGNORE_TO_PUBLISH = d_base_project / ".gitignore_for_public"

        blacklist = [
            # directories
            d_pk_root_hidden,  # 민감정보 *
            d_base_project / "__pycache__",
            d_base_project / ".cursor",
            d_base_project / ".idea",
            d_base_project / ".git",
            d_base_project / ".venv",
            d_base_project / ".pytest_cache",
            d_base_project / ".venv",
            d_base_project / ".venv",
            d_base_project / ".venv_matter",
            d_base_project / ".vscode",
            d_base_project / "pk_system.egg-info",
            d_base_project / "node_modules",
            d_base_project / "pk_cache",
            d_base_project / "pk_docs",
            d_base_project / "pk_logs",
            d_base_project / "pk_prompts",
            d_base_project / "TODO*",
            d_base_project / "prompts*",
            D_PK_FUNCTIONS / "#*.*",
            d_pk_external_tools / "__pycache__",
            d_pk_external_tools / "docker-compose-matter.yml",
            D_PK_OBJECTS / "urls.py",
            d_pk_external_tools,
            d_pk_external_tools / "#*.sh",
            d_pk_external_tools / "*.rdp",
            d_pk_external_tools / "TODO_*",
            # d_pk_external_tools / "# ensure_pk_components_sourced.sh" ,
            # d_pk_external_tools / "# ensure_pk_mysql_db_imported.sh" ,
            # d_pk_external_tools / "# ensure_uv_synced.sh" ,
            # d_pk_external_tools / "# ensure_pk_components_sourced.sh" ,
            # d_pk_external_tools / "# ensure_pk_mysql_db_imported.sh" ,
            # d_pk_external_tools / "# ensure_uv_synced.sh" ,
            # d_pk_external_tools / "#*.sh" ,
            # d_pk_external_tools / "TODO_*.sh" ,
            d_pk_internal_tools / "__pycache__",
            d_pk_internal_tools / "pk_system.egg-info",
            d_pk_internal_tools / "pk_fixers",
            d_pk_internal_tools / "pk_objects" / "__pycache__",
            d_pk_internal_tools / "pk_wrappers" / "__pycache__",
            d_pk_wrappers,
            D_PK_OBJECTS,
            d_pk_tests / "__pycache__",
            d_pk_tests / "TODO",
            D_PK_wrappers,
            # D_PK_FUNCTIONS,
            d_pk_tests,
            d_pk_cache,

            # files
            d_base_project / ".gitignore_for_test",
            F_GITIGNORE_TO_PUBLISH,
            D_PK_FUNCTIONS / "ensure_text_decoded.py",
            D_PK_FUNCTIONS / "ensure_text_encoded.py",
            d_pk_wrappers / "pk_ensure_pk_clone_published.py",
        ]
        publishlist = [  # pk_system 에  종속적인 필요한것들을 별도로 배포
            d_pk_root / "pk_qc_mode.toml",

            d_pk_info / '_version.py',

            # D_PK_FUNCTIONS / "ensure_pk_log_initialized.py",
            # D_PK_FUNCTIONS / "ensure_seconds_measured.py",
            # D_PK_FUNCTIONS / "ensure_pk_wrapper_starter_suicided.py",

            D_PK_OBJECTS,
            # D_PK_OBJECTS / "pk_spoken_manager.py",
            # D_PK_OBJECTS / "pk_colors.py",
            # D_PK_OBJECTS / "pk_qc_mode.py",
            # D_PK_OBJECTS / "pk_directories.py",
            # D_PK_OBJECTS / "pk_files.py",

            d_pk_wrappers / "pk_ensure_pk_enabled.py",
            d_pk_wrappers / "pk_ensure_pk_wrapper_starter_executed.py",
            d_pk_wrappers / "hello_world.py",
            d_pk_wrappers / "pk_ensure_python_file_unused_clean_pk_project_self.py",

        ]
        success = ensure_project_published(
            d_project_to_publish=d_base_project,
            d_destination=d_destination,
            f_gitignore_base=F_GITIGNORE_TO_PUBLISH,
            blacklist=blacklist,
            publishlist=publishlist,
        )
        if success:
            logging.debug("pk_clone has been successfully prepared for publication.")
        else:
            logging.debug(f"{PkTexts.WARNING}Failed to publish pk_clone.")

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
