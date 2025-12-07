from pathlib import Path


def is_path_covered_by_list(item_path: Path, literal_paths: set[str], grouped_glob_patterns: dict[Path, list[str]]) -> bool:
    from fnmatch import fnmatch
    from pathlib import Path

    # item_path_str = str(item_path.resolve()).casefold()

    # Check against literal paths (exact match or child of a blacklisted directory)
    for literal_path_str in literal_paths:
        literal_path_obj = Path(literal_path_str)
        if item_path == literal_path_obj or item_path.is_relative_to(literal_path_obj):
            return True

    # Check against grouped glob patterns
    for base_path_resolved, patterns in grouped_glob_patterns.items():
        if item_path.is_relative_to(base_path_resolved):
            relative_path_to_base = item_path.relative_to(base_path_resolved)
            for pattern_string in patterns:
                if fnmatch(str(relative_path_to_base), pattern_string):
                    return True
    return False
