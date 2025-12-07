import logging
from pathlib import Path
from textwrap import dedent

from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
from pk_internal_tools.pk_objects.pk_directories import d_pk_root_hidden

# 절대 덮어쓰기 금지(대상 삭제/대체 금지)
FORBID_OVERWRITE = True


def ensure_target_pnx_names_replaced() -> None:
    """
    Batch-rename file and directory names under a chosen root.
    Supports two modes for defining rules:
    1. by_toml_rules: Uses a TOML file with prefix, suffix, and replacement rules.
    2. by_typing: Allows the user to enter old/new replacement pairs directly.

    - 모든 사용자 입력은 ensure_value_completed_2025_10_13_0000 사용
    - 탐색 범위: walking_mode = "recursive" | "shallow" (사용자 입력)
    - 안전장치:
        * 불법문자(< > : " / \ | ? *) -> '_' 치환, 연속 공백 압축
        * 경로 길이 초과(총 길이, 컴포넌트 길이) 시 자동 축약 없이 LOG & SKIP
        * 충돌 시 절대 덮어쓰기 금지: 태깅(tag) 또는 스킵(skip)만 수행
    - 작업 평가:
        * 적용 전/후 동일 범위에서 파일/디렉토리 개수 비교(정합성 PASS/MISMATCH 로그)
    """
    func_n = get_caller_name()

    # A) d_working 선택
    selected = ensure_value_completed_2025_10_13_0000(key_name="d_working", func_n=func_n, options=[])
    d_working = Path(str(selected)).expanduser().resolve()
    if not d_working.exists() or not d_working.is_dir():
        logging.error(f"Working directory is invalid: {d_working}")
        return

    # A-2) walking mode 선택 (shallow / recursive)
    walking_choice = ensure_value_completed_2025_10_13_0000(
        key_name="walking_mode", func_n=func_n, options=["shallow", "recursive"]
    )
    recursive = str(walking_choice).lower() == "recursive"
    
    # B) 동작 방식 선택 (by_toml_rules / by_typing)
    operation_mode = ensure_value_completed_2025_10_13_0000(
        key_name="operation_mode", func_n=func_n, options=["by_toml_rules", "by_typing"]
    )

    replacements, prefix_rules, suffix_rules = [], [], []

    if str(operation_mode) == "by_toml_rules":
        try:
            rules_path = Path(str(d_pk_root_hidden)) / f"rename_rules_for_{func_n}.toml"
            replacements, prefix_rules, suffix_rules = _get_rules_from_toml(func_n, rules_path)
        except Exception as e:
            logging.error(f"Failed to get rules from TOML: {e}")
            return
    elif str(operation_mode) == "by_typing":
        try:
            replacements, prefix_rules, suffix_rules = _get_rules_from_typing(func_n)
        except Exception as e:
            logging.error(f"Failed to get rules from typing: {e}")
            return
    else:
        logging.error(f"Invalid operation mode: {operation_mode}")
        return

    if not replacements and not prefix_rules and not suffix_rules:
        logging.error("No valid rules found. Aborting.")
        return

    # E) 대상 수집 & 미리보기 생성
    all_paths = _collect_paths(d_working, recursive=recursive)
    files = [p for p in all_paths if p.is_file()]
    dirs = [p for p in all_paths if p.is_dir()]
    dirs.sort(key=lambda x: len(str(x)), reverse=True)  # 디렉토리는 깊은 순서로

    # --- 작업평가: 사전 카운트 ---
    before_files_count = len(files)
    before_dirs_count = len(dirs)

    preview_lines: list[str] = []
    change_count = 0

    # 파일 미리보기
    for p in files:
        new_name_raw = _transform_name(p.name, replacements, prefix_rules, suffix_rules)
        new_name, san_warns = _sanitize_candidate_name(new_name_raw)
        if new_name != p.name:
            dst = p.with_name(new_name)
            exceed, reason = _would_exceed_path_limits(dst, max_total=260, max_component=255)
            if exceed:
                preview_lines.append(f"FILE {p} -> {dst}  SKIP ({reason})")
            else:
                meta = f"  sanitize={','.join(san_warns)}" if san_warns else ""
                preview_lines.append(f"FILE {p} -> {dst}{meta}")
            change_count += 1

    # 디렉토리 미리보기
    for p in dirs:
        new_name_raw = _transform_name(p.name, replacements, prefix_rules, suffix_rules)
        new_name, san_warns = _sanitize_candidate_name(new_name_raw)
        if new_name != p.name:
            dst = p.with_name(new_name)
            exceed, reason = _would_exceed_path_limits(dst, max_total=260, max_component=255)
            if exceed:
                preview_lines.append(f"DIR  {p} -> {dst}  SKIP ({reason})")
            else:
                meta = f"  sanitize={','.join(san_warns)}" if san_warns else ""
                preview_lines.append(f"DIR  {p} -> {dst}{meta}")
            change_count += 1

    if change_count == 0:
        logging.info("No changes detected from current rules. Nothing to do.")
        return

    logging.info(f"Total planned changes: {change_count}")
    _emit_preview(preview_lines, max_lines=120)

    # F) 최종 적용 여부
    final_choice = ensure_value_completed_2025_10_13_0000(key_name="apply_changes", func_n=func_n, options=["yes", "no"])
    if str(final_choice).lower() != "yes":
        logging.info("Aborted by user. No changes applied.")
        return

    # G) 실제 적용 (경로 길이 초과는 무조건 SKIP)
    logging.info("Applying renames...")
    applied = failed = skipped = 0

    # 파일 먼저
    for p in files:
        new_name_raw = _transform_name(p.name, replacements, prefix_rules, suffix_rules)
        if new_name_raw == p.name:
            continue
        new_name, _ = _sanitize_candidate_name(new_name_raw)
        dst = p.with_name(new_name)
        exceed, reason = _would_exceed_path_limits(dst, max_total=260, max_component=255)
        if exceed:
            logging.warning(f"Skip due to path-length limits ({reason}): {p} -> {dst}")
            skipped += 1
            continue
        ok = _rename_path_avoid_collision(
            dst_src=p, dst=dst, max_total=260, max_component=255,
            collision_policy="tag"  # 절대 overwrite 금지: tag 또는 skip만 허용
        )
        if ok is True:
            applied += 1
        elif ok is False:
            failed += 1
        else:
            skipped += 1

    # 디렉토리(깊은 순서)
    for p in dirs:
        new_name_raw = _transform_name(p.name, replacements, prefix_rules, suffix_rules)
        if new_name_raw == p.name:
            continue
        new_name, _ = _sanitize_candidate_name(new_name_raw)
        dst = p.with_name(new_name)
        exceed, reason = _would_exceed_path_limits(dst, max_total=260, max_component=255)
        if exceed:
            logging.warning(f"Skip due to path-length limits ({reason}): {p} -> {dst}")
            skipped += 1
            continue
        ok = _rename_path_avoid_collision(
            dst_src=p, dst=dst, max_total=260, max_component=255,
            collision_policy="tag"  # 절대 overwrite 금지: tag 또는 skip만 허용
        )
        if ok is True:
            applied += 1
        elif ok is False:
            failed += 1
        else:
            skipped += 1

    logging.info(f"Done. Applied={applied}, Failed={failed}, Skipped={skipped}")

    # H) 작업 평가(사후 카운트 수집 & 비교)
    _evaluate_and_report_counts(
        d_working=d_working,
        recursive=recursive,
        before_files_count=before_files_count,
        before_dirs_count=before_dirs_count,
    )


# -----------------------------
# Helpers
# -----------------------------

def _get_rules_from_toml(func_n: str, rules_path: Path) -> tuple[list, list, list]:
    """Handles the logic for getting rules from a TOML file."""
    ensure_pnx_made(pnx=str(rules_path), mode="f")
    try:
        if rules_path.stat().st_size == 0:
            rules_path.write_text(_toml_template(), encoding="utf-8")
    except Exception as e:
        raise Exception(f"Failed to initialize rules file: {e}")

    open_choice = ensure_value_completed_2025_10_13_0000(
        key_name="open_rules_file", func_n=func_n, options=["open", "skip"]
    )
    if str(open_choice).lower() == "open":
        try:
            ensure_pnx_opened_by_ext(pnx=str(rules_path))
        except Exception as e:
            logging.warning(f"Failed to open rules file automatically: {e}. Please open manually: {rules_path}")

    proceed_choice = ensure_value_completed_2025_10_13_0000(
        key_name="proceed_after_edit", func_n=func_n, options=["continue", "cancel"]
    )
    if str(proceed_choice).lower() != "continue":
        raise Exception("Canceled by user.")

    try:
        return _load_rules_toml(rules_path)
    except Exception as e:
        logging.error(f"Failed to load TOML rules: {e}")
        try:
            tips = _lint_rules_toml(rules_path)
            if tips:
                logging.error("[RULES LINT] Possible issues detected:")
                for tip in tips:
                    logging.error(f" - {tip}")
        except Exception:
            pass
        raise

def _get_rules_from_typing(func_n: str) -> tuple[list, list, list]:
    """Handles the logic for getting rules from user typing."""
    replacements: list[tuple[str, str]] = []
    while True:
        old_val = ensure_value_completed_2025_10_13_0000(
            key_name="old_value_typing",
            func_n=func_n,
            guide_text="Enter the 'old' value to replace (or press Enter to finish):"
        )
        if not old_val:
            break
        
        new_val = ensure_value_completed_2025_10_13_0000(
            key_name="new_value_typing",
            func_n=func_n,
            guide_text=f"Enter the 'new' value for '{old_val}':"
        )
        replacements.append((str(old_val), str(new_val)))
        logging.info(f"Rule added: '{old_val}' -> '{new_val}'")

    logging.info(f"Finished adding rules. Total rules: {len(replacements)}")
    return replacements, [], []


def _toml_template() -> str:
    """Return initial TOML template for the rules file."""
    return dedent("""\
        # -----------------------------------------
        # Rename Rules (TOML)
        # Boundary replacements (prefix/suffix) and in-name replacements.
        # - Prefix applies when name startswith(old)
        # - Suffix applies when name endswith(old)
        # - In-name replacements apply anywhere in the base name
        # -----------------------------------------

        [[prefix_rules]]
        old = "#"
        new = "temp_"

        [[suffix_rules]]
        old = "_old"
        new = "_new"

        [[replacements]]
        old = "temp"
        new = "TMP"

        # [[replacements]]
        # old = "버전1"
        # new = "v1"
    """).strip() + "\n"


def _load_rules_toml(path: Path) -> tuple[list[tuple[str, str]], list[tuple[str, str]], list[tuple[str, str]]]:
    """
    Load TOML rules and return (replacements, prefix_rules, suffix_rules).
    - 파일을 'utf-8-sig'로 그대로 읽고, 교정 없이 파싱만 시도
    - 실패 시 예외 발생 및 상위에서 린트 결과만 출력(수정은 안 함)
    """
    text = path.read_text(encoding="utf-8-sig", errors="strict")

    # 우선 tomllib 시도 (3.11+)
    try:
        import tomllib  # type: ignore
        data = tomllib.loads(text)
    except Exception:
        # 폴백: toml 패키지
        try:
            import toml  # type: ignore
            data = toml.loads(text)
        except Exception as e2:
            raise RuntimeError(str(e2))

    def _pairs(section: str) -> list[tuple[str, str]]:
        items = data.get(section, [])
        out: list[tuple[str, str]] = []
        if isinstance(items, list):
            for obj in items:
                if isinstance(obj, dict):
                    old = str(obj.get("old", "")).strip()
                    new = str(obj.get("new", "")).strip()
                    if old:
                        out.append((old, new))
        return out

    return _pairs("replacements"), _pairs("prefix_rules"), _pairs("suffix_rules")


def _lint_rules_toml(path: Path) -> list[str]:
    """
    규칙 파일을 수정하지 않고, TOML 작성 상 **흔한 실수**만 지적하는 간단 린트.
    - '[[group]]' 라인 끝에 불필요한 내용 존재(공백/주석 제외)
    - 세미콜론(;)을 주석처럼 사용
    - 따옴표 짝이 안 맞는 듯 보이는 라인(간단 휴리스틱)
    """
    text = path.read_text(encoding="utf-8-sig", errors="ignore")
    tips: list[str] = []

    def outside_quotes_has(line: str, ch: str) -> bool:
        in_single = in_double = False
        esc = False
        for c in line:
            if esc:
                esc = False
                continue
            if c == "\\":
                esc = True
                continue
            if c == "'" and not in_double:
                in_single = not in_single
                continue
            if c == '"' and not in_single:
                in_double = not in_double
                continue
            if c == ch and not in_single and not in_double:
                return True
        return False

    for i, raw in enumerate(text.splitlines(), start=1):
        line = raw.rstrip("\n")

        # n. 그룹 헤더 뒤 불필요한 토큰
        if "[[" in line and "]]" in line:
            after = line.split("]]", 1)[1].strip()
            # TOML에서는 그룹 헤더 뒤에 공백/주석(# ...)만 허용
            if after and not after.startswith("#"):
                tips.append(f"L{i}: group header must be alone; move trailing text to a new line or use '#'. -> {line.strip()}")

        # 2) 세미콜론을 주석처럼 사용
        if outside_quotes_has(line, ";"):
            tips.append(f"L{i}: ';' is not a comment in TOML. Replace with '#'. -> {line.strip()}")

        # 3) 따옴표 짝 간단 체크 (홀수 개이면 의심)
        if line.count('"') % 2 == 1 or line.count("'") % 2 == 1:
            tips.append(f"L{i}: unmatched quotes suspected. -> {line.strip()}")

    return tips


def _collect_paths(root: Path, recursive: bool = True) -> list[Path]:
    """Collect non-hidden paths under root. Hidden = any dot-prefixed part."""
    if recursive:
        iterator = root.rglob("*")
    else:
        iterator = root.iterdir()

    paths: list[Path] = []
    for p in iterator:
        if any(part.startswith(".") for part in p.parts):
            continue
        paths.append(p)
    return paths


def _transform_name(name: str,
                    replacements: list[tuple[str, str]],
                    prefix_rules: list[tuple[str, str]],
                    suffix_rules: list[tuple[str, str]]) -> str:
    """
    Apply boundary replacements first (prefix then suffix), then in-name replacements.
    - Prefix: if name startswith(old), replace that leading segment with new.
    - Suffix: if name endswith(old), replace that trailing segment with new.
    - In-name: simple str.replace for each (old, new) in the given order.
    """
    new_name = name

    # Prefix boundary
    for old, new in prefix_rules:
        if old and new_name.startswith(old):
            new_name = new + new_name[len(old):]

    # Suffix boundary
    for old, new in suffix_rules:
        if old and new_name.endswith(old):
            new_name = new_name[:len(new_name) - len(old)] + new

    # In-name replacements (작성 순서대로)
    for old, new in replacements:
        if old:
            new_name = new_name.replace(old, new)

    return new_name


def _sanitize_candidate_name(name: str) -> tuple[str, list[str]]:
    """
    Sanitize a base name:
      - Replace Windows-illegal chars: <>:\"/\\|?*  -> "_"
      - Collapse multiple spaces to single, trim
    NOTE: 길이 때문에 임의로 줄이지 않음(요청 정책 준수).
    Returns: (sanitized_name, warnings)
    """
    import re

    warnings: list[str] = []
    original = name  # (현재 미사용, 추후 비교용)

    # Illegal chars -> "_"
    if any(ch in '<>:"/\\|?*' for ch in name):
        name = re.sub(r'[<>:"/\\|?\*]+', "_", name)
        warnings.append("illegal-chars-replaced")

    # Collapse spaces and trim
    squeezed = re.sub(r"\s+", " ", name).strip()
    if squeezed != name:
        name = squeezed
        warnings.append("spaces-collapsed")

    return name, warnings


def _would_exceed_path_limits(dst_path: Path, max_total: int = 260, max_component: int = 255) -> tuple[bool, str]:
    """Conservative Windows-style limits; return (exceeds, reason)."""
    s = str(dst_path)
    if any(len(part) > max_component for part in dst_path.parts):
        return True, "component-too-long"
    if len(s) > max_total:
        return True, "total-path-too-long"
    return False, ""


def _emit_preview(lines: list[str], max_lines: int = 120) -> None:
    total = len(lines)
    if total <= max_lines:
        for line in lines:
            logging.info(line)
        return
    head = lines[: max_lines // 2]
    tail = lines[-max_lines // 2:]
    for line in head:
        logging.info(line)
    logging.info(f"... omitted {total - len(head) - len(tail)} lines ...")
    for line in tail:
        logging.info(line)


def _rename_path_avoid_collision(*, dst_src: Path, dst: Path,
                                 max_total: int = 260, max_component: int = 255,
                                 collision_policy: str = "tag") -> bool | None:
    """
    Rename src -> dst.

    절대 덮어쓰기 금지(FORBID_OVERWRITE=True):
      - 대상 경로가 존재하면 'tag'(기본)로 고유화하거나 'skip'으로 건너뜀.
      - 대상 파일/폴더 삭제/대체(덮어쓰기) 일체 금지.
      - move 실행 직전에도 최종 목적지가 존재하면 즉시 SKIP.

    collision_policy:
      - "tag"  : 충돌 시 _DUPLICATED_WORK, _DUPLICATED_WORK_2 ...로 고유화
      - "skip" : 충돌 시 SKIP
      - "overwrite"는 무시되며 "tag"로 강제 전환됨.
    반환:
      True  = 적용 완료
      False = 실패(예: 권한/락)
      None  = 스킵(길이 초과, 동일 경로, 정책에 따른 SKIP 등)
    """
    from shutil import move

    src = dst_src
    if str(src) == str(dst):
        return None

    # 길이 한계 선검사
    exceed, reason = _would_exceed_path_limits(dst, max_total=max_total, max_component=max_component)
    if exceed:
        logging.warning(f"Skip due to path-length limits ({reason}): {src} -> {dst}")
        return None

    # 정책 강제: 절대 overwrite 금지
    policy = (collision_policy or "tag").lower()
    if FORBID_OVERWRITE and policy == "overwrite":
        logging.warning("overwrite policy requested but forbidden; falling back to 'tag'.")
        policy = "tag"

    # 충돌 처리
    if dst.exists():
        if policy == "skip":
            logging.info(f"SKIP on conflict: {src} -> {dst}")
            return None
        # policy == "tag": 꼬리표로 고유화
        candidate = dst
        n = 0
        while candidate.exists():
            n += 1
            tag = "_DUPLICATED_WORK" if n == 1 else f"_DUPLICATED_WORK_{n}"
            candidate = _name_with_tag(dst, tag, parent=dst.parent)
            exceed, reason = _would_exceed_path_limits(candidate, max_total=max_total, max_component=max_component)
            if exceed:
                logging.warning(f"Skip due to path-length limits after collision tag ({reason}): {src} -> {candidate}")
                return None
        dst = candidate  # 태깅된 최종 목적지로 업데이트

    # 마지막 안전 확인: 절대 덮어쓰기 방지
    if FORBID_OVERWRITE and dst.exists():
        logging.error(f"Destination unexpectedly exists just before move; refusing to overwrite: {dst}")
        return None

    try:
        move(str(src), str(dst))
        logging.info(f"RENAMED {src} -> {dst}")
        return True
    except Exception as e:
        logging.error(f"Rename failed: {src} -> {dst} ({e})")
        return False


def _name_with_tag(dst: Path, tag: str, *, parent: Path) -> Path:
    """Insert tag before extension if any, else append to the end."""
    name = dst.name
    if "." in name:
        stem, ext = name.rsplit(".", 1)
        new_name = f"{stem}{tag}.{ext}"
    else:
        new_name = f"{name}{tag}"
    return parent / new_name


def _evaluate_and_report_counts(
        *, d_working: Path, recursive: bool, before_files_count: int, before_dirs_count: int
) -> None:
    """
    사후 정합성 검사:
      - 같은 탐색 범위(recursive/shallow)로 다시 스캔하여
        파일/디렉토리 개수 비교 및 PASS/MISMATCH 로그.
    """
    after_paths = _collect_paths(d_working, recursive=recursive)
    after_files_count = sum(1 for p in after_paths if p.is_file())
    after_dirs_count = sum(1 for p in after_paths if p.is_dir())

    files_ok = (before_files_count == after_files_count)
    dirs_ok = (before_dirs_count == after_dirs_count)

    logging.info(
        f"[EVAL] Files count: before={before_files_count}, after={after_files_count} -> "
        f"{'PASS' if files_ok else 'MISMATCH'} (Δ={after_files_count - before_files_count})"
    )
    logging.info(
        f"[EVAL] Dirs  count: before={before_dirs_count}, after={after_dirs_count} -> "
        f"{'PASS' if dirs_ok else 'MISMATCH'} (Δ={after_dirs_count - before_dirs_count})"
    )
    if not files_ok or not dirs_ok:
        logging.warning("[EVAL] Count mismatch detected. Review skipped/failed items and rules.")

    if files_ok and dirs_ok:
        ensure_pnx_opened_by_ext(d_working)
