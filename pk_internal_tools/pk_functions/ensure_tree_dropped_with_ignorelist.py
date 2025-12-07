from pathlib import Path
from typing import Union, List, Dict, Optional

from pk_internal_tools.pk_functions.ensure_tree_printed_as_preview import ensure_tree_printed_as_preview
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_tree_dropped_with_ignorelist(
        d_target: Union[str, Path],
        ignorelist: Optional[List[Path]] = None,
        dry_run: bool = True,
        remove_hidden: bool = True,
        follow_symlinks: bool = False,
) -> Dict[str, List[str]]:
    import os, shutil, stat, logging, traceback

    # lazy logging init
    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO,
                            format="%(levelname)s %(filename)s:%(lineno)d %(message)s")

    d_target = Path(d_target).resolve()
    if not d_target.exists() or not d_target.is_dir():
        raise NotADirectoryError(f"Target dir not found: {d_target}")

    # Normalize ignorelist
    ignorelist = [Path(p).resolve() for p in (ignorelist or [])]

    def is_hidden_name(name: str) -> bool:
        return name.startswith(".")

    def make_writable(p: Path) -> None:
        try:
            mode = p.stat().st_mode
            p.chmod(mode | stat.S_IWUSR | stat.S_IXUSR)
        except Exception:
            pass

    files_or_links, dirs = [], []
    for p in d_target.rglob("*"):
        try:
            if p in ignorelist:
                continue
            if any(ig in p.parents for ig in ignorelist):
                continue
            if not remove_hidden and is_hidden_name(p.name):
                continue

            st = p.lstat()
            if stat.S_ISDIR(st.st_mode):
                dirs.append(p)
            else:
                files_or_links.append(p)
        except Exception:
            continue

    dirs.sort(key=lambda x: len(x.parts), reverse=True)

    candidates_to_drop = [str(p) for p in files_or_links + dirs]
    deleted_files, deleted_dirs, skipped, errors = [], [], [], []

    if dry_run:
        logging.info(f"[dry-run] len(candidates_to_drop)={len(candidates_to_drop)}")
        ensure_tree_printed_as_preview(candidates_to_drop)
        return {
            "deleted_files": deleted_files,
            "deleted_dirs": deleted_dirs,
            "skipped": skipped,
            "candidates_to_drop": candidates_to_drop,
            "errors": errors,
        }

    for p in files_or_links:
        try:
            if p.is_symlink() and not follow_symlinks:
                p.unlink(missing_ok=True)
            else:
                if p.exists():
                    make_writable(p)
                    p.unlink(missing_ok=True)
            deleted_files.append(str(p))
        except Exception as e:
            errors.append(f"file del failed {p} | {e}\n{traceback.format_exc()}")

    for p in dirs:
        try:
            if p.is_symlink() and not follow_symlinks:
                p.unlink(missing_ok=True)
            else:
                if p.exists():
                    try:
                        p.rmdir()
                    except OSError:
                        for root, _, files in os.walk(p, topdown=False):
                            for name in files:
                                make_writable(Path(root) / name)
                        shutil.rmtree(p)
            deleted_dirs.append(str(p))
        except Exception as e:
            errors.append(f"dir del failed {p} | {e}\n{traceback.format_exc()}")

    logging.info(f"Cleared under {d_target} | files={len(deleted_files)} dirs={len(deleted_dirs)} errors={len(errors)}")
    return {
        "deleted_files": deleted_files,
        "deleted_dirs": deleted_dirs,
        "skipped": skipped,
        "candidates_to_drop": candidates_to_drop,
        "errors": errors,
    }
