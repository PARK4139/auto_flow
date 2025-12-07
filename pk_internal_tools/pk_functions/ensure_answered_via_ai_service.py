from __future__ import annotations

from typing import Any, Dict, Optional, Tuple, Sequence
import logging
import time
import hashlib
import subprocess
import sys

from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
from pk_internal_tools.pk_functions.ensure_pressed import ensure_pressed
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_typed import ensure_typed
from pk_internal_tools.pk_objects.pk_urls import URL_CHATGPT_PK_WORKING


# ============================
# Clipboard helpers
# ============================
def _clipboard_copy(text: str) -> None:
    """Copy text to OS clipboard."""
    try:
        import pyperclip  # type: ignore
        pyperclip.copy(text)
        return
    except Exception:
        pass
    try:
        import tkinter as tk  # type: ignore
        r = tk.Tk(); r.withdraw()
        r.clipboard_clear(); r.clipboard_append(text); r.update(); r.destroy()
        return
    except Exception as e:
        logging.debug(f"clipboard copy failed: {e}")


def _clipboard_paste_py() -> str:
    """Try Python-level clipboards (pyperclip / tkinter)."""
    try:
        import pyperclip  # type: ignore
        return pyperclip.paste()
    except Exception:
        pass
    try:
        import tkinter as tk  # type: ignore
        r = tk.Tk(); r.withdraw()
        data = r.clipboard_get(); r.destroy()
        return data
    except Exception as e:
        logging.debug(f"clipboard paste(py) failed: {e}")
        return ""


def _clipboard_paste_os() -> str:
    """OS-level fallback: Windows PowerShell Get-Clipboard (Raw)."""
    try:
        if sys.platform.startswith("win"):
            proc = subprocess.run(
                ["powershell", "-NoProfile", "-Command", "Get-Clipboard -Raw"],
                capture_output=True, text=True, timeout=3
            )
            if proc.returncode == 0:
                return proc.stdout
    except Exception as e:
        logging.debug(f"clipboard paste(os) failed: {e}")
    return ""


def _clipboard_paste() -> str:
    data = _clipboard_paste_py()
    if data:
        return data
    return _clipboard_paste_os()


# ============================
# Window detection & focusing
# ============================
def is_opened_chatgpt_tab_at_browser() -> bool:
    """Heuristic: detect a window whose title contains ChatGPT/domain keywords."""
    try:
        import pygetwindow as gw  # type: ignore
    except Exception:
        logging.debug("pygetwindow not installed; assume opened=True.")
        return True

    keywords = ("ChatGPT", "chat.openai.com", "chatgpt.com", "OpenAI")
    try:
        for w in gw.getAllWindows():
            title = (w.title or "").strip()
            if any(k.lower() in title.lower() for k in keywords):
                return True
    except Exception as e:
        logging.debug(f"window detection failed: {e}")
    return False


def _bring_to_front_win32(hwnd: int) -> bool:
    try:
        import win32gui  # type: ignore
        import win32con  # type: ignore
        if hwnd:
            try:
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            except Exception:
                pass
            try:
                win32gui.SetForegroundWindow(hwnd)
                return True
            except Exception:
                return False
    except Exception:
        return False
    return False


def ensure_window_front_to_ChatGPT_tab() -> bool:
    try:
        import pygetwindow as gw  # type: ignore
    except Exception:
        logging.debug("pygetwindow not installed; cannot force front.")
        return False

    targets = []
    keywords = ("ChatGPT", "chat.openai.com", "chatgpt.com", "OpenAI")
    try:
        for w in gw.getAllWindows():
            title = (w.title or "")
            if any(k.lower() in title.lower() for k in keywords):
                targets.append(w)
        if not targets:
            return False

        for w in reversed(targets):
            try:
                hwnd = getattr(w, "_hWnd", None) or getattr(w, "hwnd", None) or getattr(w, "handle", None)
            except Exception:
                hwnd = None
            try:
                if w.isMinimized:
                    w.restore()
                w.activate()
                ensure_slept(milliseconds=180)
                return True
            except Exception as e:
                logging.debug(f"activate failed: {e}")
                if hwnd and _bring_to_front_win32(int(hwnd)):
                    ensure_slept(milliseconds=180)
                    return True
        return False
    except Exception as e:
        logging.debug(f"bring-to-front failed: {e}")
        return False


def ensure_focus_to_ChatGPT_tab_click_fallback() -> None:
    try:
        import pyautogui  # type: ignore
    except Exception:
        logging.debug("pyautogui not installed; relying on default focus.")
        return
    try:
        screen_w, screen_h = pyautogui.size()
        x = int(screen_w * 0.5); y = int(screen_h * 0.90)
        pyautogui.moveTo(x, y, duration=0.12); pyautogui.click()
        ensure_slept(milliseconds=120)
    except Exception as e:
        logging.debug(f"click fallback failed: {e}")


# ============================
# Multi-strategy copy (NO Ctrl+A)
# ============================
# 더 많은 DOM 변형에 대응: 최신/구버전/대체 구조 모두 시도
_JS_COPY_ASSISTANT = r"""
(function(){
  try {
    const pickTexts = (nodes) =>
      nodes.map(n => (n.innerText || n.textContent || '').trim()).filter(Boolean);
    const q = (sel) => Array.from(document.querySelectorAll(sel));

    // selectors (ordered by confidence)
    const S = [
      '[data-message-author-role="assistant"]',
      'main [data-message-id][data-testid="conversation-turn"] [data-message-author-role="assistant"]',
      'div[data-message-author-role="assistant"] .markdown',
      'article'
    ];

    let texts = [];
    for (const sel of S) {
      const nodes = q(sel);
      if (nodes.length) {
        texts = pickTexts(nodes);
        if (texts.length) break;
      }
    }

    const out = (texts.length ? texts.join('\\n\\n') : (document.body && document.body.innerText) || '');
    if (typeof copy === 'function') {
      copy(out);
      return 'OK:' + out.length;
    } else {
      return 'NO_COPY_FUNC';
    }
  } catch (e) {
    return 'ERR:' + (e && e.message ? e.message : e);
  }
})();
"""

def _devtools_open_console_chromium() -> None:
    # Chromium console: Ctrl+Shift+J
    ensure_pressed("ctrl", "shift", "j")
    ensure_slept(milliseconds=600)   # 포커스 안정화 대기
    # 포커스 꼬임 방지: Esc로 기존 입력 상태 클리어
    ensure_pressed("esc")
    ensure_slept(milliseconds=120)

def _devtools_close_console_chromium() -> None:
    ensure_pressed("ctrl", "shift", "j")
    ensure_slept(milliseconds=160)

def _devtools_open_console_firefox() -> None:
    # Firefox console: Ctrl+Shift+K
    ensure_pressed("ctrl", "shift", "k")
    ensure_slept(milliseconds=600)
    ensure_pressed("esc")
    ensure_slept(milliseconds=120)

def _devtools_close_console_firefox() -> None:
    ensure_pressed("ctrl", "shift", "k")
    ensure_slept(milliseconds=160)


def _copy_via_devtools_console_try(open_devtools, close_devtools) -> bool:
    """
    DevTools 열기 → JS 실행 → (닫기 전) 클립보드 즉시 확인(200/400/800ms) → 성공 시 닫고 True
    실패면 닫고 False. 이 함수는 한 번의 DevTools 오픈만 담당.
    """
    try:
        open_devtools()
        ensure_typed(_JS_COPY_ASSISTANT)
        ensure_slept(milliseconds=77)
        ensure_pressed("enter")

        # 닫기 전에 OS 클립보드 전파 대기하며 확인
        for delay_ms in (200, 400, 800):
            ensure_slept(milliseconds=delay_ms)
            data = _clipboard_paste().strip()
            if data:
                close_devtools()
                return True
        # 마지막으로 한 번 더 시도
        ensure_slept(milliseconds=300)
        if _clipboard_paste().strip():
            close_devtools()
            return True

        # 실패: 닫고 False
        close_devtools()
        return False
    except Exception as e:
        logging.debug(f"devtools copy try failed: {e}")
        try:
            close_devtools()
        except Exception:
            pass
        return False


def _copy_via_devtools_console() -> bool:
    """
    Chromium 먼저, 실패 시 Firefox 경로도 한 번만 시도.
    한 attempt 안에서 DevTools는 최대 1회만 열고 닫는다.
    """
    # Chromium path
    if _copy_via_devtools_console_try(_devtools_open_console_chromium, _devtools_close_console_chromium):
        return True
    # Firefox path
    if _copy_via_devtools_console_try(_devtools_open_console_firefox, _devtools_close_console_firefox):
        return True
    return False


def _copy_via_mouse_drag() -> bool:
    try:
        import pyautogui  # type: ignore
    except Exception:
        logging.debug("pyautogui not installed; mouse drag unavailable.")
        return False
    try:
        w, h = pyautogui.size()
        x1, y1 = int(w*0.12), int(h*0.18)
        x2, y2 = int(w*0.88), int(h*0.88)
        pyautogui.moveTo(x1, y1, duration=0.10); ensure_slept(milliseconds=40)
        pyautogui.dragTo(x2, y2, duration=0.35, button='left'); ensure_slept(milliseconds=60)
        ensure_pressed("ctrl", "c"); ensure_slept(milliseconds=160)
        return True
    except Exception as e:
        logging.debug(f"mouse drag failed: {e}")
        return False


def _copy_via_ctrl_a() -> bool:
    try:
        ensure_pressed("ctrl", "a"); ensure_slept(milliseconds=77)
        ensure_pressed("ctrl", "c"); ensure_slept(milliseconds=160)
        return True
    except Exception as e:
        logging.debug(f"ctrl+a copy failed: {e}")
        return False


def _try_copy_by_strategies(order: Sequence[str]) -> bool:
    """
    한 attempt에서 각 전략은 최대 1회만 시도한다.
    DevTools가 실패하면 즉시 다음 전략(mouse_drag → ctrl_a)으로 넘어간다.
    """
    for how in order:
        if how == "devtools":
            if _copy_via_devtools_console():
                return True
        elif how == "mouse_drag":
            if _copy_via_mouse_drag():
                return True
        elif how == "ctrl_a":
            if _copy_via_ctrl_a():
                return True
    return False


def _stable_clipboard_read(copy_order: Sequence[str], max_attempts: int = 3, backoff_ms: int = 140) -> Tuple[str, str, int]:
    """
    시나리오:
      - 주어진 전략들을 순서대로 1회씩 시도
      - 성공 시 즉시 읽기 → 동일성 확인 위해 한 번 더 복사+읽기 (DevTools는 내부에서 이미 읽기 확인)
    Returns: (text, sha1, copy_attempts)
    """
    attempts = 0
    for attempt in range(1, max_attempts + 1):
        attempts = attempt

        if not _try_copy_by_strategies(copy_order):
            ensure_slept(milliseconds=backoff_ms * attempt)
            continue

        t1 = _clipboard_paste().strip(); ensure_slept(milliseconds=60)

        # 같은 전략으로 한 번 더 복사 수행 (짧게)
        _try_copy_by_strategies(copy_order); ensure_slept(milliseconds=60)
        t2 = _clipboard_paste().strip()

        if t1 and (t1 == t2):
            h = hashlib.sha1(t1.encode("utf-8","ignore")).hexdigest()
            return t1, h, attempts

        ensure_slept(milliseconds=backoff_ms * attempt)

    # 최종 단발성 시도
    _try_copy_by_strategies(copy_order); ensure_slept(milliseconds=120)
    t = _clipboard_paste().strip()
    h = hashlib.sha1(t.encode("utf-8","ignore")).hexdigest() if t else ""
    return t, h, attempts


def ensure_gpt_answer_done(
    copy_order: Sequence[str],
    initial_timeout_s: float = 30.0,
    total_timeout_s: float = 90.0,
    stable_checks: int = 3,
    interval_ms: int = 500
) -> Dict[str, Any]:
    start = time.time()
    first_visible_at: Optional[float] = None
    stable_count = 0
    last_len = -1
    last_hash = ""
    copy_attempts_total = 0

    ensure_slept(milliseconds=450)

    while True:
        now = time.time()
        elapsed = now - start

        text, cur_hash, copy_attempts = _stable_clipboard_read(copy_order)
        copy_attempts_total += copy_attempts
        cur_len = len(text)

        if first_visible_at is None and cur_len > 0:
            first_visible_at = now

        if cur_len > 0 and cur_len == last_len and cur_hash and (cur_hash == last_hash):
            stable_count += 1
        else:
            stable_count = 0
            last_len = cur_len
            last_hash = cur_hash

        if stable_count >= stable_checks:
            return {
                "stabilized": True,
                "first_visible_latency_ms": int(((first_visible_at or now) - start) * 1000),
                "total_wait_ms": int((now - start) * 1000),
                "final_length": cur_len,
                "hash": cur_hash,
                "checks": stable_count,
                "copy_attempts": copy_attempts_total,
            }

        if first_visible_at is None and elapsed >= initial_timeout_s:
            break
        if elapsed >= total_timeout_s:
            break

        ensure_slept(milliseconds=interval_ms)

    return {
        "stabilized": False,
        "first_visible_latency_ms": int(((first_visible_at or start) - start) * 1000),
        "total_wait_ms": int((time.time() - start) * 1000),
        "final_length": last_len if last_len >= 0 else 0,
        "hash": last_hash,
        "checks": stable_count,
        "copy_attempts": copy_attempts_total,
    }


def get_answer_from_chatgpt_tab(copy_order: Sequence[str]) -> Tuple[str, str, int]:
    text, h, attempts = _stable_clipboard_read(copy_order)
    return text, h, attempts


# ============================
# Main
# ============================
@ensure_seconds_measured
def ensure_answered_via_ai_service(prompt: str) -> Dict[str, Any]:
    """
    ChatGPT 웹 UI를 통해 답변 텍스트를 가져온다.
    - DevTools(JS copy) → mouse_drag → ctrl_a 순서로 복사 시도
    - DevTools는 닫기 전 클립보드 읽기 확인 (지연 전파 흡수)
    """
    import webbrowser

    if not prompt:
        logging.debug("empty prompt; nothing to send.")
        return {"text": "", "usage": {}, "raw": None, "stabilized": False, "meta": {"reason": "empty_prompt"}}

    copy_order = ("devtools", "mouse_drag", "ctrl_a")

    NEW_CHAT_URL = URL_CHATGPT_PK_WORKING
    opened_invoke_ok = False
    for _ in range(3):
        try:
            webbrowser.open_new_tab(NEW_CHAT_URL)
            logging.debug(f"browser opened: {NEW_CHAT_URL}")
            opened_invoke_ok = True
            break
        except Exception as e:
            logging.debug(f"browser open failed: {e}")
            ensure_slept(milliseconds=200)

    opened = is_opened_chatgpt_tab_at_browser()
    if not opened:
        for _ in range(300):
            if is_opened_chatgpt_tab_at_browser():
                opened = True; break
            ensure_slept(milliseconds=111)
    if opened:
        logging.debug("chatgpt tab detected")
    else:
        logging.debug("chatgpt tab not detected; proceed anyway")

    if ensure_window_front_to_ChatGPT_tab():
        logging.debug("window brought to front")
    else:
        logging.debug("could not force front; relying on OS focus")
    ensure_focus_to_ChatGPT_tab_click_fallback()

    # Try to clear input
    try:
        ensure_pressed("ctrl", "a"); ensure_slept(milliseconds=60)
        ensure_pressed("backspace"); ensure_slept(milliseconds=77)
    except Exception:
        pass

    ensure_typed(prompt); ensure_slept(milliseconds=160)
    ensure_pressed("enter"); ensure_slept(milliseconds=180)

    # 안정화 대기: 복사 시도 루프가 내부적으로 클립보드 상태를 확인
    done_meta = ensure_gpt_answer_done(
        copy_order=copy_order,
        initial_timeout_s=35.0,
        total_timeout_s=95.0,
        stable_checks=3,
        interval_ms=650,
    )

    gpt_answer, h, copy_attempts = get_answer_from_chatgpt_tab(copy_order)
    logging.debug(f"result length={len(gpt_answer)} stabilized={done_meta.get('stabilized')}")

    return {
        "text": gpt_answer,
        "usage": {},
        "raw": None,
        "stabilized": bool(done_meta.get("stabilized")),
        "meta": {
            "first_visible_latency_ms": done_meta.get("first_visible_latency_ms"),
            "total_wait_ms": done_meta.get("total_wait_ms"),
            "final_length": done_meta.get("final_length"),
            "hash": h,
            "opened_invoke_ok": opened_invoke_ok,
            "copy_attempts": copy_attempts,
            "copy_order": list(copy_order),
        },
    }
