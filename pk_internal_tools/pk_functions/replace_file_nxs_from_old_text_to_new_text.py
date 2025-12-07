import logging
import os
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_pnxs_renamed_2025_10_29 import ensure_pnxs_renamed_2025_10_29


def replace_file_nxs_from_old_text_to_new_text(d_working, old_text, new_text, target_type='both', with_walking: bool = True):
    """
    target_types =['files', 'both','directories', 'both']

    Finds items in a directory and renames them by replacing old_text with new_text.
    Can filter by type (files, directories, or both).
    Search can be recursive (with_walking=True) or top-level only (with_walking=False).
    """
    if not old_text or '%%' in old_text:
        logging.warning("Invalid old_text provided. Aborting rename.")
        return

    if not new_text or '%%' in new_text:
        logging.warning("Invalid new_text provided. Aborting rename.")
        return

    d_working_path = Path(d_working)
    if not d_working_path.is_dir():
        logging.error(f"Working directory not found: {d_working}")
        return

    to_rename_list = []
    
    if with_walking:
        # Iterate in reverse order (bottom-up) to handle directory renames correctly
        for root, dirs, files in os.walk(d_working, topdown=False):
            items_to_check = []
            if target_type in ['files', 'both']:
                items_to_check.extend(files)
            if target_type in ['directories', 'both']:
                items_to_check.extend(dirs)

            for name in items_to_check:
                if old_text in name:
                    src_path = Path(root) / name
                    # Check if path exists to avoid issues with already renamed parent dirs
                    if src_path.exists():
                        new_name = name.replace(old_text, new_text)
                        dst_path = Path(root) / new_name
                        to_rename_list.append((str(src_path), str(dst_path)))
    else: # without_walking
        root_path = Path(d_working)
        all_items = list(root_path.iterdir())
        
        dirs = [d.name for d in all_items if d.is_dir()]
        files = [f.name for f in all_items if f.is_file()]

        items_to_check = []
        if target_type in ['files', 'both']:
            items_to_check.extend(files)
        if target_type in ['directories', 'both']:
            items_to_check.extend(dirs)

        for name in items_to_check:
            if old_text in name:
                src_path = root_path / name
                if src_path.exists():
                    new_name = name.replace(old_text, new_text)
                    dst_path = root_path / new_name
                    to_rename_list.append((str(src_path), str(dst_path)))

    if to_rename_list:
        logging.info(f"Found {len(to_rename_list)} items to rename.")
        ensure_pnxs_renamed_2025_10_29(to_rename_list)
    else:
        logging.info("No items found to rename with the given criteria.")
