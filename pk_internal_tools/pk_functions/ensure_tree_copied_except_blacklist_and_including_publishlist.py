from pathlib import Path
from typing import List, Iterable, Tuple, Set

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_tree_copied_except_blacklist_and_including_publishlist(
    d_working: Path,
    dst_dir: Path,
    blacklist: List[Path],
    publishlist: List[Path],
) -> Path | None:
    """
    Phase 1) COPY PUBLISH FIRST (override):
      - Expand publishlist (files + directories, wildcard supported).
      - Create ancestor dirs and copy files, ignoring blacklist.

    Phase 2) COPY DEFAULT (respect blacklist):
      - Walk source tree; copy everything except blacklist and already-copied publish items.

    Returns:
        dst_dir on success, None on error.
    """
    import os, shutil, logging, traceback

    from pk_internal_tools.pk_functions.is_path_covered_by_list import is_path_covered_by_list
    from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    try:
        # ---- sanitize ----
        blacklist = blacklist or []
        publishlist = publishlist or []
        d_working = Path(d_working).resolve()
        dst_dir = Path(dst_dir).resolve()

        def is_windows() -> bool:
            return os.name == "nt"

        def key(p: Path) -> str:
            s = str(p)
            return s.casefold() if is_windows() else s

        if d_working == dst_dir or d_working in dst_dir.parents:
            logging.debug(f"invalid copy: {d_working} -> {dst_dir}")
            return dst_dir

        dst_dir.mkdir(parents=True, exist_ok=True)

        # ---- build blacklist matchers ----
        auto_exclude_dirs = {
            Path(".git"), Path("__pycache__"), Path(".venv"),
            Path(".venv"), Path(".venv"), Path("node_modules"),
        }
        literal_excluded: Set[str] = set()
        grouped_excluded = {}

        for p in list(blacklist) + list(auto_exclude_dirs):
            p = Path(p)
            if any(sym in p.name for sym in ("*", "?")) or any(sym in p.stem for sym in ("*", "?")):
                base = (d_working / p.parent).resolve()
                grouped_excluded.setdefault(base, []).append(p.name)
            else:
                abs_p = (p if p.is_absolute() else (d_working / p)).resolve()
                literal_excluded.add(key(abs_p))

        def covered_by_blacklist(p: Path) -> bool:
            return is_path_covered_by_list(p.resolve(), literal_excluded, grouped_excluded)

        # ---- PUBLISH EXPANSION ----
        def expand_publish_entries(entries: List[Path]) -> Tuple[Set[Path], Set[Path]]:
            """Return (publish_dirs, publish_files) as absolute paths under d_working."""
            dirs: Set[Path] = set()
            files: Set[Path] = set()
            for raw in entries:
                item = (raw if Path(raw).is_absolute() else (d_working / raw)).resolve()
                # wildcard?
                if any(sym in Path(raw).name for sym in ("*", "?")) or any(sym in Path(raw).stem for sym in ("*", "?")):
                    base = (d_working / Path(raw).parent).resolve()
                    pat = Path(raw).name
                    if base.exists():
                        for m in base.glob(pat):
                            m = m.resolve()
                            if m.is_dir():
                                dirs.add(m)
                                for r, _, fs in os.walk(m):
                                    for fn in fs:
                                        files.add((Path(r) / fn).resolve())
                            elif m.is_file():
                                files.add(m)
                    else:
                        logging.warning(f"Publish glob base does not exist: {base}")
                else:
                    if item.exists():
                        if item.is_dir():
                            dirs.add(item)
                            for r, _, fs in os.walk(item):
                                for fn in fs:
                                    files.add((Path(r) / fn).resolve())
                        elif item.is_file():
                            files.add(item)
                    else:
                        logging.warning(f"Publish entry does not exist: {item}")
            return dirs, files

        publish_dirs, publish_files = expand_publish_entries(publishlist)

        # ---- Phase 1: COPY PUBLISH FIRST (ignore blacklist) ----
        copied_rel_keys: Set[str] = set()
        copied_count = 0

        def rel_of(p: Path) -> Path:
            return p.resolve().relative_to(d_working)

        # ensure publish dirs
        for d in sorted(publish_dirs, key=lambda p: len(p.parts)):
            try:
                (dst_dir / rel_of(d)).mkdir(parents=True, exist_ok=True)
                logging.debug(f"[CREATED DIR] (PUBLISH) {rel_of(d)}")
                copied_count += 1
            except Exception as e:
                logging.debug(traceback.format_exc())

        # copy publish files
        for f in sorted(publish_files, key=lambda p: len(p.parts)):
            try:
                rel = rel_of(f)
                dst_f = dst_dir / rel
                dst_f.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst_f)
                copied_rel_keys.add(key(rel))
                logging.debug(f"[COPIED FILE] (PUBLISH) {rel}")
                copied_count += 1
            except Exception as e:
                logging.debug(traceback.format_exc())

        # ---- Phase 2: COPY DEFAULT (respect blacklist, skip already-copied) ----
        normal_dirs: Set[Path] = set()
        normal_files: List[Path] = []

        for root, dirs, files in os.walk(d_working, topdown=True):
            root_path = Path(root).resolve()

            # prune dirs that are blacklisted; BUT keep publish ancestors so traversal continues
            keep = []
            for dn in dirs:
                d = (root_path / dn).resolve()
                # if directory itself is blacklisted, prune
                if covered_by_blacklist(d):
                    # 만약 퍼블리시가 이 안에 이미 복사되었더라도, Phase 2는 굳이 더 내려갈 필요 없음
                    continue
                keep.append(dn)
                normal_dirs.add(d)
            dirs[:] = keep

            for fn in files:
                f = (root_path / fn).resolve()
                rel = rel_of(f)
                if key(rel) in copied_rel_keys:
                    continue
                if covered_by_blacklist(f):
                    continue
                normal_files.append(f)

        # create remaining dirs & copy files
        for d in sorted(normal_dirs, key=lambda p: len(p.parts)):
            dst_d = dst_dir / rel_of(d)
            if not dst_d.exists():
                try:
                    dst_d.mkdir(parents=True, exist_ok=True)
                    logging.debug(f"[CREATED DIR] (DEFAULT) {rel_of(d)}")
                    copied_count += 1
                except Exception as e:
                    logging.debug(traceback.format_exc())

        for f in normal_files:
            rel = rel_of(f)
            if key(rel) in copied_rel_keys:
                continue
            try:
                dst_f = dst_dir / rel
                dst_f.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst_f)
                logging.debug(f"[COPIED FILE] (DEFAULT) {rel}")
                copied_rel_keys.add(key(rel))
                copied_count += 1
            except Exception as e:
                logging.debug(traceback.format_exc())

        logging.debug(f"[{PkTexts.DONE}] {copied_count} item(s) copied to '{dst_dir}'.")
        return dst_dir

    except Exception as e:
        ensure_debugged_verbose(traceback, e)
        return None
