from pk_internal_tools.pk_functions.ensure_paused import ensure_paused
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.is_os_windows import is_os_windows


def _logging_debug_and_print(text):
    import logging
    logging.debug(text)
    print(text)


@ensure_seconds_measured
def ensure_target_file_names_and_target_file_texts_replaced_via_manual():
    """
        TODO: Write docstring for ensure_target_file_names_and_target_file_texts_replaced_via_manual.
    """
    try:
        import logging
        from pk_internal_tools.pk_objects.pk_files import F_GITIGNORE, F_GEMINI_MD, F_GEMINIIGNORE, F_PYPROJECT_TOML, F_GITATTRIBUTES, F_ENV, F_RUN_CMD
        from pk_internal_tools.pk_objects.pk_modes import PkModesForEnsureTargetFilenameAndFileContentTextReplaced
        from pk_internal_tools.pk_functions.ensure_target_file_names_and_target_file_texts_replaced import ensure_target_file_names_and_target_file_texts_replaced
        from pk_internal_tools.pk_functions.ensure_target_file_name_and_file_texts_replaced import ensure_target_file_name_and_file_texts_replaced
        from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
        from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT_HIDDEN, D_PK_EXTERNAL_TOOLS, D_PK_FUNCTIONS, D_PK_wrappers, D_PK_OBJECTS, D_PK_TESTS, D_PK_ROOT, D_PK_ROOT, D_PK_INTERNAL_TOOLS, D_HISTORY_CACHE, D_MOUSE_CLICK_COORDINATION_HISTORY, D_PK_DOCS, D_PK_MEMO_REPO, D_USERPROFILE, D_PK_TODO, D_PK_CACHE, D_PK_KIRIA
        from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE

        if is_os_windows():
            ensure_command_executed(cmd='chcp 65001')

        ensure_paused('r u sure to continue?\n')

        # TODO
        # "ensure_pk_yldp06yl_toggle_cli.py" ,   "ensure_pk_yldp06yl_toggle.py"
        # "ensure_pk_yldp06yl_rgb_cli.py" ,   "ensure_pk_yldp06yl_rgb.py"
        # "ensure_pk_yldp06yl_on_cli.py" ,   "ensure_pk_yldp06yl_on.py"
        # "ensure_pk_yldp06yl_off_cli.py" ,   "ensure_pk_yldp06yl_off.py"
        # "ensure_pk_yldp06yl_info_cli.py" ,   "ensure_pk_yldp06yl_info.py"
        # "ensure_pk_yldp06yl_color_temp_cli.py" ,   "ensure_pk_yldp06yl_color_temp.py"
        # "ensure_pk_yldp06yl_brightness_cli.py" ,   "ensure_pk_yldp06yl_brightness.py"

        # pk_option : simple
        old_text = 'PkColors'  # %%PK_DELI MITER%%
        new_text = 'PkColors'  # mkr

        # pk_option : " " -> "_"
        # old_text = 'ensure_matrix_console_made'.replace(" ", "_")
        # new_text = 'ensure_matrix_console_made'

        # pk_option : dictionary correction
        # old_text = '_like_person'
        # new_text = '_like_human'

        # pk_option : logging style correction
        # old_text = '_logging_debug_and_print(" '
        # new_text = '_logging_debug_and_print("

        # pk_option : logging style correction
        # old_text = '_logging_debug_and_print("'
        # new_text = '_logging_debug_and_print("

        # pk_option : de prefix double
        # old_text = '_executed'* 2
        # new_text = "_executed"
        # old_text = '_title'* 2
        # new_text = "_title"
        # old_text = '_like_person'* 2
        # new_text = "_like_person"
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
        # old_text = rf'ensure_youtube_videos_downloaded_2025_05_01_0000'
        # new_text = rf'ensure_youtube_videos_downloaded_2025_05_01_0000'

        # pk_option : try to automatic
        # old_text = rf'_enabled.py'
        # new_text = rf'ensure      pk_flow_assistance     ran'
        # new_text = new_text.replace('_', ' ')
        # new_text = '_'.join(new_text.split())
        # new_text = new_text.strip()
        # _logging_debug_and_print(f'''new_text={new_text} ''')
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
        # _logging_debug_and_print(f'''new_text={new_text} ''')
        # ensure_pk_system_log_editable()

        # pk_option : default
        d_targets = [
            # d_pk_system,  # not recommanded, too slow, for too many files, include system like .git
            D_PK_ROOT_HIDDEN,
            D_PK_INTERNAL_TOOLS,
            D_PK_EXTERNAL_TOOLS,  # D_PK_EXTERNAL_TOOLS 대신 D_PK_EXTERNAL_TOOLS 사용
            D_PK_FUNCTIONS,
            D_PK_wrappers,
            D_PK_OBJECTS,
            D_PK_TESTS,
            D_PK_CACHE,
            D_HISTORY_CACHE,
            D_MOUSE_CLICK_COORDINATION_HISTORY,
            D_PK_DOCS,
            D_PK_ROOT / ".cursor",
            D_PK_MEMO_REPO,
            D_PK_TODO,
            D_PK_KIRIA,
            rf"{D_USERPROFILE}\Downloads\pk_system\.pk_system\pk_history",
        ]

        # d_targets = [ # pk_option
        #     D_PK_ROOT_HIDDEN,
        # ]

        # d_targets = get_pnxs_from_d_working(d_working=d_pk_system, only_dirs=True, with_walking=True)

        # ignored_directory_names = [".venv", ".venv", ".venv", "__pycache__"]
        ignored_directory_names = [".venv", ".venv", "__pycache__", ".git"]

        # target_extensions = [".py", ".cmd", ".bat", ".ps1", ".sh", ".bak", ".txt"]  # pk_option
        target_extensions = [".py", ".cmd", ".bat", ".ps1", ".sh", ".bak", ".txt", ".md", ".zshrc", ".bashrc", ".history"]  # pk_option

        # pk_option : upper
        # for d_target in d_targets:
        #     ensure_target_file_names_and_target_file_texts_replaced(d_target, old_text.upper(), new_text.upper(), target_extensions=target_extensions, ignored_directory_names = ignored_directory_names)

        # pk_option : upper
        # for d_target in d_targets:
        #     ensure_target_file_names_and_target_file_texts_replaced(d_target, old_text.lower(), new_text.lower(), target_extensions=target_extensions, ignored_directory_names=ignored_directory_names)

        # pk_option : keep cases
        for d_target in d_targets:
            _logging_debug_and_print(f'''{PK_UNDERLINE}''')
            _logging_debug_and_print(f'''# d_target={d_target}''')
            ensure_target_file_names_and_target_file_texts_replaced(d_target=d_target, old_text=old_text, new_text=new_text, target_extensions=target_extensions, ignored_directory_names=ignored_directory_names, operation_mode=PkModesForEnsureTargetFilenameAndFileContentTextReplaced.FILENAME_AND_FILECONTENT)

        f_targets = [
            F_GITIGNORE,
            F_GEMINI_MD,
            F_GEMINIIGNORE,
            F_PYPROJECT_TOML,
            F_GITATTRIBUTES,
            F_ENV,
            F_RUN_CMD,
        ]
        for f_target in f_targets:
            _logging_debug_and_print(f'''{PK_UNDERLINE}''')
            _logging_debug_and_print(f'''# f_target={f_target}''')
            ensure_target_file_name_and_file_texts_replaced(f_target=f_target, old_text=old_text, new_text=new_text, operation_mode=PkModesForEnsureTargetFilenameAndFileContentTextReplaced.FILENAME_AND_FILECONTENT)

    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
