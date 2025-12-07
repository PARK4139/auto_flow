import inspect
import os
import re
import traceback

from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_functions.get_file_id import get_file_id
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pk_internal_tools.pk_functions.get_values_from_historical_file_routine import get_values_from_historical_file_routine
from pk_internal_tools.pk_functions.ensure_pk_log_initialized import ensure_pk_log_initialized
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_objects.pk_texts import PkTexts
from pk_internal_tools.pk_objects.pk_directories import D_PK_FUNCTIONS
from pk_internal_tools.pk_objects.pk_directories  import d_pk_root



def get_rename_map(d_working):
    part_pattern = re.compile(r"^(part_\d+_)(.+\.py)$")
    rename_map = {}
    for fname in os.listdir(d_working):
        match = part_pattern.match(fname)
        if match:
            new_name = match.group(2)
            rename_map[fname] = new_name
    return rename_map


def rename_files(d_working, rename_map, dry_run=True):
    updated_rename_map = {}
    for old_filename, new_filename in rename_map.items():
        old_path = os.path.join(d_working, old_filename)
        base, ext = os.path.splitext(new_filename)
        new_name = new_filename
        new_path = os.path.join(d_working, new_name)
        counter = 1
        while os.path.exists(new_path):
            new_name = f"{base}_DUPLICATED_{counter}{ext}"
            new_path = os.path.join(d_working, new_name)
            counter += 1
        updated_rename_map[old_filename] = new_name
        if dry_run:
            print(f"[{PkTexts.PREVIEW}] Rename: {old_filename} -> {new_name}")
        else:
            os.rename(old_path, new_path)
            print(f"[{PkTexts.RENAMED}] Rename: {old_filename} -> {new_name}")
    return updated_rename_map


def pk_ensure_target_filenames_renamed_from_prefix_xxx(mode=None):
    func_n = get_caller_name()
    if QC_MODE:
        d_working = D_PK_FUNCTIONS
    else:
        key_name = "d_working"
        d_working = get_values_from_historical_file_routine(file_id=get_file_id(key_name, func_n), key_hint=f'{key_name}', options=[D_PK_FUNCTIONS])
    if mode is None:
        if QC_MODE:
            exec_mode = PkTexts.EXECUTION
        else:
            exec_mode = ensure_value_completed_2025_10_12_0000(
                key_name=f"{PkTexts.MODE}=",
                options=[PkTexts.PREVIEW, PkTexts.EXECUTION]
            ).strip()
    else:
        exec_mode = mode
    dry_run = exec_mode == PkTexts.PREVIEW
    rename_map = get_rename_map(d_working)
    rename_files(d_working, rename_map, dry_run=dry_run)
    return rename_map


if __name__ == "__main__":
    try:
        ensure_pk_log_initialized(__file__=__file__)
        pk_ensure_target_filenames_renamed_from_prefix_xxx()
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
