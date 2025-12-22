import json
import logging
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

from pk_internal_tools.pk_functions.alert_as_gui import alert_as_gui
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_objects.pk_directories import D_PK_COOKIES
from pk_internal_tools.pk_objects.pk_files import F_INSTAGRAM_COOKIES_TXT
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name


# ... (생략)

@ensure_seconds_measured
def ensure_instagram_cookies_created(force_refresh=False):
    """
    Instagram 쿠키를 생성 및 관리하는 메인 함수. YouTube 로직을 기반으로 함.
    """
    D_PK_COOKIES.mkdir(parents=True, exist_ok=True)  # Ensure the cookie directory exists
    cookie_file = F_INSTAGRAM_COOKIES_TXT
    cookie_meta_file = D_PK_COOKIES / "instagram_cookies_metadata.json"

    logging.debug("Instagram 쿠키 관리 시스템 시작")

    if force_refresh:
        logging.debug("강제 갱신 모드: 기존 쿠키를 백업하고 새로 생성합니다.")
        return _force_refresh_cookies(cookie_file, cookie_meta_file)

    cookie_status = _diagnose_cookie_status(cookie_file, cookie_meta_file)

    if cookie_status == "valid":
        logging.debug("인스타그램 쿠키가 유효합니다.")
        return True
    elif cookie_status == "expired":
        logging.debug("️ 인스타그램 쿠키가 만료되었습니다. 갱신이 필요합니다.")
        return _refresh_cookies(cookie_file, cookie_meta_file)
    elif cookie_status == "missing":
        logging.debug("인스타그램 쿠키 파일이 없습니다. 새로 생성합니다.")
        return _create_new_cookies(cookie_file, cookie_meta_file)
    elif cookie_status == "invalid":
        logging.debug("️ 인스타그램 쿠키 파일이 손상되었습니다. 새로 생성합니다.")
        return _create_new_cookies(cookie_file, cookie_meta_file)

    return False


def _diagnose_cookie_status(cookie_file: Path, cookie_meta_file: Path) -> str:
    if not cookie_file.exists() or cookie_file.stat().st_size == 0:
        return "missing"
    if cookie_meta_file.exists():
        try:
            with open(cookie_meta_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            if 'expires_at' in metadata and datetime.now() > datetime.fromisoformat(metadata['expires_at']):
                return "expired"
            return "valid"
        except (json.JSONDecodeError, KeyError, ValueError):
            return "invalid"
    # 메타데이터 파일이 없어도, 쿠키 파일이 존재하고 비어있지 않으면 유효하다고 판단
    return "valid"


def _refresh_cookies(cookie_file: Path, cookie_meta_file: Path) -> bool:
    logging.debug("인스타그램 쿠키 갱신 중...")
    return _create_new_cookies(cookie_file, cookie_meta_file)


def _force_refresh_cookies(cookie_file: Path, cookie_meta_file: Path) -> bool:
    logging.debug("인스타그램 쿠키 강제 갱신 중...")
    return _create_new_cookies(cookie_file, cookie_meta_file)


def _create_new_cookies(cookie_file: Path, cookie_meta_file: Path) -> bool:
    logging.debug("🆕 새 인스타그램 쿠키 생성 중 (브라우저에서 직접 추출)...")
    try:
        cmd = [
            "yt-dlp",
            "--cookies-from-browser", "chrome",
            "--cookies", str(cookie_file),
            "--print", "id",
            "https://www.instagram.com"
        ]
        logging.debug(f"yt-dlp를 이용한 쿠키 추출 시도: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)

        if result.returncode == 0 and cookie_file.exists() and cookie_file.stat().st_size > 0:
            _create_cookie_metadata(cookie_file, cookie_meta_file)
            logging.info("yt-dlp를 통해 브라우저에서 쿠키를 성공적으로 추출했습니다.")
            return True
        else:
            logging.warning(f"yt-dlp를 이용한 쿠키 추출에 실패했습니다. Stderr: {result.stderr.strip()}")
            return _create_cookies_fallback(cookie_file, cookie_meta_file)

    except Exception as e:
        logging.error(f"yt-dlp 쿠키 생성 중 예외 발생: {e}, 대안 방식으로 시도합니다.")
        return _create_cookies_fallback(cookie_file, cookie_meta_file)


def _create_cookies_fallback(cookie_file: Path, cookie_meta_file: Path) -> bool:
    logging.debug("대안 방식: browser_cookie3로 쿠키 생성 시도")
    try:
        import browser_cookie3
        from http.cookiejar import MozillaCookieJar

        logging.debug("Chrome 브라우저에서 instagram.com 도메인 쿠키를 찾습니다...")
        cj = browser_cookie3.chrome(domain_name='instagram.com')

        if not cj:
            logging.warning("browser_cookie3가 Chrome에서 인스타그램 쿠키를 찾지 못했습니다. 수동 가이드로 전환합니다.")
            return _guide_user_for_manual_cookie_creation(cookie_file)

        jar = MozillaCookieJar(str(cookie_file))
        for cookie in cj:
            jar.set_cookie(cookie)
        jar.save(ignore_discard=True, ignore_expires=True)

        if cookie_file.exists() and cookie_file.stat().st_size > 0:
            _create_cookie_metadata(cookie_file, cookie_meta_file)
            logging.info("대안 방식(browser_cookie3)으로 쿠키 생성에 성공했습니다.")
            return True
        else:
            logging.error("대안 방식으로 쿠키 파일을 생성했지만, 파일이 비어있거나 생성되지 않았습니다. 수동 가이드로 전환합니다.")
            return _guide_user_for_manual_cookie_creation(cookie_file)
    except Exception as e:
        logging.error(f"browser_cookie3 쿠키 생성 중 치명적인 오류 발생: {e}. 수동 가이드로 전환합니다.")
        return _guide_user_for_manual_cookie_creation(cookie_file)


def _guide_user_for_manual_cookie_creation(cookie_file: Path) -> bool:
    # Lazy imports
    import webbrowser
    import textwrap
    try:
        import pyperclip
    except ImportError:
        logging.error("'pyperclip' 라이브러리가 필요합니다. `pip install pyperclip` 명령어로 설치해주세요.")
        return False
    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    func_n = get_caller_name()

    logging.warning("모든 자동 쿠키 추출 방법이 실패했습니다. 클립보드를 이용한 수동 가이드 모드를 시작합니다.")

    extension_url = "https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm"

    guide_text = textwrap.dedent(f"""
    ------------------------------------------------------------------------------------
    [클립보드를 이용한 수동 쿠키 생성 가이드]

    n. 'Chrome에 추가' 버튼을 눌러 설치하세요. # 'Cookie-Editor' 확장 프로그램 추가
    n. 인스타그램(instagram.com) 탭으로 이동하여 로그인합니다.
    n. click 'Cookie-Editor' 아이콘 / 'Export' / NetScape   # save to clipboard as json
    ------------------------------------------------------------------------------------
    """)
    logging.info(guide_text)
    alert_as_gui(guide_text)

    try:
        webbrowser.open(extension_url)
    except Exception as e:
        logging.error(f"웹 브라우저를 여는 데 실패했습니다: {e}")

    user_response = ensure_value_completed(
        key_name="쿠키 정보 클립보드 복사 가이드를 수행하셨습니까",
        options=[PkTexts.YES, PkTexts.NO],
        func_n=func_n,
    )

    if user_response == PkTexts.NO:
        logging.error("사용자가 수동 쿠키 생성을 취소했습니다.")
        return False

    try:
        cookie_data_from_clipboard = pyperclip.paste()
        if not cookie_data_from_clipboard or "instagram.com" not in cookie_data_from_clipboard:
            logging.error("클립보드에 유효한 인스타그램 쿠키 정보가 없습니다. 다시 시도해주세요.")
            return False

        cookie_file.parent.mkdir(parents=True, exist_ok=True)
        with open(cookie_file, 'w', encoding='utf-8') as f:
            f.write(cookie_data_from_clipboard)

        logging.info(f"클립보드의 쿠키 정보를 '{cookie_file}' 파일에 저장했습니다.")
        logging.info("이제 메모장에서 파일 내용을 확인하고, 이상이 없으면 저장 후 창을 닫아주세요.")

        ensure_pnx_opened_by_ext(pnx=cookie_file)

        edit_response = ensure_value_completed(
            key_name="파일 내용을 확인하고 저장하셨습니까",
            options=[PkTexts.YES, PkTexts.NO]
        )

        if edit_response == PkTexts.NO:
            logging.error("사용자가 파일 확인 및 저장을 취소했습니다.")
            return False

        if cookie_file.exists() and cookie_file.stat().st_size > 0:
            _create_cookie_metadata(cookie_file, cookie_file.with_suffix('.json'))
            logging.info("수동 쿠키 파일 생성을 완료했습니다.")
            return True
        else:
            logging.error("최종 쿠키 파일이 생성되지 않았거나 비어있습니다.")
            return False

    except Exception as e:
        logging.error(f"클립보드 쿠키 처리 중 치명적인 오류 발생: {e}")
        return False


def _create_cookie_metadata(cookie_file: Path, cookie_meta_file: Path):
    try:
        metadata = {
            'created_at': datetime.now().isoformat(),
            'file_modified': datetime.fromtimestamp(cookie_file.stat().st_mtime).isoformat(),
            'file_size': cookie_file.stat().st_size,
            'expires_at': (datetime.now() + timedelta(days=1)).isoformat(),  # 1일 후 만료
            'version': '1.0',
            'method': 'mixed'
        }
        with open(cookie_meta_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.debug(f"️ 인스타그램 쿠키 메타데이터 생성 실패: {e}")
