
"""
Robust directory scanner for Windows paths to find media files.
- Handles \\?\ prefix, trailing dots/spaces, hidden chars.
- Uses Path (cross-platform friendly)
- Lazy imports inside functions
- Standard logging format
"""

from __future__ import annotations

from typing import Iterable, List, Sequence, Union

from pk_internal_tools.pk_objects.pk_ttl_cache_manager import ensure_pk_ttl_cached

PathLike = Union[str, "Path"]


def _strip_quotes(s: str) -> str:
    if len(s) >= 2 and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
        return s[1:-1]
    return s


def _has_invalid_tail_segment_chars(segment: str) -> bool:
    if not segment:
        return False
    return segment.endswith(" ") or segment.endswith(".")


def _segments_with_issues(p_str: str) -> List[str]:
    from pathlib import PureWindowsPath
    segs = list(PureWindowsPath(p_str).parts)
    return [seg for seg in segs if _has_invalid_tail_segment_chars(seg)]


def _maybe_strip_win_longpath_prefix(p_str: str) -> str:
    prefix = r"\\?\\"
    if p_str.startswith(prefix):
        no_prefix = p_str[len(prefix):]
        return no_prefix
    return p_str


def _normalize_windows_path(p: PathLike) -> str:
    from pathlib import Path
    if isinstance(p, Path):
        p_str = str(p)
    else:
        p_str = str(p)

    p_str = _strip_quotes(p_str).replace("/", "\\")
    p_str = p_str.strip()
    p_str = _maybe_strip_win_longpath_prefix(p_str)
    return p_str


def _ensure_windows_extended_prefix_if_needed(p_str: str) -> str:
    return p_str


def _validate_path_for_winapi(p_str: str) -> None:
    bad_segs = _segments_with_issues(p_str)
    if bad_segs:
        raise OSError(
            123,
            f"Invalid path syntax: segment(s) end with space/dot: {bad_segs!r}",
            p_str,
        )

    illegal = set('<>:\"/|?*')
    from pathlib import PureWindowsPath
    p_win = PureWindowsPath(p_str)

    # Check drive part if it exists
    if p_win.drive:
        pass

    # Check root part if it exists
    if p_win.root:
        pass

    # Check the actual path segments (excluding drive and root)
    start_index = 0
    if p_win.drive or p_win.root:
        start_index = 1  # Skip the first element which is the combined drive and root

    for seg in p_win.parts[start_index:]:
        if any(ch in illegal for ch in seg):
            raise OSError(123, f"Invalid character in segment: {seg!r}", p_str)


def _match_patterns(path_obj, patterns: Sequence[str]) -> bool:
    name = path_obj.name
    # Convert extensions to glob patterns if they are not already
    glob_patterns = [pat if '*' in pat else f'*{pat}' for pat in patterns]
    for pat in glob_patterns:
        if path_obj.match(pat):
            return True
    return False



# pk_checkpoint
@ensure_pk_ttl_cached(ttl_seconds=60 * 1 * 1, maxsize=128) # pk_option
def get_filtered_media_files_v_2025_10_03(
        path_to_scan: PathLike,
        patterns: Sequence[str] = None,
        recursive: bool = True,
) -> List[str]:
    """
    Scan directory and return media files matching patterns.
    Combines video and audio extensions by default.
    Robust to Windows path quirks.
    """
    import logging
    from pathlib import Path
    from pk_internal_tools.pk_objects.pk_file_extensions import PK_FILE_EXTENSIONS

    if patterns is None:
        # Combine video and audio extensions from the central dictionary
        patterns = list(PK_FILE_EXTENSIONS['videos'] | PK_FILE_EXTENSIONS['audios'])

    try:
        p_str = _normalize_windows_path(path_to_scan)
        _validate_path_for_winapi(p_str)
        p_str = _ensure_windows_extended_prefix_if_needed(p_str)
        base = Path(p_str)

        if not base.exists():
            logging.warning("Path does not exist: %r", p_str)
            return []

        if not base.is_dir():
            logging.warning("Path is not a directory: %r", p_str)
            return []

        iter_paths: Iterable[Path] = base.rglob("*") if recursive else base.glob("*")

        results: List[str] = []
        for f in iter_paths:
            try:
                if f.is_file() and _match_patterns(f, patterns):
                    results.append(str(f))
            except OSError:
                continue

        return results

    except OSError as e:
        import logging
        logging.error("Failed to scan path. path=%r err=[WinError %s] %s",
                      path_to_scan, getattr(e, "winerror", "?"), e)
        try:
            s = str(path_to_scan)
            dbg = {
                "repr": repr(s),
                "length": len(s),
                "ord_tail": [ord(c) for c in s[-10:]],
                "has_prefix_\\?\\": s.startswith(r"\\?\\"),
            }
            logging.debug("Path debug: %s", dbg)
        except Exception as e:
            pass
        return []
    except Exception as e:
        import logging
        logging.exception("Unexpected error in get_filtered_media_files(%r): %s",
                          path_to_scan, e)
        return []
