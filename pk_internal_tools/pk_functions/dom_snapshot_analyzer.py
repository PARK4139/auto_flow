import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup


DEFAULT_BUTTON_KEYWORD_SETS = [
    ["나만의 스마트 홈 만들기", "Create my smart home"],
    ["계정 만들기", "Create account", "완료"]
]


@dataclass
class DomSnapshot:
    snapshot_path: Path
    soup: BeautifulSoup
    buttons: List[str]
    inputs: List[str]


def capture_dom_snapshot(html: str, *, label: str, prefix: str = "dom") -> DomSnapshot:
    """
    Save the given HTML to pk_logs/selenium/ and return parsed info for reuse.
    """
    from pk_internal_tools.pk_objects.pk_directories import d_pk_logs
    log_dir = d_pk_logs / "selenium"
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    normalized_label = label.replace(" ", "_")
    file_path = log_dir / f"{prefix}_{normalized_label}_{timestamp}.html"
    file_path.write_text(html, encoding="utf-8")

    soup = BeautifulSoup(html, "html.parser")
    buttons = [
        " ".join(button.get_text(strip=True).split())
        for button in soup.find_all("button")
        if button.get_text(strip=True)
    ]
    inputs = [
        f"name={inp.get('name')} id={inp.get('id')} type={inp.get('type')} placeholder={inp.get('placeholder')}"
        for inp in soup.find_all("input")
    ]

    logging.debug(
        "[dom-snapshot][%s] saved=%s buttons=%s inputs=%s",
        label,
        file_path,
        buttons,
        inputs,
    )

    return DomSnapshot(
        snapshot_path=file_path,
        soup=soup,
        buttons=buttons,
        inputs=inputs,
    )


def analyze_buttons_for_keywords(buttons: List[str], keyword_sets=None) -> List[str]:
    if keyword_sets is None:
        keyword_sets = DEFAULT_BUTTON_KEYWORD_SETS

    matches = []
    for keywords in keyword_sets:
        for button_text in buttons:
            if any(keyword in button_text for keyword in keywords):
                matches.append(button_text)
                break
    return matches

