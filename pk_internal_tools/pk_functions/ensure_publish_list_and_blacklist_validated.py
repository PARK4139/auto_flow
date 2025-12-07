from pathlib import Path
from typing import Iterable, List, Set, Tuple

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_publish_list_and_blacklist_validated(
    *,
    d_dst: Path,
    blacklist: List[Path],
    publishlist: List[Path],
) -> bool:
    """
    Validation rules (post-copy):
      1) Blacklisted FILE present in destination -> FAIL,
         unless the exact file is also in publish expanded set -> ALLOW.
      2) Blacklisted DIR present in destination:
         - If it's an ancestor of any publish path -> ALLOW **if** the dir contains ONLY publish files/dirs.
         - If it contains any non-publish file -> FAIL.
         - Otherwise (no publish relation) -> FAIL on existence.

    Notes:
      - `blacklist` and `publishlist` are expected as **dst-relative** paths by the caller.
      - Wildcards supported in the last segment of entries (same policy as copy phase).
    """
    import os
    import logging

    d_dst = Path(d_dst).resolve()

    # ---------- helpers ----------
    def expand_entries(base: Path, entries: Iterable[Path]) -> Tuple[Set[Path], Set[Path]]:
        """Expand (dirs, files) under base for mixed (literal / wildcard) entries."""
        dirs: Set[Path] = set()
        files: Set[Path] = set()
        for raw in entries:
            raw = Path(raw)
            abs_item = (base / raw).resolve()
            if any(sym in raw.name for sym in ("*", "?")) or any(sym in raw.stem for sym in ("*", "?")):
                abs_base = (base / raw.parent).resolve()
                if not abs_base.exists():
                    continue
                for m in abs_base.glob(raw.name):
                    m = m.resolve()
                    if m.is_dir():
                        dirs.add(m)
                        for r, _, fs in os.walk(m):
                            for fn in fs:
                                files.add((Path(r) / fn).resolve())
                    elif m.is_file():
                        files.add(m)
            else:
                if abs_item.exists():
                    if abs_item.is_dir():
                        dirs.add(abs_item)
                        for r, _, fs in os.walk(abs_item):
                            for fn in fs:
                                files.add((Path(r) / fn).resolve())
                    elif abs_item.is_file():
                        files.add(abs_item)
        return dirs, files

    def all_ancestors_of(paths: Iterable[Path], stop_at: Path) -> Set[Path]:
        out: Set[Path] = set()
        stop_at = stop_at.resolve()
        for p in paths:
            p = p.resolve()
            cur = p
            while True:
                cur = cur.parent
                if cur == stop_at or stop_at not in cur.parents and cur != stop_at:
                    break
                out.add(cur)
                if cur == stop_at:
                    break
        return out

    # ---------- expand publish under destination ----------
    pub_dirs, pub_files = expand_entries(d_dst, publishlist)
    pub_paths = pub_dirs | pub_files
    pub_ancestors = all_ancestors_of(pub_paths, d_dst)

    # quick key set for membership
    def k(p: Path) -> str:
        s = str(p.resolve())
        return s.casefold() if os.name == "nt" else s

    pub_file_keys = {k(p) for p in pub_files}
    pub_dir_keys = {k(p) for p in pub_dirs}
    pub_ancestor_keys = {k(p) for p in pub_ancestors}

    # ---------- scan blacklist presence ----------
    # n. files
    bl_dirs, bl_files = set(), set()
    for entry in blacklist:
        e = (d_dst / entry).resolve()
        # wildcard?
        if any(sym in entry.name for sym in ("*", "?")) or any(sym in entry.stem for sym in ("*", "?")):
            base = (d_dst / entry.parent).resolve()
            if base.exists():
                for m in base.glob(entry.name):
                    (bl_dirs if m.is_dir() else bl_files).add(m.resolve())
        else:
            if e.exists():
                (bl_dirs if e.is_dir() else bl_files).add(e)

    # ---- files: strict unless explicitly published ----
    for f in bl_files:
        if k(f) in pub_file_keys:
            # allowed: blacklisted file explicitly published
            continue
        logging.debug(f"Blacklist leaked FILE into destination: {f.relative_to(d_dst)}")
        return False

    # ---- dirs: allow if (ancestor of publish) AND contains only published content ----
    for d in bl_dirs:
        d_key = k(d)
        if (d_key in pub_dir_keys) or (d_key in pub_ancestor_keys):
            # check contents: must all be published files/dirs
            for r, ds, fs in os.walk(d):
                r_path = Path(r).resolve()
                for fn in fs:
                    f = (r_path / fn).resolve()
                    if k(f) not in pub_file_keys:
                        logging.debug(
                            f"Blacklist dir contains NON-publish file: "
                            f"{f.relative_to(d_dst)} under {d.relative_to(d_dst)}"
                        )
                        return False
            # only publish content -> ok
            continue

        # not related to publish -> existence itself is a leak
        logging.debug(f"Blacklist leaked DIR into destination: {d.relative_to(d_dst)}")
        return False

    return True
