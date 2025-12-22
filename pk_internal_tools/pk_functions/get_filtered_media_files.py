from os import PathLike
from typing import Sequence, List


def get_files_filtered_from_db(
        directory_to_scan: PathLike,
        allowed_extensions: Sequence[str],
        name_parts_to_ignore: List[str] = None,
        regex_patterns_to_ignore: List[str] = None,
        with_sync: bool = False,
        use_db: bool = True
):
    """
    Gets filtered media files.
    By default, it tries to use the fast DB query (use_db=True).
    If use_db is False or the DB query fails, it falls back to a direct file system scan.
    """
    import logging
    from pathlib import Path

    if use_db:
        try:
            from .ensure_media_db_synced import get_files_from_db

            # Provide default empty lists if None
            if name_parts_to_ignore is None:
                name_parts_to_ignore = []
            if regex_patterns_to_ignore is None:
                regex_patterns_to_ignore = []

            return get_files_from_db(
                d_working=Path(directory_to_scan),
                allowed_extensions=list(allowed_extensions) if allowed_extensions else [],
                name_parts_to_ignore=name_parts_to_ignore,
                regex_patterns_to_ignore=regex_patterns_to_ignore,
                with_sync=with_sync
            )
        except Exception as e:
            logging.warning(f"DB-based media file search failed: {e}. Falling back to direct scan.")
            # Fallback to the other function

    # Fallback implementation
    logging.info("Using fallback direct file system scan.")
    from pk_internal_tools.pk_functions.get_filtered_media_files_v_2025_10_03 import get_filtered_media_files_v_2025_10_03
    # The fallback function's signature is unknown, but we adapt to what the old wrapper was trying to do.
    return get_filtered_media_files_v_2025_10_03(
        directory_to_scan,
        patterns=allowed_extensions,
        recursive=True
    )
