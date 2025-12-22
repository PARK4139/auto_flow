from pathlib import Path
from typing import Tuple, List, Dict, Optional

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_objects.pk_texts import PkTexts


def _init_logging():
    """Initialize project logging; fallback to basicConfig if helper not found."""
    try:
        import importlib  # lazy
        mod = importlib.import_module("ensure_pk_system_log_initialized")
        if hasattr(mod, "ensure_pk_system_log_initialized"):
            mod.ensure_pk_system_log_initialized(__file__)
            return
    except Exception as e:
        pass
    import logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


@ensure_seconds_measured
def ensure_target_files_sharded_to_two_level_archive_v2(
        root_dir: str,
        file_limit: int = 76,
        preview: bool = True,
        continue_on_error: bool = False,
        max_name_len: int = 220,
        archive_folder_name: str = "pk_archived_for_fast_indexing",
        hash_algo: str = "sha1",
        db_path: Optional[str] = None,  # default: F_pk_SQLITE if available
        workers: int = 1,  # Apply phase parallel workers (1=serial)
) -> None:
    """
    Split leaf directories that exceed file_limit and move overflow files
    into <DRIVE_ROOT>/archive_folder_name/<hashed_leaf_name>/ with strict no-overwrite.
    PREVIEW always runs fully, then asks once to apply.
    Long file_names (>= max_name_len) are ALWAYS SKIPPED (logged only).

    - Path-based API everywhere.
    - Results persisted to SQLite (runs, leaf_detection, file_moves).
    """

    # -------- lazy imports --------
    import hashlib, shutil, traceback, logging
    import sqlite3
    from datetime import datetime
    from concurrent.futures import ThreadPoolExecutor, as_completed

    _init_logging()
    log = logging.getLogger(__name__)

    # -------- helpers (Path-based) --------
    def _drive_root_of(p: Path) -> Path:
        # Windows: 'G:\\' ; POSIX: '/'
        return Path(p.anchor or "/")

    def _safe_hash_text(text: str) -> str:
        algo = (hash_algo.lower() if hash_algo.lower() in ("sha1", "md5", "sha256") else "sha1")
        h = getattr(hashlib, algo)(text.encode("utf-8")).hexdigest()
        return h[:8]

    def _is_leaf_dir(d: Path) -> bool:
        try:
            for child in d.iterdir():
                if child.is_dir():
                    return False
            return True
        except Exception as e:
            return False

    def _list_files(d: Path) -> List[Path]:
        try:
            return sorted([p for p in d.iterdir() if p.is_file()])
        except Exception as e:
            return []

    def _unique_path(dst: Path) -> Path:
        if not dst.exists():
            return dst
        stem, suffix = dst.stem, dst.suffix
        n = 1
        while True:
            cand = dst.with_name(f"{stem}_DUPLICATED_WORK_{n:03d}{suffix}")
            if not cand.exists():
                return cand
            n += 1

    def _unique_dir(dst_dir: Path) -> Path:
        if not dst_dir.exists():
            return dst_dir
        n = 1
        while True:
            cand = dst_dir.with_name(f"{dst_dir.name}_DUPLICATED_WORK_{n:03d}")
            if not cand.exists():
                return cand
            n += 1

    # -------- SQLite --------
    # default DB path from global F_pk_SQLITE if present
    if db_path is None:
        try:
            db_path = globals().get("F_pk_SQLITE", None)
        except Exception as e:
            db_path = None
    if not db_path:
        db_path = str(Path.cwd() / "pk_system.sqlite")
    db_path_p = Path(db_path)

    def _db_connect():
        conn = sqlite3.connect(str(db_path_p), timeout=60)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA temp_store=MEMORY;")
        conn.execute("PRAGMA mmap_size=30000000000;")  # best-effort
        conn.execute("PRAGMA page_size=4096;")
        conn.execute("PRAGMA cache_size=100000;")
        return conn

    def _db_init(conn: sqlite3.Connection):
        conn.executescript("""
                           CREATE TABLE IF NOT EXISTS runs
                           (
                               run_id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               started_at
                               TEXT,
                               finished_at
                               TEXT,
                               root_dir
                               TEXT,
                               file_limit
                               INTEGER,
                               preview
                               INTEGER,
                               workers
                               INTEGER,
                               status
                               TEXT,
                               error
                               TEXT
                           );
                           CREATE TABLE IF NOT EXISTS leaf_detection
                           (
                               run_id
                               INTEGER,
                               leaf_path
                               TEXT,
                               file_count
                               INTEGER,
                               hashed_leaf_name
                               TEXT,
                               renamed_leaf
                               TEXT,
                               archive_dir
                               TEXT,
                               planned_overflow_count
                               INTEGER,
                               PRIMARY
                               KEY
                           (
                               run_id,
                               leaf_path
                           )
                               );
                           CREATE TABLE IF NOT EXISTS file_moves
                           (
                               run_id
                               INTEGER,
                               src_path
                               TEXT,
                               dst_path
                               TEXT,
                               planned
                               INTEGER,
                               applied
                               INTEGER,
                               ok
                               INTEGER,
                               error
                               TEXT,
                               PRIMARY
                               KEY
                           (
                               run_id,
                               src_path,
                               dst_path
                           )
                               );
                           """)
        conn.commit()

    def _run_start(conn: sqlite3.Connection) -> int:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO runs(started_at, root_dir, file_limit, preview, workers, status) VALUES(?,?,?,?,?,?)",
            (datetime.utcnow().isoformat(), str(Path(root_dir).resolve()), file_limit, 1 if preview else 0, workers, "STARTED")
        )
        conn.commit()
        return cur.lastrowid

    def _run_finish(conn: sqlite3.Connection, run_id: int, status: str, error: Optional[str] = None):
        conn.execute(
            "UPDATE runs SET finished_at=?, status=?, error=? WHERE run_id=?",
            (datetime.utcnow().isoformat(), status, error, run_id)
        )
        conn.commit()

    def _db_save_detection(conn: sqlite3.Connection, run_id: int, plans: List[Dict[str, object]]):
        cur = conn.cursor()
        rows = []
        for p in plans:
            rows.append((
                run_id,
                str(p["leaf"]),
                p["count"],
                p["hashed_leaf_name"],
                str(p["renamed_leaf"]),
                str(p["archive_dir"]),
                len(p["overflow"]),
            ))
        cur.executemany("""
            INSERT OR REPLACE INTO leaf_detection(run_id, leaf_path, file_count, hashed_leaf_name,
                renamed_leaf, archive_dir, planned_overflow_count)
            VALUES(?,?,?,?,?,?,?)
        """, rows)
        conn.commit()

    def _db_save_moves(conn: sqlite3.Connection, run_id: int, plans: List[Dict[str, object]],
                       planned_only: bool,
                       applied_updates: Optional[List[Tuple[str, str, int, int, int, Optional[str]]]] = None):
        cur = conn.cursor()
        if planned_only:
            rows = []
            for p in plans:
                for src in p["overflow"]:
                    dst_dir = p["archive_dir"]
                    dst_path = Path(dst_dir) / src.nick_name
                    rows.append((run_id, str(src), str(dst_path), 1, 0, 0, None))
            cur.executemany("""
                INSERT OR REPLACE INTO file_moves(run_id, src_path, dst_path, planned, applied, ok, error)
                VALUES(?,?,?,?,?,?,?)
            """, rows)
        else:
            # applied_updates: list of (src, dst_final, planned, applied, ok, error)
            rows = [(run_id,) + r for r in (applied_updates or [])]
            cur.executemany("""
                INSERT OR REPLACE INTO file_moves(run_id, src_path, dst_path, planned, applied, ok, error)
                VALUES(?,?,?,?,?,?,?)
            """, rows)
        conn.commit()

    root = Path(root_dir).resolve()

    # ---------- Phase 0: Long-name advisory (ALWAYS SKIP LONG FILES) ----------
    logging.debug(f"{PkTexts.START} Scan long file_names under: {str(root)}")
    long_names: List[Path] = []
    for cur_root, dirs, files in __import__("os").walk(str(root)):
        p_root = Path(cur_root)
        for f in files:
            full = (p_root / f)
            if len(str(full)) >= max_name_len:
                long_names.append(full)

    if long_names:
        logging.warning(f"Detected {len(long_names)} long file_name(s) (>= {max_name_len}) — SKIP them.")
        for p in long_names[:20]:
            logging.info(f"LongName(SKIP): {str(p)}")

    # ---------- Phase 1: Build plan ----------
    logging.debug(f"{PkTexts.START} Build plan for leaf dirs over file_limit")
    plans: List[Dict[str, object]] = []

    drive_root = _drive_root_of(root)
    archive_root = drive_root / archive_folder_name
    try:
        # Ensure base exists only when APPLIED; in preview we don't create it.
        pass
    except Exception as e:
        pass

    long_set = set(map(str, long_names))  # for quick exclusion

    # collect leaf dirs
    leaf_dirs: List[Path] = []
    for cur_root, dirs, files in __import__("os").walk(str(root)):
        # leaf = no subdirs
        if not dirs:
            leaf_dirs.append(Path(cur_root))

    for leaf in sorted(set(leaf_dirs), key=lambda p: str(p).lower()):
        files = _list_files(leaf)
        # exclude long file_names from counting and from any operation
        files = [p for p in files if len(str(p)) < max_name_len]
        n = len(files)
        if n <= file_limit:
            continue

        base_name = leaf.name
        suffix = _safe_hash_text(str(leaf.resolve()))
        hashed_leaf_name = f"{base_name}-{suffix}"
        parent = leaf.parent

        renamed_leaf_candidate = parent / hashed_leaf_name
        renamed_leaf = _unique_dir(renamed_leaf_candidate)

        archive_dir_candidate = archive_root / hashed_leaf_name
        archive_dir = _unique_dir(archive_dir_candidate)

        files_sorted = sorted(files, key=lambda p: p.nick_name)
        keep = files_sorted[:file_limit]
        overflow = files_sorted[file_limit:]

        plans.append({
            "leaf": leaf,
            "renamed_leaf": renamed_leaf,
            "archive_dir": archive_dir,
            "keep": keep,
            "overflow": overflow,
            "hashed_leaf_name": hashed_leaf_name,
            "count": n,
        })

    # ---------- DB write (PREVIEW plan) ----------
    conn = _db_connect()
    _db_init(conn)
    run_id = _run_start(conn)
    logging.debug(f"{PkTexts.DB} DB at: {str(db_path_p)} (run_id={run_id})")

    try:
        _db_save_detection(conn, run_id, plans)
        _db_save_moves(conn, run_id, plans, planned_only=True)
    except Exception as e:
        logging.error(f"DB write failed (preview plan): {e}")
        traceback.print_exc()

    # ---------- Preview summary ----------
    logging.debug(f"{PkTexts.PREVIEW} Detected {len(plans)} leaf dir(s) > limit({file_limit}).")
    total_overflow = sum(len(p["overflow"]) for p in plans)
    logging.debug(f"{PkTexts.PLAN} Total overflow files (excluding long names): {total_overflow}")
    if not plans:
        _run_finish(conn, run_id, status="NO_ACTION")
        logging.debug(f"{PkTexts.DONE} No action required. Saved empty run to DB.")
        conn.close()
        return

    for p in plans[:5]:
        logging.debug(f"{PkTexts.PLAN} Leaf: {str(p['leaf'])}")
        logging.debug(f"{PkTexts.PLAN} → Rename leaf to: {str(p['renamed_leaf'])}")
        logging.debug(f"{PkTexts.PLAN} → Create archive: {str(p['archive_dir'])}")
        logging.debug(f"{PkTexts.PLAN} Keep {len(p['keep'])} / Move {len(p['overflow'])}")
        for f in p["overflow"][:5]:
            logging.debug(f"{PkTexts.PLAN_TO_MOVE} {str(f)} -> {str(Path(p['archive_dir']) / f.nick_name)}")

    # ---- Ask to apply (ONLY ONCE, AFTER FULL PREVIEW) ----
    logging.debug(f"{PkTexts.ASK} Apply these changes now? (y/N)")
    if input().strip().lower() != "y":
        _run_finish(conn, run_id, status="PREVIEW_ONLY")
        logging.debug(f"{PkTexts.SKIP} User declined. Preview saved to DB.")
        conn.close()
        return

    # ---------- Phase 2: Apply ----------
    # Ensure archive root exists (now it's time to touch disk)
    try:
        archive_root.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logging.error(f"Archive root create failed: {str(archive_root)}")
        traceback.print_exc()
        if not continue_on_error:
            _run_finish(conn, run_id, status="ERROR", error="archive_root_create_failed")
            conn.close()
            return

    def _apply_one_plan(p: Dict[str, object]) -> Tuple[List[Tuple[str, str, int, int, int, Optional[str]]], str, bool, str]:
        """
        Returns:
            rows: list of (src, dst_final, planned, applied, ok, error)
            leaf_str, ok_dir, err
        """
        moves_rows: List[Tuple[str, str, int, int, int, Optional[str]]] = []
        leaf: Path = p["leaf"]  # type: ignore
        renamed_leaf: Path = p["renamed_leaf"]  # type: ignore
        archive_dir: Path = p["archive_dir"]  # type: ignore
        overflow: List[Path] = p["overflow"]  # type: ignore

        try:
            # Rename leaf (safe)
            if not leaf.exists():
                logging.warning(f"Leaf missing (skip rename): {str(leaf)}")
            else:
                if leaf.resolve() != renamed_leaf.resolve():
                    logging.debug(f"{PkTexts.RENAME} :{str(leaf)} -> {str(renamed_leaf)}")
                    leaf.rename(renamed_leaf)
                else:
                    logging.info(f"Leaf already desired name: {str(leaf)}")

            # Ensure archive dir
            archive_dir.mkdir(parents=True, exist_ok=True)
            logging.debug(f"{PkTexts.CREATED} {str(archive_dir)}")

            # Move overflow (skip long names defensively again)
            for src in overflow:
                if len(str(src)) >= max_name_len:
                    logging.debug(f"{PkTexts.SKIPPED} Long path skipped: {str(src)}")
                    moves_rows.append((str(src), str(archive_dir / src.name), 1, 0, 0, "long_path_skipped"))
                    continue

                rel_name = src.name
                src_now = renamed_leaf / rel_name
                if not src_now.is_file():
                    logging.debug(f"{PkTexts.SKIP} Missing (already processed?): {str(src_now)}")
                    moves_rows.append((str(src), str(archive_dir / rel_name), 1, 0, 0, "missing"))
                    continue

                dst = archive_dir / rel_name
                dst_final = dst if not dst.exists() else _unique_path(dst)
                logging.debug(f"{PkTexts.MOVE} {str(src_now)} -> {str(dst_final)}")
                shutil.move(str(src_now), str(dst_final))
                moves_rows.append((str(src), str(dst_final), 1, 1, 1, None))
            return moves_rows, str(leaf), True, ""

        except Exception as e:
            traceback.print_exc()
            err = str(e)
            for src in overflow:
                moves_rows.append((str(src), str(archive_dir / src.name), 1, 0, 0, err))
            return moves_rows, str(leaf), False, err

    applied_dirs = 0
    moved_files = 0
    had_error = False

    if workers <= 1:
        for p in plans:
            rows, leaf_str, ok_dir, err = _apply_one_plan(p)
            try:
                _db_save_moves(conn, run_id, plans=[], planned_only=False, applied_updates=rows)
            except Exception as e:
                logging.error(f"DB update failed (serial): {e}")
            if ok_dir:
                applied_dirs += 1
                moved_files += sum(1 for _, _, _, ap, ok, _ in rows if ap and ok)
            else:
                had_error = True
                if not continue_on_error:
                    logging.debug(f"{PkTexts.ASK} Error processing leaf: {leaf_str}. Continue? (y/N)")
                    if input().strip().lower() != "y":
                        break
    else:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futures = [ex.submit(_apply_one_plan, p) for p in plans]
            for fut in as_completed(futures):
                rows, leaf_str, ok_dir, err = fut.result()
                try:
                    _db_save_moves(conn, run_id, plans=[], planned_only=False, applied_updates=rows)
                except Exception as e:
                    logging.error(f"DB update failed (parallel): {e}")
                if ok_dir:
                    applied_dirs += 1
                    moved_files += sum(1 for _, _, _, ap, ok, _ in rows if ap and ok)
                else:
                    had_error = True
                    if not continue_on_error:
                        logging.debug(f"{PkTexts.ASK} Error processing leaf: {leaf_str}. Continue? (y/N)")
                        if input().strip().lower() != "y":
                            break

    status = "APPLIED" if not had_error else "APPLIED_WITH_ERRORS"
    _run_finish(conn, run_id, status=status)
    conn.close()

    logging.debug(f"{PkTexts.RESULT} Applied to {applied_dirs} dir(s), moved {moved_files} file(s).")
    logging.debug(f"{PkTexts.DONE} Run saved to DB (run_id={run_id}).")
