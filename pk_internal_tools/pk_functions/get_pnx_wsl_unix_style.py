from pathlib import Path
from typing import Union, Optional


def get_pnx_wsl_unix_style(pnx: Union[str, Path]) -> Optional[str]:
    """
    Resolve a Windows path to a WSL POSIX path by:
      1) chdir to the target (dir or parent of file),
      2) querying WSL: `wsl --cd "<cwd>" -- pwd`,
      3) restoring original cwd in a `finally` block,
      4) returning POSIX string (NOT Path!) to avoid backslash conversion on Windows.

    Returns:
        str POSIX path like '/mnt/c/Users/...' on success, or None on failure.
    """
    # lazy imports (keep your style)
    import os
    import subprocess
    import logging
    import posixpath  # for safe POSIX join (never backslashes)

    # Snapshot original CWD (must be restored)
    origin_cwd = Path.cwd()

    try:
        p = Path(pnx)

        # We want absolute Windows path, but target may not exist (e.g., new file to be created).
        # So resolve() without strict to normalize, then check existence separately.
        try:
            p_abs = p.resolve(strict=False)
        except Exception:
            p_abs = p

        # Decide chdir target: directory itself, or parent of a file
        is_existing = p_abs.exists()
        is_dir = p_abs.is_dir() if is_existing else (p.suffix == "" and not p.name)  # best-effort for non-existing
        if is_existing:
            chdir_target = p_abs if p_abs.is_dir() else p_abs.parent
        else:
            # If not exists, chdir to parent (must exist) or bail out
            chdir_target = (p_abs if p_abs.name == "" else p_abs.parent)

        if not chdir_target.exists():
            logging.error(f"chdir target does not exist: {chdir_target}")
            return None

        # Change to target directory
        os.chdir(chdir_target)

        # Ask WSL to map the current Windows CWD to a POSIX path
        proc = subprocess.run(
            ["wsl", "--cd", str(chdir_target), "--", "pwd"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if proc.returncode != 0:
            logging.error(
                f"'wsl --cd ... pwd' failed for {chdir_target} "
                f"(exit={proc.returncode})\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
            )
            return None

        wsl_dir = (proc.stdout or "").strip().splitlines()[-1].strip()
        if not wsl_dir.startswith("/"):
            logging.error(f"Invalid WSL path from pwd: '{wsl_dir}' for {chdir_target}")
            return None

        # If original pnx was a file, append the basename on POSIX side
        if is_existing and p_abs.is_file():
            return posixpath.join(wsl_dir, p_abs.name)
        if (not is_existing) and p.suffix:  # non-existing file with extension
            return posixpath.join(wsl_dir, p.name)

        # Directory (existing or intended): return the directory POSIX path
        return wsl_dir

    except Exception as e:
        import logging
        logging.error(f"get_pnx_wsl_unix_style failed: {e}")
        return None

    finally:
        # Always restore original CWD
        try:
            os.chdir(origin_cwd)
        except Exception as e:
            import logging
            logging.warning(f"[PkTexts2025.WARN] Failed to restore CWD to {origin_cwd}: {e}")
