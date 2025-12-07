from pathlib import Path

from pk_internal_tools.pk_functions.ensure_target_opened_advanced import ensure_target_opened_advanced
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


def _handle_remove_readonly(func, path, exc):
    import os
    import stat
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else:
        raise


@ensure_seconds_measured
def _ensure_replace_filename_and_file_contents_replaced_advanced(old_text, new_text, d_checkout):
    from pk_internal_tools.pk_functions.ensure_target_filenames_and_file_content_texts_replaced_advanced import ensure_target_filenames_and_file_content_texts_replaced_advanced

    ignored_directory_names = [".venv", ".venv", "__pycache__", ".git"]
    target_extensions = [".py", ".cmd", ".bat", ".ps1", ".sh", ".bak", ".txt", ".md", ".zshrc", ".bashrc", ".history", ".toml"]
    ensure_target_filenames_and_file_content_texts_replaced_advanced(
        d_target=d_checkout,
        old_text=old_text,
        new_text=new_text,
        target_extensions=target_extensions,
        ignored_directory_names=ignored_directory_names
    )


@ensure_seconds_measured
def ensure_project_published(*, d_project_to_publish: Path, d_destination: Path, f_gitignore_base: Path, blacklist: list[Path], publishlist: list[Path]):
    import logging
    import shutil
    import traceback
    from pathlib import Path
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_objects.pk_files import F_UV_PYTHON_EXE, F_UV_ACTIVATE_BAT
    from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
    from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
    from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
    from pk_internal_tools.pk_functions.get_easy_speakable_text import get_easy_speakable_text
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken

    from pk_internal_tools.pk_functions.ensure_copy_file_as_file_renamed import ensure_copy_file_as_file_renamed
    from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
    from pk_internal_tools.pk_functions.ensure_git_cloned_project_from_git_hub import ensure_git_cloned_project_from_git_hub
    from pk_internal_tools.pk_functions.ensure_git_repo_pushed import ensure_git_repo_pushed
    from pk_internal_tools.pk_functions.ensure_publish_list_and_blacklist_validated import ensure_publish_list_and_blacklist_validated
    from pk_internal_tools.pk_functions.ensure_tree_dropped_with_ignorelist import ensure_tree_dropped_with_ignorelist
    from pk_internal_tools.pk_functions.ensure_tree_printed import ensure_tree_printed
    from pk_internal_tools.pk_functions.get_text_red import get_text_red
    from pk_internal_tools.pk_functions.normalize_entries_to_dst_relative import normalize_entries_to_dst_relative
    from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_objects.pk_urls import URL_GIT_HUB_PK_TASK_ORCHESTRATOR_CLI_GIT
    from pk_internal_tools.pk_functions.get_nx import get_nx
    from pk_internal_tools.pk_functions.ensure_tree_copied_except_blacklist_and_including_publishlist import ensure_tree_copied_except_blacklist_and_including_publishlist
    from pk_internal_tools.pk_objects.pk_mode_manager import PkModeManager

    try:
        if publishlist is None:
            publishlist = []
        if blacklist is None:
            blacklist = []

        # mode = PkModeManager.FAST_DEBUG
        mode = PkModeManager.SERVICE_OPERATION

        d_checkout = d_destination
        logging.debug(f'd_project_to_publish={d_project_to_publish}')
        logging.debug(f'd_checkout={d_checkout}')
        logging.debug(f'mode={mode}')

        # remove pk_clone
        if d_checkout.exists():
            logging.debug(f"{d_checkout} is removing ...")
            shutil.rmtree(d_checkout, onerror=_handle_remove_readonly)
        logging.debug(PK_UNDERLINE)
        logging.debug(f"after remove")
        ensure_tree_printed(d_checkout, max_depth=1)
        if d_checkout.exists():
            logging.debug(get_text_red(f"shutil.rmtree() is not worked"))
            return False

        # git clone pk_clone
        repository_url = URL_GIT_HUB_PK_TASK_ORCHESTRATOR_CLI_GIT
        git_branch_name = "main"
        d_checkout = d_checkout
        ensure_git_cloned_project_from_git_hub(repository_url=repository_url, branch_name=git_branch_name, checkout_path=d_checkout)
        logging.debug(PK_UNDERLINE)
        logging.debug(f"after git clone")
        ensure_tree_printed(d_checkout, max_depth=1)
        if not d_checkout.exists():
            logging.debug(get_text_red(f"ensure_git_cloned_project_from_git_hub() is not worked"))
            return False

        # drop pk_clone tree without .git
        f_checkout_git = d_checkout / ".git"
        ignorelist = [f_checkout_git]
        ensure_tree_dropped_with_ignorelist(d_target=d_checkout, ignorelist=ignorelist, dry_run=False)
        logging.debug(PK_UNDERLINE)
        logging.debug(f"after drop")
        ensure_tree_printed(d_checkout, max_depth=1)
        for file_to_ignore in ignorelist:
            if not file_to_ignore.exists():
                logging.debug(get_text_red(f"ensure_tree_dropped_with_ignorelist() is failed"))
                return False

        # f_gitignore_to_publish -> .gitignore 로 rename 하여 배포
        f_gitignore_to_publish = d_checkout / ".gitignore"
        if not ensure_copy_file_as_file_renamed(file_to_copy=f_gitignore_base, file_renamed=f_gitignore_to_publish):
            if not f_gitignore_to_publish.exists():
                logging.debug(get_text_red(f"ensure_copy_file_as_file_renamed() is failed"))
                return False

        # copy tree to publish
        logging.debug(f"Copying files from {d_project_to_publish} to {get_nx(d_checkout)}({d_checkout})...")
        ensure_tree_copied_except_blacklist_and_including_publishlist(d_project_to_publish, d_checkout, blacklist, publishlist)
        logging.debug(PK_UNDERLINE)
        blacklist_rel = normalize_entries_to_dst_relative(
            entries=blacklist,
            d_src=d_project_to_publish,
            d_dst=d_checkout,  # 목적지 루트
        )
        f_checkout_git_rel = Path(f_checkout_git).resolve(strict=False).relative_to(d_checkout)
        blacklist_rel.remove(f_checkout_git_rel)  # blacklist_rel 내부에 f_checkout_git_rel 없으면 에러 return
        publishlist_rel = normalize_entries_to_dst_relative(
            entries=publishlist,
            d_src=d_project_to_publish,
            d_dst=d_checkout,  # 목적지 루트
        )
        ok = ensure_publish_list_and_blacklist_validated(
            d_dst=d_checkout,
            blacklist=blacklist_rel,
            publishlist=publishlist_rel,
        )
        logging.debug(f"after copy")
        ensure_tree_printed(d_checkout, max_depth=2)
        if not ok:
            logging.debug(get_text_red(f"ensure_tree_copied_except_blacklist_and_including_publishlist() is failed"))
            return False
        logging.debug("블랙리스트 제외, 화이트리스트 포함, 복제완료")

        # # f_gitignore_to_publish -> .gitignore 로 rename 하여 배포
        # f_gitignore_to_publish = d_checkout / ".gitignore"
        # if not ensure_copy_file_as_file_renamed(file_to_copy=f_gitignore_base, file_renamed=f_gitignore_to_publish):
        #     if not f_gitignore_to_publish.exists():
        #         logging.debug(get_text_red(f"ensure_copy_file_as_file_renamed() is failed"))
        #         return False

        # replace project file contents text and filename text
        _ensure_replace_filename_and_file_contents_replaced_advanced(old_text=f"pk_external_tools", new_text="resources", d_checkout=d_checkout)
        _ensure_replace_filename_and_file_contents_replaced_advanced(old_text=f"pk_internal_tools", new_text="sources", d_checkout=d_checkout)
        _ensure_replace_filename_and_file_contents_replaced_advanced(old_text=f"pk_wrappers", new_text="wrappers", d_checkout=d_checkout)
        _ensure_replace_filename_and_file_contents_replaced_advanced(old_text=f"pk_objects", new_text="objects", d_checkout=d_checkout)
        _ensure_replace_filename_and_file_contents_replaced_advanced(old_text=f"pk_functions", new_text="functions", d_checkout=d_checkout)
        _ensure_replace_filename_and_file_contents_replaced_advanced(old_text=f"pk_info", new_text="system_info", d_checkout=d_checkout)
        _ensure_replace_filename_and_file_contents_replaced_advanced(old_text=f"pk_os_layer_resources", new_text="system_resources", d_checkout=d_checkout)
        _ensure_replace_filename_and_file_contents_replaced_advanced(old_text=f"pk_sounds", new_text="system_sounds", d_checkout=d_checkout)
        _ensure_replace_filename_and_file_contents_replaced_advanced(old_text=f"pk_logs", new_text="logs", d_checkout=d_checkout)
        # _ensure_replace_filename_and_file_contents_replaced_advanced(old_text=f"pk_qc_mode.toml", new_text="project_config.toml", d_checkout=d_checkout)
        _ensure_replace_filename_and_file_contents_replaced_advanced(old_text=f"pk_qc_mode_toml", new_text="project_config", d_checkout=d_checkout)
        ensure_spoken(get_easy_speakable_text(f'파일트리 명칭 변경완료'))

        _ensure_replace_filename_and_file_contents_replaced_advanced(old_text="pk_system", new_text=get_nx(d_destination), d_checkout=d_checkout)
        _ensure_replace_filename_and_file_contents_replaced_advanced(old_text="pk_system".upper(), new_text=get_nx(d_destination).upper(), d_checkout=d_checkout)
        ensure_spoken(get_easy_speakable_text(f'프로젝트명 변경완료'))

        _ensure_replace_filename_and_file_contents_replaced_advanced(old_text="wjdgn", new_text='pk_security_literal', d_checkout=d_checkout)
        ensure_spoken(get_easy_speakable_text(f'보안강화 완료'))

        ensure_pnx_opened_by_ext(d_checkout)
        ensure_spoken(get_easy_speakable_text(f'배포준비 완료'))

        python_file = d_checkout / f"sources" / f"wrappers" / f"pk_ensure_python_file_unused_clean_{get_nx(d_destination)}_project_self.py"
        cmd = rf'"cd /d "{d_pk_root}" && {F_UV_ACTIVATE_BAT} && {F_UV_PYTHON_EXE} "{python_file}"'
        ensure_command_executed(cmd)

        question = f'깃 허브로 퍼블리싱을 진행할까요?'
        ensure_spoken(get_easy_speakable_text(question))
        if QC_MODE:
            # pk_option
            # ok = ensure_value_completed_2025_10_12_0000(key_hint=rf"{question}=", values=[PkTexts.YES, PkTexts.NO])
            ok = PkTexts.YES
        else:
            ok = ensure_value_completed_2025_10_12_0000(key_name=question, options=[PkTexts.YES, PkTexts.NO])
        if ok != PkTexts.YES:
            ensure_pk_wrapper_starter_suicided(__file__)
        state = ensure_git_repo_pushed(d_local_repo=d_checkout)
        if not state or state.get("state") == False:
            ensure_spoken("깃 푸쉬 실패")
            return False
        ensure_spoken("깃 푸쉬 성공")
        logging.debug(f'''state={state} ''')

        ensure_target_opened_advanced(URL_GIT_HUB_PK_TASK_ORCHESTRATOR_CLI_GIT)
        ensure_pnx_opened_by_ext(d_checkout)
        return True

    except:
        ensure_debug_loged_verbose(traceback)
        return False
    finally:
        ensure_spoken(wait=True)
