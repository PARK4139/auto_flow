from pathlib import Path
from typing import Optional, List

from pk_internal_tools.pk_objects.pk_modes import PkModesForEnsurePnxBackedUp


def ensure_pnx_backed_up(pnx_working: Path, d_destination: Path, with_timestamp: bool = True, blacklist: Optional[List[str]] = None, back_up_mode: Optional[PkModesForEnsurePnxBackedUp] = None):
    import datetime
    import logging
    import os
    import shutil
    import tarfile
    import tempfile
    import traceback
    from pathlib import Path

    from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
    from pk_internal_tools.pk_functions.ensure_disk_capacity_safe import ensure_disk_capacity_safe
    from pk_internal_tools.pk_functions.ensure_git_repo_pushed import ensure_git_repo_pushed
    from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    from pk_internal_tools.pk_functions.ensure_trash_bin_emptied import ensure_trash_bin_emptied
    from pk_internal_tools.pk_functions.ensure_tree_copied_except_blacklist_and_including_whitelist import ensure_tree_copied_except_blacklist_and_including_whitelist
    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.ensure_values_completed import ensure_values_completed
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_objects.pk_modes import PkModesForEnsurePnxBackedUp
    from pk_internal_tools.pk_objects.pk_modes import PkModes
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    func_n = get_caller_name()
    try:
        pnx_working = Path(pnx_working)
        d_destination = Path(d_destination)
        logging.debug(f"pnx_working: {pnx_working}, exists: {pnx_working.exists()}")
        logging.debug(f"Before is_dir/is_file check: pnx_working={pnx_working}, is_dir={pnx_working.is_dir()}, is_file={pnx_working.is_file()}")
        if not pnx_working.exists():
            question = f"백업 대상이 존재하지 않습니다"
            logging.warning(question)
            ensure_spoken(question)
            return None

        # Interactive selection for blacklist if None
        if blacklist is None:
            if pnx_working.is_dir():
                sub_dirs = [str(d.relative_to(pnx_working)) for d in pnx_working.iterdir() if d.is_dir()]
                if sub_dirs:
                    directories_to_exclude = ensure_values_completed(
                        key_name="directories_to_exclude",
                        options=sub_dirs,
                        func_n=func_n,
                    )
                    if directories_to_exclude:
                        blacklist = [Path(item) for item in directories_to_exclude]  # Convert to Path objects
                        logging.info(f"선택된 제외 대상 디렉토리: {blacklist}")
                    else:
                        logging.info("제외할 하위 디렉토리가 선택되지 않았습니다.")
                else:
                    logging.info("제외할 하위 디렉토리가 없습니다.")
            else:
                logging.info(f"'{pnx_working}'은(는) 디렉토리가 아니므로 하위 디렉토리 제외를 선택할 수 없습니다.")
            # blacklist can be empty list now if nothing selected or no sub_dirs

        # Interactive selection for back_up_mode
        if back_up_mode is None:
            func_n = get_caller_name()
            back_up_mode_str = ensure_value_completed(
                key_name="back_up_mode",
                options=[member.value.lower() for member in PkModesForEnsurePnxBackedUp],
                func_n=func_n,
                guide_text="select back_up_mode"
            )
            back_up_mode = PkModesForEnsurePnxBackedUp(back_up_mode_str.upper())

        if back_up_mode == PkModesForEnsurePnxBackedUp.LOCAL_BACK_UP:
            ensure_pnx_made(d_destination, mode='d')

            logging.debug(f"QC_MODE is: {QC_MODE}")
            if not QC_MODE:
                ok, msg, stats = ensure_disk_capacity_safe(target_path=".", danger_used_percent=95.0)
                logging.debug(f"Disk capacity check result: ok={ok}, msg={msg}, stats={stats}")
                if not ok:
                    question = "디스크 용량이 부족합니다. 휴지통을 비울까요"
                    ensure_spoken(question)
                    ok = ensure_value_completed(key_name=question, options=[PkTexts.YES, PkTexts.NO], func_n=func_n)
                    logging.debug(f"User choice for trash bin: {ok}")
                    if ok == PkTexts.YES:
                        logging.debug("휴지통 비우기 실행")
                        ensure_trash_bin_emptied()
                    else:
                        logging.debug("휴지통 비우기 취소. 백업을 중단합니다.")
                        return None

            rar_result = None
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                file_to_compress = None

                if pnx_working.is_dir():
                    logging.debug(f"pnx_working is a directory. Copying to temp dir: {temp_path}")
                    # The contents of pnx_working will be copied into this new directory
                    target_copy_dir = temp_path / pnx_working.name
                    target_copy_dir.mkdir()
                    d_copied_tree = ensure_tree_copied_except_blacklist_and_including_whitelist(
                        d_working=pnx_working,
                        dst_dir=target_copy_dir,
                        blacklist=blacklist,  # Pass the (potentially interactive) blacklist
                        whitelist=[]
                    )
                    file_to_compress = d_copied_tree
                    logging.debug(f"After directory copy: d_copied_tree={d_copied_tree}")

                elif pnx_working.is_file():
                    logging.debug(f"pnx_working is a file. Copying to temp dir: {temp_path}")
                    # Create a directory inside temp to hold the file, preserving a parent folder structure
                    target_copy_dir = temp_path / pnx_working.stem
                    target_copy_dir.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(pnx_working, target_copy_dir / pnx_working.name)
                    file_to_compress = target_copy_dir
                    logging.debug(f"After file copy: target_copy_dir={target_copy_dir}")
                else:
                    logging.debug(f"pnx_working is neither a file nor a directory: {pnx_working}")
                    return None

                if file_to_compress is None:
                    logging.warning(f"file_to_compress is None. Skipping further processing for {pnx_working}.")
                    return None

                logging.debug(f"file_to_compress: {file_to_compress}, exists: {file_to_compress.exists()}")

                is_thing_to_compress_empty = not (file_to_compress.exists() and any(os.listdir(file_to_compress)))
                logging.debug(f"is_thing_to_compress_empty: {is_thing_to_compress_empty}")

                if not is_thing_to_compress_empty:
                    base_name = pnx_working.name
                    if with_timestamp:
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        file_compressed_n = f"{base_name}_{timestamp}"
                    else:
                        file_compressed_n = base_name

                    file_compressed_nx = f"{file_compressed_n}.tar.gz"
                    file_compressed = d_destination / file_compressed_nx

                    with tarfile.open(file_compressed, "w:gz") as tar:
                        tar.add(str(file_to_compress), arcname='.')

                    rar_result = str(file_compressed)
                else:
                    message = f"백업할 내용이 없습니다. 소스 폴더가 비어있어 압축을 건너뛰니다."
                    logging.warning(message)
                    ensure_spoken(message)
                    rar_result = None

            # The TemporaryDirectory context manager handles all cleanup of temp_dir
            logging.debug(f"Final rar_result: {rar_result}")
            return rar_result

        elif back_up_mode == PkModesForEnsurePnxBackedUp.GIT_HUB_BACK_UP:
            logging.info(f"GitHub 백업 모드를 선택했습니다. 대상: '{pnx_working}'를 '{d_destination}'에 백업합니다.")

            # Copy files from pnx_working to d_dst before pushing
            if pnx_working.is_dir():
                logging.info(f"'{pnx_working}' 내용을 '{d_destination}'로 복사합니다.")
                ensure_tree_copied_except_blacklist_and_including_whitelist(
                    d_working=pnx_working,
                    dst_dir=d_destination,
                    blacklist=blacklist  # Pass the (potentially interactive) blacklist
                )
            elif pnx_working.is_file():
                logging.info(f"'{pnx_working}' 파일을 '{d_destination}'로 복사합니다.")
                # ensure_pnx_made(d_dst, mode='d') # ensure_tree_copied handles directory creation
                shutil.copy2(pnx_working, d_destination / pnx_working.name)
            else:
                logging.error(f"백업 대상 '{pnx_working}'이 유효하지 않습니다.")
                ensure_spoken(f"백업 대상 '{pnx_working}'이 유효하지 않습니다.")
                return None

            # Call ensure_git_repo_pushed
            git_push_result = ensure_git_repo_pushed(d_local_repo=d_destination, pk_commit_mode=PkModes.MSP_COMMIT_MASSAGE_MODE)

            if git_push_result and git_push_result.get("state"):
                logging.info(f"GitHub 백업 완료: {d_destination}")
                return str(d_destination)
            else:
                logging.error(f"GitHub 백업 실패: {d_destination}")
                return None
        else:
            logging.error(f"알 수 없는 백업 모드: {back_up_mode.value}")
            ensure_spoken(f"알 수 없는 백업 모드: {back_up_mode.value}")
            return None

    except Exception as e:
        ensure_debugged_verbose(traceback, e)
    finally:
        ensure_spoken(read_finished_wait_mode=True)
