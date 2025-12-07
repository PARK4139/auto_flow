import os
import shutil


# TODO : 테스트 필요
def ensure_directory_destroyed_without_overwrite(
        working_dir: str,
        move_empty_dirs: bool = True,
        dest_dirname: str = "_destroyed",
        merged_empty_dirname: str = "empty_directory_merged"
) -> None:
    """
    Move all files under `working_dir` into `working_dir/dest_dirname` with rename on duplicates.
    Optionally move all empty directories into a single merged folder.
    """
    working_dir = os.path.abspath(working_dir)
    dest_root = os.path.join(working_dir, dest_dirname)
    os.makedirs(dest_root, exist_ok=True)

    if move_empty_dirs:
        empty_dir_dest = os.path.join(working_dir, merged_empty_dirname)
        os.makedirs(empty_dir_dest, exist_ok=True)

    for dirpath, dirnames, filenames in os.walk(working_dir, topdown=False):
        # Skip destination folders
        if os.path.abspath(dirpath) in {os.path.abspath(dest_root), os.path.abspath(os.path.join(working_dir, merged_empty_dirname))}:
            continue

        # Move files
        for filename in filenames:
            src_path = os.path.join(dirpath, filename)
            base_name, ext = os.path.splitext(filename)
            dst_path = os.path.join(dest_root, filename)

            counter = 1
            while os.path.exists(dst_path):
                dst_path = os.path.join(dest_root, f"{base_name}_{counter}{ext}")
                counter += 1

            shutil.move(src_path, dst_path)

        # Move empty directories if enabled
        if move_empty_dirs:
            if not os.listdir(dirpath):  # still empty
                basename = os.path.basename(dirpath)
                dst_path = os.path.join(empty_dir_dest, basename)
                counter = 1
                while os.path.exists(dst_path):
                    dst_path = os.path.join(empty_dir_dest, f"{basename}_{counter}")
                    counter += 1
                shutil.move(dirpath, dst_path)
