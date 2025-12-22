def _normalize_window_title(s: str, *, collapse_inner_spaces: bool = False) -> str:
    import unicodedata

    if s is None:
        return ""

    # n. Unicode normalize
    s = unicodedata.normalize("NFKC", s)

    # 2) NBSP -> normal space
    s = s.replace("\u00A0", " ")

    # 3) remove zero-width chars
    for zw in ("\u200B", "\u200C", "\u200D", "\uFEFF"):
        s = s.replace(zw, "")

    # 5) trim edges
    return s


def _visualize_string(s: str) -> str:
    """
    Make invisible characters visible for logging.
    Example output:
      [ ABC ] raw_len=5 | repr=' ABC ' | chars= (0x20),A(0x41),B(0x42),C(0x43),(0x20)
    """
    parts = []
    for ch in s:
        parts.append(f"{ch}({hex(ord(ch))})")
    return f"[{s}] raw_len={len(s)} | repr={repr(s)} | chars={', '.join(parts)}"


def get_window_titles_2024(
        process_img_n: str | None = None,
        *,
        normalize: bool = True,
        collapse_inner_spaces: bool = False,
        unique: bool = True,
        include_invisible: bool = False,
        debug_visualize: bool = False,
):
    import logging
    import traceback

    import psutil
    import win32gui
    import win32process

    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    def _maybe_normalize(title: str) -> str:
        return (
            _normalize_window_title(title, collapse_inner_spaces=collapse_inner_spaces)
            if normalize else title
        )

    def _append_title(buf: list[str], title_raw: str):
        title = _maybe_normalize(title_raw)
        if not title:
            return
        if unique:
            # Deduplicate while preserving order (py3.7+ dict preserves insertion order)
            if title not in seen:
                seen.add(title)
                buf.append(title)
        else:
            buf.append(title)

        if QC_MODE and debug_visualize:
            logging.debug("[get_window_titles] collected="
                          f"{_visualize_string(title_raw)} -> normalized={_visualize_string(title)}")

    # Collect buffer and seen set for de-duplication
    titles: list[str] = []
    seen: set[str] = set()

    try:
        if process_img_n:
            # n. Find PIDs for the given image name
            pids = [p.info["pid"] for p in psutil.process_iter(["name", "pid"]) if p.info["name"] == process_img_n]
            if QC_MODE:
                logging.debug(f"[get_window_titles] Found PIDs for '{process_img_n}': {pids}")

            if not pids:
                logging.debug(f"[get_window_titles] Process '{process_img_n}' not found.")
                return titles

            def _enum_by_pid(hwnd, pid_list):
                # Filter by owner PID
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if found_pid in pid_list:
                    if include_invisible or win32gui.IsWindowVisible(hwnd):
                        name = win32gui.GetWindowText(hwnd)
                        if name:
                            _append_title(titles, name)
                return 1  # continue enumeration

            # It is fine to pass the full pid list once;
            # EnumWindows will test each hwnd's pid membership.
            win32gui.EnumWindows(_enum_by_pid, pids)

            if QC_MODE:
                logging.debug(f"[get_window_titles] Titles for process '{process_img_n}': {titles}")
            return titles

        else:
            # All windows (visible by default)
            def _enum_all(hwnd, _lparam):
                if include_invisible or win32gui.IsWindowVisible(hwnd):
                    name = win32gui.GetWindowText(hwnd)
                    if name:
                        _append_title(titles, name)
                return 1  # continue enumeration

            win32gui.EnumWindows(_enum_all, None)
            return titles

    except Exception as e:
        logging.debug(rf"[get_window_titles] traceback.format_exc()={traceback.format_exc()}")

