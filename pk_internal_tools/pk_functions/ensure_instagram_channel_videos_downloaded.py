import logging
import os
import textwrap
import traceback
from pathlib import Path
from typing import List, Optional

import yt_dlp

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_functions.ensure_instagram_cookies_created import ensure_instagram_cookies_created
from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_f_contained_signature import get_f_contained_signature
from pk_internal_tools.pk_functions.is_f_contained_signature import is_f_contained_signature
from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING, D_PK_CACHE
from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE, F_INSTAGRAM_COOKIES_TXT
from pk_internal_tools.pk_objects.pk_instagram_db_manager import PkInstagramDB
from pk_internal_tools.pk_objects.pk_texts import PkTexts


@ensure_seconds_measured
def ensure_instagram_channel_videos_downloaded():
    """
    Downloads Instagram channel (user account) videos using yt-dlp, with proper cookie handling and DB management.
    """
    try:
        d_pnx = D_PK_WORKING
        logging.debug("Instagram 채널 비디오 다운로드 시스템 시작")

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
        
        # ensure_instagram_db_manager.py 파일에서 PkInstagramDB의 테이블에 channel_name 컬럼 추가
        _ensure_channel_name_column_exists(db_manager)

        # 사용자에게 채널 이름 또는 URL 입력 받기
        channel_input = ensure_value_completed(
            key_name="인스타그램_채널_이름_또는_URL_입력", # 파일 시스템에 안전한 이름으로 변경
            guide_text="다운로드할 인스타그램 채널 이름 또는 URL을 입력하세요 (예: @username 또는 https://www.instagram.com/username/)"
        )

        if not channel_input:
            logging.info("채널 입력이 없어 다운로드를 취소합니다.")
            return True

        # 채널 URL 정규화 (사용자 이름 -> URL)
        channel_url = _normalize_channel_input_to_url(channel_input)
        if not channel_url:
            logging.error(f"유효하지 않은 채널 입력 형식입니다: {channel_input}")
            return False
            
        logging.info(f"채널 URL: {channel_url} 에서 비디오 목록을 수집합니다.")
        
        # yt-dlp를 사용하여 채널의 모든 비디오/게시물 URL 추출
        urls_from_channel = _get_urls_from_channel(channel_url, cookie_opts)
        if not urls_from_channel:
            logging.warning(f"'{channel_input}' 채널에서 다운로드할 비디오를 찾을 수 없거나 접근할 수 없습니다.")
            return True

        db_manager.add_urls_to_db(urls_from_channel, cookie_opts, channel_name=channel_input) # channel_name 추가
        
        # --- Download Logic (existing logic similar to ensure_instagram_videos_downloaded) ---
        logging.debug("URL 입력 및 DB 업데이트 완료. 바로 다운로드를 시작합니다.")

        ydl_opts = {
            'ffmpeg_location': str(F_FFMPEG_EXE),
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(d_pnx, 'instagram_%(uploader)s_%(title)s_[%(id)s].%(ext)s'),
            'no_progress': True, 'noplaylist': True, 'merge_output_format': 'mp4',
            'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}]
        }
        ydl_opts.update(cookie_opts)

        pending_urls = db_manager.get_pending_urls() # 채널에서 수집된 PENDING URL 포함
        if not pending_urls:
            logging.info("다운로드할 새 영상이 없습니다.")
            return True

        logging.info(f"총 {len(pending_urls)}개의 영상을 다운로드합니다.")
        downloaded_files = []
        all_downloads_successful = True
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for url_entry in pending_urls: # PkInstagramDB의 get_pending_urls는 (raw_url, video_id, channel_name) 튜플을 반환하도록 수정될 수 있음.
                # 현재 PkInstagramDB.get_pending_urls는 raw_url만 반환하므로, 여기서는 raw_url만 사용
                url = url_entry # assume url_entry is raw_url

                video_id = db_manager.get_instagram_shortcode(url)
                if not video_id:
                    all_downloads_successful = False
                    continue

                try:
                    id_signature = f"[{video_id}]"
                    if is_f_contained_signature(signature=id_signature, d_pnx=Path(d_pnx), expected_extension=".mp4"):
                        logging.info(f"이미 다운로드된 파일입니다. 건너킵니다: {video_id}")
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
                    all_downloads_successful = False
                    continue

        # --- Post-download Play Option ---
        if downloaded_files:
            play_option = ensure_value_completed(key_name="다운로드한 동영상을 재생할까요", options=[PkTexts.SKIP, PkTexts.play])
            if play_option == PkTexts.play:
                logging.info(f"{PkTexts.play} 시작: {downloaded_files}")
                for video_file in downloaded_files:
                    ensure_pnx_opened_by_ext(pnx=video_file)

        return all_downloads_successful

    except Exception as e:
        import traceback
        logging.error(f"예상치 못한 오류 발생: {e}")
        ensure_debugged_verbose(traceback, e)
        return False


def _normalize_channel_input_to_url(channel_input: str) -> Optional[str]:
    """
    사용자 입력을 정규화된 인스타그램 채널 URL로 변환합니다.
    예: @username -> https://www.instagram.com/username/
        https://www.instagram.com/username/ -> https://www.instagram.com/username/
    """
    if channel_input.startswith("https://www.instagram.com/"):
        if not channel_input.endswith("/"): # /로 끝나지 않으면 추가
            channel_input += "/"
        return channel_input
    elif channel_input.startswith("@"):
        username = channel_input[1:]
        return f"https://www.instagram.com/{username}/"
    else: # 사용자 이름만 입력된 경우
        return f"https://www.instagram.com/{channel_input}/"
    return None # 유효하지 않은 형식


def _get_urls_from_channel(channel_url: str, cookie_opts: dict) -> List[str]:
    """
    yt-dlp를 사용하여 주어진 인스타그램 채널 URL에서 모든 비디오/게시물 URL을 추출합니다.
    """
    urls = []
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True, # flat extract for playlists/channels
            'force_generic_extractor': False, # Instagram is a specific extractor
            'cookiefile': cookie_opts.get('cookiefile'),
            'ignoreerrors': True, # 개별 동영상 오류 무시하고 계속 진행
            'verbose': True, # 상세 로그 활성화
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logging.debug(f"yt-dlp로 채널 정보 추출 시도: {channel_url}")
            info = ydl.extract_info(channel_url, download=False)
            
            if info is None: # None 체크 추가
                logging.warning(f"yt-dlp가 채널 '{channel_url}'의 정보를 추출하지 못했습니다 (None 반환).")
                return urls # 빈 리스트 반환
            
            if 'entries' in info:
                for entry in info['entries']:
                    if entry and 'url' in entry: # 비디오만 추출
                        # yt-dlp의 Instagram extractor는 type이 'Instagram Post'인 entry를 반환합니다.
                        # 여기에 'extractor_key': 'Instagram'와 같은 정보가 있다면 더 정확할 수 있습니다.
                        urls.append(entry['url'])
                    elif entry and 'webpage_url' in entry: # Fallback for entries that only have webpage_url
                         urls.append(entry['webpage_url'])
            else:
                # 단일 게시물 URL이 입력되었을 경우를 대비
                if 'url' in info:
                    urls.append(info['url'])
                elif 'webpage_url' in info:
                    urls.append(info['webpage_url'])

    except yt_dlp.utils.DownloadError as e:
        logging.error(f"yt-dlp로 채널 '{channel_url}'의 비디오 목록을 수집하는 데 실패했습니다: {e}")
    except Exception as e:
        logging.error(f"예상치 못한 오류로 채널 '{channel_url}'의 비디오 목록 수집에 실패했습니다: {e}")
    
    return urls

def _ensure_channel_name_column_exists(db_manager: PkInstagramDB):
    """
    PkInstagramDB의 instagram_urls 테이블에 'channel_name' 컬럼이 없으면 추가합니다.
    """
    cur = db_manager.pk_db.pk_db_connection.cursor()
    cur.execute("PRAGMA table_info(instagram_urls)")
    columns = [info[1] for info in cur.fetchall()]
    if 'channel_name' not in columns:
        logging.info("instagram_urls 테이블에 'channel_name' 컬럼을 추가합니다.")
        cur.execute("ALTER TABLE instagram_urls ADD COLUMN channel_name TEXT")
        db_manager.pk_db.pk_db_connection.commit()
