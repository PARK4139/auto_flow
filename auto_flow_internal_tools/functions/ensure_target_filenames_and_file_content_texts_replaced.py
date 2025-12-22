import sys
from pathlib import Path

# When running a script directly, its parent directory is added to sys.path.
# To allow imports from the 'source' package, we need to add the project root.
# This script is at 'source/functions/', so the project root is three levels up.
_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

# Now that the project root is on the path, we can import the setup script
# which handles the rest of the paths (like the submodule).
# import source.internal_setup # Removed as 'source' directory no longer exists

from pk_internal_tools.pk_objects.pk_system_operation_options import \
    SetupOpsForPnxReplacement


from auto_flow_internal_tools.constants.af_directory_paths import D_PROJECT_ROOT_PATH, D_FUNCTIONS_PATH
from auto_flow_internal_tools.constants.af_file_paths import (
    F_GITIGNORE_PATH,
    F_GITIGNORE_PUBLIC_PATH,
    F_GEMINI_MD_PATH,
    F_PYPROJECT_TOML_PATH,
    F_RUN_CMD_PATH,
    F_SETUP_CMD_PATH,
    F_TEARDOWN_CMD_PATH,
    F_GITATTRIBUTES_PATH,
    F_ENV_PATH,
)

if __name__ == "__main__":
    import logging

    from pk_internal_tools.pk_functions.ensure_target_filename_and_file_content_text_replaced import \
        ensure_target_filename_and_file_content_text_replaced



    from pk_internal_tools.pk_functions.ensure_target_filenames_and_file_content_texts_replaced import \
        ensure_target_filenames_and_file_content_texts_replaced

    # pk_option : simple
    # old_text = '업무자동화'
    # new_text = 'auto_flow'
    old_text = 'ensure_custom_cli_started'
    new_text = 'ensure_custom_cli_started'
    # pk_ensure_target_filenames_and_file_content_texts_replaced


    # pk_option : " " -> "_"
    # old_text = 'ensure_matrix_console_made'.replace(" ", "_")
    # new_text = 'ensure_matrix_console_made'

    # pk_option : dictionary correction
    # old_text = '_like_person'
    # new_text = '_like_human'

    # pk_option : logging style correction
    # old_text = 'logging.debug(" '
    # new_text = 'logging.debug("'

    # pk_option : logging style correction
    # old_text = 'logging.debug("'
    # new_text = 'logging.debug("'

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
    # old_text = rf'ensure_youtube_videos_downloaded_2025_05_01_0000'
    # new_text = rf'ensure_youtube_videos_downloaded_2025_05_01_0000'

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
        D_PROJECT_ROOT_PATH,
        D_FUNCTIONS_PATH,
        # D_PK_SYSTEM_PATH,  # Removed to comply with read-only pk_system submodule rule
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
        ensure_target_filenames_and_file_content_texts_replaced(d_target=d_target, old_text=old_text, new_text=new_text, target_extensions=target_extensions, ignored_directory_names=ignored_directory_names, operation_mode=SetupOpsForPnxReplacement.FILE_NAMES_AND_CONTENTS_ONLY)


    f_targets = [
        F_GITIGNORE_PATH, # Re-enabled as per user's request
        F_GITIGNORE_PUBLIC_PATH, # Re-enabled as per user's request
        F_GEMINI_MD_PATH, # Re-enabled as per user's request
        F_PYPROJECT_TOML_PATH, # Re-enabled as per user's request
        F_RUN_CMD_PATH, # Re-enabled as per user's request
        F_SETUP_CMD_PATH, # Re-enabled as per user's request
        F_TEARDOWN_CMD_PATH, # Re-enabled as per user's request
        F_GITATTRIBUTES_PATH, # Re-enabled as per user's request
        F_ENV_PATH,
    ]
    for f_target in f_targets:
        if f_target.exists():
            ensure_target_filename_and_file_content_text_replaced(f_target=f_target, old_text=old_text, new_text=new_text,operation_mode=SetupOpsForPnxReplacement.FILE_NAMES_AND_CONTENTS_ONLY)
        else:
            logging.debug(f"[SKIP] 파일이 존재하지 않습니다: {f_target}")