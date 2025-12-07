import logging

from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured

from typing import Optional, Tuple

@ensure_seconds_measured
def ensure_text_clicked_via_ocr_without_timelimit(text, doubleclick_mode=False):
    ensure_text_clicked_via_ocr_without_timelimit_v2(text, doubleclick_mode)


def ensure_text_clicked_via_ocr_without_timelimit_v1(text, doubleclick_mode=False):
    # TODO : 너무 느리고, 영어도 제대로 못하는 상태같아. 개선필요.
    from pk_internal_tools.pk_functions import ensure_spoken
    from pk_internal_tools.pk_functions.does_text_bounding_box_exist_via_easy_ocr import does_text_bounding_box_exist_via_easy_ocr
    from pk_internal_tools.pk_functions.click_mouse_left_btn import click_mouse_left_btn
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    ensure_spoken(rf"광학 문자 인식을 통하여 클릭할 텍스트를 찾습니다.")
    while 1:
        if does_text_bounding_box_exist_via_easy_ocr(string=text):
            click_mouse_left_btn(doubleclick_mode=doubleclick_mode)
            return True
        # ensure_slept(minutes=10)
        ensure_slept(minutes=20)


def ensure_text_clicked_via_ocr_without_timelimit_v2(
    text: str,
    doubleclick_mode: bool = False,
    lang: str = "eng",                      # "eng" 또는 "kor+eng" 등으로 조정
    conf_threshold: int = 70,               # Tesseract confidence(0~100) 필터
    fuzzy_threshold: float = 0.85,          # 부분/유사 매칭 허용치(0~1), 높을수록 엄격
    poll_minutes: int = 20,                 # 못 찾으면 다음 시도까지 대기(분). 기존 코드 스타일 유지
    move_duration: float = 0.2,             # 커서 이동 애니메이션 시간(초)
    region: Optional[Tuple[int, int, int, int]] = None,  # (left, top, width, height) 지정 시 해당 영역만 OCR
) -> bool:
    """
    ensure_text_clicked_via_ocr_without_timelimit() - pytesseract 기반 구현
    - 스크린샷(멀티모니터 포함) → Tesseract로 OCR → 원하는 텍스트 바운딩박스 찾기 → 마우스 이동 후 클릭
    - EasyOCR 의존 제거, pytesseract + OpenCV/mss/pyautogui 사용
    - Windows/WSL/Linux/Mac 호환(단, Windows 위주로 테스트 가정)
    """


    """
    Find the given text on screen via OCR (pytesseract) and click it.
    Loops until found (no time limit), sleeping 'poll_minutes' between tries.

    Args:
        text: Target text to click.
        doubleclick_mode: True to double-click, else single click.
        lang: Tesseract language hint, e.g., "eng" or "kor+eng".
        conf_threshold: Minimum confidence from tesseract 'image_to_data'.
        fuzzy_threshold: If exact substring not found, accept similar text above this ratio.
        poll_minutes: Sleep minutes between retries if not found.
        move_duration: Mouse move duration in seconds.
        region: Optional (left, top, width, height) to limit OCR area.

    Returns:
        True if clicked; function loops until success.
    """
    # --- Lazy imports (startup speed / user's preference) ---
    import os
    import sys
    import time
    from difflib import SequenceMatcher

    # 프로젝트 유틸 (존재 가정)
    from pk_internal_tools.pk_functions import ensure_spoken
    from pk_internal_tools.pk_functions.click_mouse_left_btn import click_mouse_left_btn
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept

    # Third-party
    # - pip install pytesseract opencv-python mss pyautogui pillow
    try:
        import pytesseract
    except:
        logging.debug("pytesseract import fail")
    import cv2
    import numpy as np

    # 스크린샷용: mss 멀티모니터 지원, PIL 대체
    # - pip install mss
    try:
        import mss
    except Exception as e:
        logging.debug("mss import fail")
        raise

    # --- Tesseract 실행파일 경로 설정(Windows 배려) ---
    if os.name == "nt" and not getattr(pytesseract, "pytesseract", pytesseract).__dict__.get("tesseract_cmd"):
        TESSERACT_CANDIDATES = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        ]
        for cand in TESSERACT_CANDIDATES:
            if os.path.isfile(cand):
                pytesseract.pytesseract.tesseract_cmd = cand
                break

    # --- 내부 유틸: 전체 스크린샷(또는 region) 캡처 ---
    def _grab_screen(region_xywh: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        """
        Returns a numpy array (H, W, 3) in BGR (cv2) order.
        If region_xywh is None: capture entire virtual screen (all monitors).
        region_xywh = (left, top, width, height)
        """
        with mss.mss() as sct:
            if region_xywh is None:
                # 전체 가상화면
                mon = sct.monitors[0]  # monitor[0] is the "all monitors" bounding box
                bbox = {
                    "left": mon["left"],
                    "top": mon["top"],
                    "width": mon["width"],
                    "height": mon["height"],
                }
            else:
                left, top, width, height = region_xywh
                bbox = {"left": left, "top": top, "width": width, "height": height}

            img = np.array(sct.grab(bbox))  # BGRA
            # Drop alpha channel => BGR
            img = img[:, :, :3]
            return img

    # --- 내부 유틸: Tesseract로 텍스트 + 바운딩박스 추출 ---
    def _find_text_bbox_via_tesseract(
        target: str,
        lang_: str,
        conf_min: int,
        fuzzy_min: float,
        region_xywh: Optional[Tuple[int, int, int, int]] = None,
    ) -> Optional[Tuple[int, int, int, int]]:
        """
        Returns bbox (x, y, w, h) in absolute screen coords if found; else None.
        """
        img_bgr = _grab_screen(region_xywh)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

        # 문서/자연이미지 모두를 고려해, 과도한 전처리는 피하고 원본으로 시도 후 필요시 보강
        # 필요하면 아래와 같이 대비/샤픈/그레이 등을 추가로 적용 가능:
        # img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        # img_rgb = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2RGB)

        custom_oem_psm = r'--oem 3 --psm 6'  # LSTM(default), assume a block of text
        data = pytesseract.image_to_data(
            img_rgb, lang=lang_, config=custom_oem_psm, output_type=pytesseract.Output.DICT
        )

        # image_to_data 출력: 'text', 'conf', 'left', 'top', 'width', 'height' 등
        texts = data.get("text", [])
        confs = data.get("conf", [])
        lefts = data.get("left", [])
        tops = data.get("top", [])
        widths = data.get("width", [])
        heights = data.get("height", [])

        target_norm = target.strip().lower()

        best_match = None  # (score, idx)
        for i, raw in enumerate(texts):
            if not raw or raw.strip() == "":
                continue
            try:
                conf = float(confs[i])
            except Exception:
                # 일부 환경에서 -1 또는 비수치 문자열이 들어올 수 있음
                conf = -1.0

            if conf < conf_min:
                continue

            cand = raw.strip()
            cand_norm = cand.lower()

            # n. 부분 문자열 완전일치 우선
            direct_hit = target_norm in cand_norm

            # 2) 유사도(SequenceMatcher)로 보조 판정
            ratio = SequenceMatcher(None, target_norm, cand_norm).ratio()

            if direct_hit or ratio >= fuzzy_min:
                score = (1.0 if direct_hit else 0.0) + ratio * 0.5 + (conf / 200.0)  # heuristic
                if best_match is None or score > best_match[0]:
                    best_match = (score, i)

        if best_match is None:
            return None

        _, idx = best_match
        x = int(lefts[idx])
        y = int(tops[idx])
        w = int(widths[idx])
        h = int(heights[idx])

        # region 보정: region 기준이었다면 절대 좌표로 환산
        if region_xywh is not None:
            left0, top0, _, _ = region_xywh
            x += left0
            y += top0

        return (x, y, w, h)

    # --- 내부 유틸: 마우스 이동 후 클릭 ---
    def _move_and_click_center(bbox_xywh: Tuple[int, int, int, int], dbl: bool, move_sec: float):
        import pyautogui
        x, y, w, h = bbox_xywh
        cx, cy = x + w // 2, y + h // 2
        pyautogui.moveTo(cx, cy, duration=move_sec)
        if dbl:
            click_mouse_left_btn(doubleclick_mode=True)
        else:
            click_mouse_left_btn(doubleclick_mode=False)

    # --- 본 로직 ---
    ensure_spoken(rf"광학 문자 인식을 통하여 클릭할 텍스트를 찾습니다.")
    while True:
        bbox = _find_text_bbox_via_tesseract(
            target=text,
            lang_=lang,
            conf_min=conf_threshold,
            fuzzy_min=fuzzy_threshold,
            region_xywh=region,
        )
        if bbox is not None:
            _move_and_click_center(bbox, doubleclick_mode, move_duration)
            return True

        # 원 코드 스타일을 존중하여 긴 간격 대기(분 단위)
        # 필요시 poll_minutes를 0.1~0.5 같은 소수로 줄여 폴링 주기를 짧게 할 수 있음.
        ensure_slept(minutes=poll_minutes)
