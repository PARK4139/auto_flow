# file: flet_alert_gui.py
# Minimal Flet-based alert dialog that emits a single JSON line to stdout.
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import flet as ft


def _parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Flet alert dialog (JSON in, JSON out)")
    ap.add_argument("--request-file", required=True, help="Path to JSON request file")
    return ap.parse_args()


def _load_request(path: str | Path) -> Dict[str, Any]:
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def _emit_result(button_clicked: Optional[str], input_value: Optional[str]) -> None:
    """Emit exactly one JSON object to stdout and flush."""
    out = {"button_clicked": button_clicked, "input_value": input_value}
    print(json.dumps(out, ensure_ascii=False))
    sys.stdout.flush()


def _run_app(req: Dict[str, Any]) -> None:
    # Required/basic fields
    title: str = (req.get("title") or "알림")
    ment: str = (req.get("ment") or "")
    input_default: str = (req.get("input_text_default") or "")
    btn_list: List[str] = list(req.get("btn_list") or ["확인"])
    auto_click: int = int(req.get("auto_click_positive_btn_after_seconds") or 0)

    # Optional UX fields
    default_idx: int = int(req.get("default_button_index", 0))
    cancel_idx: int = int(req.get("cancel_button_index", -1))  # -1 disables ESC
    always_on_top: bool = bool(req.get("always_on_top", False))
    win_w: int = int(req.get("window_width", 480))
    win_h: int = int(req.get("window_height", 260))

    # Normalize indices
    if not (0 <= default_idx < len(btn_list)):
        default_idx = 0 if btn_list else -1
    if not (0 <= cancel_idx < len(btn_list)):
        cancel_idx = -1

    def app(page: ft.Page):
        page.title = title
        page.window_width = win_w
        page.window_height = win_h
        page.window_center()
        page.padding = 20
        if always_on_top:
            page.window_always_on_top = True

        # Ensure native desktop window (not web view)
        page.window_prevent_close = False

        # State holders
        emitted = {"done": False}
        clicked: Dict[str, Optional[str]] = {"text": None}

        # Optional input
        input_field: Optional[ft.TextField] = None
        if input_default != "":
            input_field = ft.TextField(value=input_default, autofocus=True, expand=True)

        def emit_once_and_close(text_for_button: Optional[str]) -> None:
            """Emit JSON exactly once, then close window."""
            if not emitted["done"]:
                emitted["done"] = True
                txt = input_field.value if input_field else None
                _emit_result(text_for_button, txt)
            # Give stdout a moment to flush on some environments (defensive)
            page.update()
            try:
                page.window_destroy()
            except Exception:
                # As a last resort, terminate the process hard after a tiny delay.
                os._exit(0)

        # Buttons
        def make_btn(label: str, idx: int) -> ft.ElevatedButton:
            return ft.ElevatedButton(text=label, on_click=lambda e, t=label: emit_once_and_close(t))

        buttons = [make_btn(b, i) for i, b in enumerate(btn_list)]

        # Layout
        items: List[ft.Control] = [ft.Text(ment, selectable=True)]
        if input_field:
            items += [ft.Container(height=8), input_field]
        items += [ft.Container(height=16), ft.Row(buttons, alignment=ft.MainAxisAlignment.END, wrap=True)]
        page.add(ft.Column(items, expand=True))

        # Auto-click (timeout -> default button)
        if auto_click > 0 and btn_list and 0 <= default_idx < len(btn_list):
            async def auto_close():
                await asyncio.sleep(auto_click)
                if not emitted["done"]:
                    emit_once_and_close(btn_list[default_idx])
            page.run_task(auto_close())

        # Keyboard shortcuts: Enter -> default, Esc -> cancel
        def on_key(e: ft.KeyboardEvent):
            if emitted["done"]:
                return
            if e.key in ("Enter", "NumpadEnter"):
                if 0 <= default_idx < len(btn_list):
                    emit_once_and_close(btn_list[default_idx])
            elif e.key == "Escape":
                if 0 <= cancel_idx < len(btn_list):
                    emit_once_and_close(btn_list[cancel_idx])

        page.on_keyboard_event = on_key

        # Window closed by OS or user (X). If not emitted yet, emit with None.
        def on_window_event(e: ft.ControlEvent):
            if e.data == "close" and not emitted["done"]:
                emit_once_and_close(None)

        page.on_window_event = on_window_event

    # Force a native desktop window (avoids browser fallback)
    ft.app(target=app, view=ft.AppView.FLET_APP)


def main() -> None:
    args = _parse_args()
    req = _load_request(args.request_file)
    _run_app(req)


if __name__ == "__main__":
    main()
