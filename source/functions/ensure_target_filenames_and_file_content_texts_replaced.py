

if __name__ == "__main__":
    import logging
    from ...resource.pk_system.pk_system_sources.pk_system_objects.pk_system_operation_options import \
        SetupOpsForEnsureTargetFilenameAndFileContentTextReplacedAdvanced

    from ...resource.pk_system.pk_system_sources.pk_system_functions.ensure_target_filename_and_file_content_text_replaced import \
        ensure_target_filename_and_file_content_text_replaced

    from ...resource.pk_system.pk_system_sources.pk_system_objects.pk_system_directories import D_DOWNLOADS, \
        D_PK_SYSTEM, \
        D_MOUSE_CLICK_HISTORY, D_HISTORY_CACHE, D_PK_SYSTEM_TESTS, D_PK_SYSTEM_OBJECTS, D_PK_SYSTEM_REFACTORS, \
        D_PK_SYSTEM_FUNCTIONS, D_PK_SYSTEM_OS_LAYER_RESOURCES, D_PK_SYSTEM_RESOURCES, D_PK_SYSTEM_SOURCES, \
        D_PK_SYSTEM_SENSITIVE

    from ...resource.pk_system.pk_system_sources.pk_system_functions.ensure_target_filenames_and_file_content_texts_replaced import \
        ensure_target_filenames_and_file_content_texts_replaced

    # literal to replace
    # signature
    # signature

    # pk_option : simple
    old_text = '업무자동화'
    new_text = 'autoflow'

    # pk_option : " " -> "_"
    # old_text = 'ensure_matrix_console_made'.replace(" ", "_")
    # new_text = 'ensure_matrix_console_made'

    # pk_option : dictionary correction
    # old_text = '_like_person'
    # new_text = '_like_human'

    # pk_option : logging style correction
    # old_text = 'logging.debug(" '
    # new_text = 'logging.debug("

    # pk_option : logging style correction
    # old_text = 'logging.debug("'
    # new_text = 'logging.debug("

    # pk_option : de prefix double
    # old_text = 'itories'* 2
    # new_text = "itories"
    # old_text = '_v_2025_10_12_0000'* 2
    # new_text = "_v_2025_10_12_0000"
    # old_text = '_0000'* 2
    # new_text = "_0000"
    # old_text = 'ensure_'* 2
    # new_text = "ensure_"
    # old_text = '_by_window_title'* 2
    # new_text = "_by_window_title"
    # old_text = 'pk_'* 2
    # new_text = "pk_"
    # old_text = '_enabled'* 2
    # new_text = "_enabled"

    # pk_option : try to automatic
    # old_text = rf'ensure_' * 2
    # old_text = rf'ensure_youtube_videos_downloaded_v_2025_05_01_0000'
    # new_text = rf'ensure_youtube_videos_downloaded_v_2025_05_01_0000'

    # pk_option : try to automatic
    # old_text = rf'_enabled.py'
    # new_text = rf'ensure      pk_life_assistance     ran'
    # new_text = new_text.replace('_', ' ')
    # new_text = '_'.join(new_text.split())
    # new_text = new_text.strip()
    # logging.debug(f'''new_text={new_text} ''')
    # raise

    # pk_option : try to automatic
    # mode = 3
    # s = rf'pk_ensure_venv_path_config_updated'
    # if mode == 1:
    #     old_text = s
    #     new_text = rf'pk_ensure_drag_changed_printed '
    # elif mode == 2: # deduplicate mode
    #     new_text = rf'at_time_promised'
    #     old_text = rf'{new_text}_{new_text}'
    # elif mode == 3:
    #     old_text = s[3:] if s.startswith("pk_") else s
    #     prefix = rf"pk_ensure"
    #     object = rf"venv_path_config"
    #     verb = rf"updateed"
    #     suffix = "_" + rf"via_google"
    #     suffix = ""
    #     new_text = rf"{prefix}_{object}_{verb}{suffix}"

    # TODO
    # old_text = rf'push_pnx_to_github'  # pk_option # 하드코딩 유지
    # double_object_verb = rf'ensure' # pk_option # 하드코딩 유지
    # object = rf'pnx' # 하드코딩말고 old_text에서 형태소 분석으로 목적어(object)를 추출하여 초기화
    # verb = rf'push' # 하드코딩말고 old_text에서 형태소 분석으로 동사(verb)를 추출하여 초기화
    # past_participle = rf'{verb}ed' # past participle 는 경우에 따라 ed 가 아닌 경우가 있어. 더 정확한 처리가 필요.
    # past_participle_and_decorating_word = old_text.replace(rf"_{object}_", "_").replace(verb, past_participle)
    # new_text = double_object_verb.removeprefix("_").removesuffix("_") + "_" + object.removeprefix("_").removesuffix("_") + "_" + past_participle_and_decorating_word.removeprefix("_").removesuffix("_")
    # logging.debug(f'''new_text={new_text} ''')
    # ensure_pk_system_log_editable()

    # pk_option : memo
    # d_targets = [
    #     F_MEMO_WORKING_MD,
    # ]

    # pk_option : default
    d_targets = [
        #     D_PK_SYSTEM,  # not recomanded, too slow, for too many files, include system like .git
        D_PK_SYSTEM_SENSITIVE,
        D_PK_SYSTEM_SOURCES,
        D_PK_SYSTEM_RESOURCES,
        D_PK_SYSTEM_OS_LAYER_RESOURCES,
        D_PK_SYSTEM_FUNCTIONS,
        D_PK_SYSTEM_REFACTORS,
        D_PK_SYSTEM_OBJECTS,
        D_PK_SYSTEM_TESTS,
        D_HISTORY_CACHE,
        D_MOUSE_CLICK_HISTORY,
    ]

    # d_targets = [ # pk_option
    #     D_PK_SYSTEM_SENSITIVE,
    # ]

    # d_targets = get_pnxs_from_d_working(d_working=D_PK_SYSTEM, only_dirs=True, with_walking=True)

    # ignored_directory_names = [".venv", ".venv_linux", ".venv_windows", "__pycache__"]
    ignored_directory_names = [".venv", ".venv_linux", "__pycache__", ".git"]

    # target_extensions = [".py", ".cmd", ".bat", ".ps1", ".sh", ".bak", ".txt"]  # pk_option
    target_extensions = [".py", ".cmd", ".bat", ".ps1", ".sh", ".bak", ".txt", ".md", ".zshrc", ".bashrc", ".history"]  # pk_option

    # pk_option : upper
    # for d_target in d_targets:
    #     ensure_target_filenames_and_file_content_texts_replaced(d_target, old_text.upper(), new_text.upper(), target_extensions=target_extensions, ignored_directory_names = ignored_directory_names)

    # pk_option : upper
    # for d_target in d_targets:
    #     ensure_target_filenames_and_file_content_texts_replaced(d_target, old_text.lower(), new_text.lower(), target_extensions=target_extensions, ignored_directory_names=ignored_directory_names)

    # pk_option : keep cases
    for d_target in d_targets:
        logging.debug(f'''d_target={d_target} ''')
        ensure_target_filenames_and_file_content_texts_replaced(d_target=d_target, old_text=old_text, new_text=new_text, target_extensions=target_extensions, ignored_directory_names=ignored_directory_names, operation_mode=SetupOpsForEnsureTargetFilenameAndFileContentTextReplacedAdvanced.BOTH)

    f_targets = [
        D_PK_SYSTEM / ".gitignore",
        D_PK_SYSTEM / ".gitignore_for_public",
        D_PK_SYSTEM / "GEMINI.md",
        D_PK_SYSTEM / "pyproject.toml",
        D_PK_SYSTEM / "run.cmd",
        D_PK_SYSTEM / "setup.cmd",
        D_PK_SYSTEM / "teardown.cmd",
        D_PK_SYSTEM / ".gitattributes",
        D_DOWNLOADS / '.env',
    ]
    for f_target in f_targets:
        ensure_target_filename_and_file_content_text_replaced(f_target=f_target, old_text=old_text, new_text=new_text,operation_mode=SetupOpsForEnsureTargetFilenameAndFileContentTextReplacedAdvanced.BOTH)
