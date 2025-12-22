from pathlib import Path
from typing import Union, List, Optional

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_tree_printed_as_preview(
        candidates: List[Union[str, Path]],
        *,
        use_color: bool = True,
        show_symlink_suffix: bool = True,
        dir_suffix: str = "/",
        indent_unit: str = "    ",
        return_text: bool = False,
        logger=None,
) -> Optional[str]:
    import os
    from pathlib import Path
    from typing import List

    if not candidates:
        msg = "(no candidates)"
        if logger:
            logger.info(msg)
        else:
            print(msg)
        return msg if return_text else None

    # Normalize to Path & resolve
    abs_list = [Path(c).resolve(strict=False) for c in candidates]

    # Windows: guard against different drives
    if os.name == "nt":
        drives = {p.drive.upper() for p in abs_list}
        if len(drives) > 1:
            raise ValueError(f"Candidates are on different drives {drives}; cannot render a single tree.")

    # Common base
    try:
        common = Path(os.path.commonpath([str(p) for p in abs_list]))
    except ValueError as e:
        raise ValueError("Candidates do not share a common base; cannot render a single tree.") from e
    if common.is_file():
        common = common.parent
    base = common

    # Relativize
    rels = [p.relative_to(base) for p in abs_list]

    # ---- Build tree
    TREE_FILES_KEY = "_files"
    TREE_DIRS_KEY = "_dirs"

    def _new_node():
        return {TREE_FILES_KEY: [], TREE_DIRS_KEY: {}}

    tree = _new_node()

    for rel in rels:
        parts = list(rel.parts)
        cursor = tree
        for i, name in enumerate(parts):
            at_end = i == len(parts) - 1
            if at_end:
                cursor[TREE_FILES_KEY].append(name)
            else:
                cursor = cursor[TREE_DIRS_KEY].setdefault(name, _new_node())

    # ---- Pretty print
    if use_color:
        C_DIR = "\033[94m"
        C_FILE = "\033[97m"
        C_RESET = "\033[0m"
    else:
        C_DIR = C_FILE = C_RESET = ""

    BRANCH, LAST, VERT, SPACE = "├── ", "└── ", "│   ", "    "
    lines: List[str] = []
    lines.append(str(base) + dir_suffix)

    def _render(node, prefix_stack: List[bool]):
        entries = sorted(node[TREE_DIRS_KEY].keys()) + sorted(node[TREE_FILES_KEY])
        total = len(entries)
        for idx, name in enumerate(entries):
            is_last = idx == total - 1
            branch = LAST if is_last else BRANCH
            spine = "".join(VERT if not last else SPACE for last in prefix_stack)

            if name in node[TREE_DIRS_KEY]:
                lines.append(f"{spine}{branch}{C_DIR}{name}{dir_suffix}{C_RESET}")
                _render(node[TREE_DIRS_KEY][name], prefix_stack + [is_last])
            else:
                lines.append(f"{spine}{branch}{C_FILE}{name}{C_RESET}")

    _render(tree, [])

    text = "\n".join(lines)
    if logger:
        logger.info(text)
    else:
        print(text)
    return text if return_text else None
