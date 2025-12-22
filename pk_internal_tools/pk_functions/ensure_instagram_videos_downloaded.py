import logging
import os
from pathlib import Path

import yt_dlp

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_instagram_cookies_created import ensure_instagram_cookies_created
from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_f_contained_signature import get_f_contained_signature
from pk_internal_tools.pk_functions.is_f_contained_signature import is_f_contained_signature
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE, F_INSTAGRAM_URLS_TO_DOWNLOAD_TXT, F_INSTAGRAM_COOKIES_TXT
from pk_internal_tools.pk_objects.pk_instagram_db_manager import PkInstagramDB
from pk_internal_tools.pk_objects.pk_texts import PkTexts


@ensure_seconds_measured
def ensure_instagram_videos_downloaded():
    """
    Downloads Instagram videos using yt-dlp, with proper cookie handling and DB management.
    """
    try:
        d_pnx = D_PK_WORKING

        # --- Cookie Handling ---
        if not ensure_instagram_cookies_created():
            logging.error("인스타그램 쿠키를 생성하거나 찾을 수 없어 다운로드를 진행할 수 없습니다.")
            return False
        cookie_file = Path(F_INSTAGRAM_COOKIES_TXT)
        if not cookie_file.exists() or cookie_file.stat().st_size == 0:
            logging.error(f"쿠키 생성/확인 후에도 쿠키 파일이 없거나 비어있습니다: {cookie_file}")
            return False
        logging.info(f"자동으로 관리되는 쿠키 파일을 사용합니다: {cookie_file}")
        cookie_opts = {'cookiefile': str(cookie_file)}

        # --- DB and URL Handling ---
        db_manager = PkInstagramDB()

        f_url_input_txt = Path(F_INSTAGRAM_URLS_TO_DOWNLOAD_TXT)
        urls_from_txt = _get_urls_from_txt_file(f_url_input_txt)
        db_manager.add_urls_to_db(urls_from_txt, cookie_opts)

        # --- Download Logic ---
        logging.debug("URL 입력 및 DB 업데이트 완료. 바로 다운로드를 시작합니다.")

        ydl_opts = {
            'ffmpeg_location': str(F_FFMPEG_EXE),
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(d_pnx, 'instagram_%(uploader)s_%(title)s_[%(id)s].%(ext)s'),
            'no_progress': True, 'noplaylist': True, 'merge_output_format': 'mp4',
            'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}]
        }
        ydl_opts.update(cookie_opts)

        pending_urls = db_manager.get_pending_urls()
        if not pending_urls:
            logging.info("다운로드할 새 영상이 없습니다.")
            return True

        logging.info(f"총 {len(pending_urls)}개의 영상을 다운로드합니다.")
        downloaded_files = []
        all_downloads_successful = True  # Flag to track overall success
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for url in pending_urls:
                video_id = db_manager.get_instagram_shortcode(url)
                if not video_id:
                    all_downloads_successful = False  # Treat missing video_id as a failure
                    continue

                try:
                    id_signature = f"[{video_id}]"
                    if is_f_contained_signature(signature=id_signature, d_pnx=Path(d_pnx), expected_extension=".mp4"):
                        logging.info(f"이미 다운로드된 파일입니다. 건너뜁니다: {video_id}")
                        db_manager.update_download_status(video_id, "COMPLETED")
                        continue

                    info = ydl.extract_info(url, download=True)

                    downloaded_file = get_f_contained_signature(signature=id_signature, d_pnx=Path(d_pnx), expected_extension=".mp4")
                    if downloaded_file:
                        logging.info(f"다운로드 성공: {downloaded_file.name}")
                        db_manager.update_download_status(video_id, "COMPLETED")
                        downloaded_files.append(downloaded_file)
                    else:
                        raise Exception("yt-dlp 실행 후 파일이 생성되지 않았습니다.")

                except Exception as e:
                    error_msg = str(e)
                    logging.error(f"다운로드 실패: {url}, 오류: {error_msg}")
                    db_manager.update_download_status(video_id, "FAILED", error_message=error_msg)
                    all_downloads_successful = False  # Mark as failed
                    continue

        # --- Post-download Play Option ---
        if downloaded_files:
            play_option = ensure_value_completed(key_name="다운로드한 동영상을 재생할까요", options=[PkTexts.SKIP, PkTexts.play])
            if play_option == PkTexts.play:
                logging.info(f"{PkTexts.play} 시작: {downloaded_files}")
                for video_file in downloaded_files:
                    ensure_pnx_opened_by_ext(pnx=video_file)

        return all_downloads_successful  # Return the overall success flag

    except Exception as e:
        import traceback
        logging.error(f"예상치 못한 오류 발생: {e}")
        ensure_debugged_verbose(traceback, e)
        return False


def _get_urls_from_txt_file(file_path: Path) -> list[str]:
    """Gets URLs from the input text file after user confirmation."""
    func_n = get_caller_name()
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if not file_path.exists(): file_path.touch()
    ensure_pnx_opened_by_ext(pnx=file_path)
    while True:
        ok = ensure_value_completed(
            key_name="URL 입력을 완료하셨습니까",
            options=[PkTexts.YES, PkTexts.NO],
            func_n=func_n
        )
        if ok == PkTexts.YES: break
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
