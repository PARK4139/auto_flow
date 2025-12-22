#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Set

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


# -----------------------------
# Lazy imports (keeps import-time side effects minimal)
# -----------------------------
def _lazy_modulefinder():
    import modulefinder  # type: ignore
    return modulefinder


def _lazy_send2trash():
    try:
        from send2trash import send2trash  # type: ignore
        return send2trash
    except Exception as e:
        return None


# -----------------------------
# Utilities
# -----------------------------
def relpath(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except Exception as e:
        return str(path.resolve())


def normalize_paths(paths: Iterable[Path]) -> Set[Path]:
    return {p.resolve() for p in paths}


def iter_all_py_files(project_root: Path, safe_filter: bool = True) -> Set[Path]:
    """
    Collect all .py files under project_root, optionally applying a safety filter
    to exclude common directories like venv/.git/tests/build/dist/__pycache__.
    """
    import os

    skip_dirs = {".git", "__pycache__", "build", "dist", ".eggs", ".mypy_cache", ".pytest_cache"}
    venv_prefixes = (".venv", "venv", ".venv", ".venv")

    all_files: Set[Path] = set()
    for root, dirs, files in os.walk(project_root):
        root_path = Path(root)

        if safe_filter:
            # prune directories in-place for faster traversal
            dirs[:] = [
                d for d in dirs
                if d not in skip_dirs
                   and not any(d.startswith(vp) for vp in venv_prefixes)
                   and d != "tests"
            ]

        for f in files:
            if f.endswith(".py"):
                all_files.add((root_path / f).resolve())

    return all_files


# -----------------------------
# Import tracing
# -----------------------------
def get_imported_files_from_entrypoint(entrypoint: Path) -> Set[Path]:
    """
    Use modulefinder to collect .py files imported when running the entry script.
    WARNING: This executes the top-level of the entry script.
    """
    import logging
    from pathlib import Path as _Path

    modulefinder = _lazy_modulefinder()
    finder = modulefinder.ModuleFinder()
    try:
        finder.run_script(str(entrypoint))
    except Exception as e:
        # Allow partial graph; dynamic imports or runtime errors may occur.
        logging.warning(f"run_script raised during analysis: entry='{entrypoint}' err='{e}'")

    imported_files: Set[Path] = set()
    for _, mod in finder.modules.items():
        f = getattr(mod, "__file__", None)
        if not f:
            continue
        # Only track pure .py files (ignore .pyc/.so/.pyd etc.)
        try:
            p = _Path(f)
            if p.suffix == ".py":
                imported_files.add(p.resolve())
        except Exception as e:
            # Ignore any path issues silently
            pass
    return imported_files


def get_imported_files_from_entrypoints(entrypoints: Iterable[Path]) -> Set[Path]:
    import logging

    used: Set[Path] = set()
    for ep in entrypoints:
        logging.debug(f"[TRACE] analyzing entrypoint: {ep}")
        used |= get_imported_files_from_entrypoint(ep)
    return used


# -----------------------------
# Deletion & pruning
# -----------------------------
def delete_files(files: Iterable[Path], use_trash: bool, dry_run: bool, project_root: Path) -> None:
    import os
    import logging

    send2trash = _lazy_send2trash() if use_trash else None

    for f in sorted(files):
        rel = relpath(f, project_root)
        if dry_run:
            logging.debug(f"[DRY-RUN] Would remove | rel='{rel}' abs='{f}'")
            continue

        try:
            if send2trash is not None:
                send2trash(str(f))
                logging.debug(f"[REMOVED (trash)] rel='{rel}' abs='{f}'")
            else:
                os.remove(f)
                logging.debug(f"[REMOVED] rel='{rel}' abs='{f}'")
        except FileNotFoundError:
            logging.debug(f"[SKIP] already missing | rel='{rel}' abs='{f}'")
        except IsADirectoryError:
            logging.debug(f"[SKIP] is a directory (file expected) | rel='{rel}' abs='{f}'")
        except Exception as e:
            logging.error(f" remove failed | rel='{rel}' abs='{f}' err='{e}'")


def prune_empty_dirs(root: Path, dry_run: bool) -> None:
    """
    Remove empty directories bottom-up. Logs every directory considered.
    """
    import os
    import logging

    for current_root, dirs, files in os.walk(root, topdown=False):
        current = Path(current_root)
        try:
            # If directory has no files and no subdirs after pruning
            if not files and not dirs:
                if dry_run:
                    logging.debug(f"[DRY-RUN] Would rmdir: '{current}'")
                else:
                    current.rmdir()
                    logging.debug(f"[RMDIR] '{current}'")
        except Exception as e:
            logging.error(f" rmdir failed | '{current}' err='{e}'")


# -----------------------------
# Public API
# -----------------------------
@ensure_seconds_measured
def ensure_python_file_unused_clean(
    project_root: Path,
    entrypoints: Iterable[Path],
    execute: bool = False,
    trash: bool = False,
    prune_empty_dirs_flag: bool = False,
    safe_filter: bool = True,
    extra_keep: Iterable[str] | None = None,
) -> bool:
    """
    Delete .py files not imported from given entrypoint(s).
    All logs are emitted via logging.debug. No logging config is set here.

    Args:
        project_root: Project root directory.
        entrypoints: Iterable of entry script paths (absolute or relative to project_root).
        execute: If True, actually delete files. If False, DRY-RUN only.
        trash: If True and send2trash is available, move files to OS trash.
        prune_empty_dirs_flag: If True, prune empty directories after deletion.
        safe_filter: If True, skip common dirs like .git/__pycache__/build/dist/tests/venv*.
        extra_keep: Optional glob patterns (relative to project_root) to additionally keep.

    Returns:
        True on success; False on validation failure or unexpected exception.
    """
    import logging
    import traceback
    from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose  # keep project-local helper

    try:
        # Normalize and validate project_root
        project_root = project_root.resolve()
        if not project_root.exists() or not project_root.is_dir():
            logging.error(f" project_root not found or not a directory: '{project_root}'")
            return False

        # Normalize entrypoints
        eps_resolved: Set[Path] = set()
        for ep in entrypoints:
            ep_path = Path(ep)
            if not ep_path.is_absolute():
                ep_path = (project_root / ep_path)
            ep_path = ep_path.resolve()
            eps_resolved.add(ep_path)

        missing_eps = [str(ep) for ep in eps_resolved if not ep.exists()]
        if missing_eps:
            for ep in missing_eps:
                logging.error(f" entrypoint not found: '{ep}'")
            return False

        # Collect all .py files and used/imported .py files
        all_py = iter_all_py_files(project_root, safe_filter=safe_filter)
        logging.info(f"project_root='{project_root}'")
        logging.info(f"total .py files discovered={len(all_py)} (safe_filter={safe_filter})")

        used_py = get_imported_files_from_entrypoints(eps_resolved)
        logging.info(f"total imported .py from entrypoints={len(used_py)}")

        # Ensure entrypoint files themselves are treated as used
        used_py |= normalize_paths(eps_resolved)

        # Apply extra keep patterns (relative to project_root)
        if extra_keep:
            extra_keep_set: Set[Path] = set()
            for pattern in extra_keep:
                for p in project_root.glob(pattern):
                    if p.is_file() and p.suffix == ".py":
                        extra_keep_set.add(p.resolve())
            if extra_keep_set:
                logging.info(f"extra keep count={len(extra_keep_set)}")
                used_py |= extra_keep_set

        # Compute unused set limited to project tree
        unused_py = {p for p in all_py if p.resolve() not in used_py}

        # Log summary lists (relative + absolute)
        logging.debug("========== USED (.py) ==========")
        for p in sorted(used_py):
            if project_root in p.parents or p == project_root:
                logging.debug(f"[USED]   rel='{relpath(p, project_root)}' abs='{p}'")

        logging.debug("========== UNUSED CANDIDATES (.py) ==========")
        for p in sorted(unused_py):
            logging.debug(f"[UNUSED] rel='{relpath(p, project_root)}' abs='{p}'")

        dry_run = not execute
        logging.debug(f"[SUMMARY] used={len(used_py)} unused={len(unused_py)} total={len(all_py)} dry_run={dry_run}")

        # Delete unused
        delete_files(unused_py, use_trash=trash, dry_run=dry_run, project_root=project_root)

        # Optionally prune empty dirs
        if prune_empty_dirs_flag:
            prune_empty_dirs(project_root, dry_run=dry_run)

        return True

    except Exception as e:
        # Project-local verbose traceback handler
        ensure_debugged_verbose(traceback, e)
        return False
