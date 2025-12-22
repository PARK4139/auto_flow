import traceback
from pathlib import Path
from typing import List
from typing import Optional

from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3


# @ensure_seconds_measured
def ensure_youtube_videos_downloaded():
    try:
        import logging
        import os
        import textwrap
        import traceback
        from pathlib import Path
        from typing import List
        from typing import Optional
        import traceback
        from pathlib import Path
        from typing import List
        from typing import Optional

        from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3

        from pk_internal_tools.pk_functions.backup_successful_cookies import backup_successful_cookies
        from pk_internal_tools.pk_functions.ensure_ubuntu_pkg_enabled import ensure_ubuntu_pkg_enabled
        from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
        from pk_internal_tools.pk_functions.ensure_values_completed import ensure_values_completed
        from pk_internal_tools.pk_functions.ensure_youtube_cookies_created import ensure_youtube_cookies_created
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        from pk_internal_tools.pk_functions.get_p import get_p
        from pk_internal_tools.pk_functions.get_pnx_ubuntu_pkg_enabled import get_pnx_ubuntu_pkg_enabled
        from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
        from pk_internal_tools.pk_objects.pk_colors import PkColors
        from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT_HIDDEN
        from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
        from pk_internal_tools.pk_objects.pk_directories import D_YOUTUBE_DOWNLOADS_CACHE
        from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
        from pk_internal_tools.pk_objects.pk_files import F_YOUTUBE_COOKIES_TXT, F_YOUTUBE_URLS_TO_DOWNLOAD_TXT
        from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3
        from pk_internal_tools.pk_objects.pk_texts import PkTexts

        d_pnx = D_PK_WORKING
        logging.debug("YouTube 쿠키 관리 시스템 초기화 중...")

        try:
            cookie_management_success = ensure_youtube_cookies_created()
            if not cookie_management_success:
                logging.debug("️ 쿠키 관리에 실패했습니다. 기본 모드로 진행합니다.")
                cookie_exists = False
            else:
                cookie_path = Path(F_YOUTUBE_COOKIES_TXT)
                cookie_exists = cookie_path.exists() and cookie_path.stat().st_size > 0

        except ImportError:
            logging.debug("️ 새로운 쿠키 관리 시스템을 사용할 수 없습니다. 기존 방식으로 진행합니다.")
            cookie_path = Path(F_YOUTUBE_COOKIES_TXT)
            cookie_exists = cookie_path.stat().st_size > 0

        if not cookie_exists:
            logging.debug("️ 쿠키 파일이 없습니다. 연령 제한 동영상은 다운로드할 수 없을 수 있습니다.")
            logging.debug(f"쿠키 파일 경로: {F_YOUTUBE_COOKIES_TXT}")
            logging.debug("자동 쿠키 관리를 위해 'ensure_youtube_cookies_created()' 함수를 실행해주세요.")

            cookie_guide = textwrap.dedent(f"""
                쿠키 파일 생성 방법:
                1. Chrome에서 YouTube에 로그인
                2. 확장 프로그램 'Get cookies.txt' 설치
                3. YouTube 페이지에서 쿠키 내보내기
                4. 파일명을 'youtube_cookies.txt'로 저장
                5. {D_PK_ROOT_HIDDEN} 폴더에 복사
                
                또는 자동 관리:
                python -m pk_external_tools.pk_functions.ensure_youtube_cookies_created
            """).lstrip()

            logging.debug(cookie_guide)

            # 쿠키 없이 계속 진행할지 확인
            question = rf"쿠키 없이 계속 진행하시겠습니까"
            ok = ensure_value_completed(key_name=question, options=[PkTexts.YES, PkTexts.NO])
            if ok != PkTexts.YES:
                return

        if is_os_windows():
            ffmpeg_location = rf'{Path(get_p(F_FFMPEG_EXE))}'
        else:
            ensure_ubuntu_pkg_enabled('ffmpeg')
            ffmpeg_location = get_pnx_ubuntu_pkg_enabled('ffmpeg')

        # ydl_opts 구성 (쿠키 파일 존재 여부에 따라)
        ydl_opts = {
            'ffmpeg_location': ffmpeg_location,
            'format': 'bestvideo+bestaudio/best',  # 최상의 비디오 & 오디오 선택
            'outtmpl': os.path.join(d_pnx, '%(title)s [%(id)s].%(ext)s'),
            'no_progress': True,  # 라이브러리의 기본 진행률 표시를 비활성화합니다.
            'noplaylist': True,
            'merge_output_format': 'mp4',  # 병합 시 MP4로 저장
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'  # 변환 후 MP4로 저장
            }],
            'geo_bypass': True,  # 지역 제한 우회
        }

        # 쿠키 파일이 존재하는 경우에만 추가
        if cookie_exists:
            ydl_opts['cookiefile'] = str(F_YOUTUBE_COOKIES_TXT)
            ydl_opts['extractor_args'] = {'youtube': ['player_client=web']}  # 딕셔너리 형태로 변경
            ydl_opts['user_agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140 Safari/537.36'
            logging.debug("쿠키 파일을 사용하여 연령 제한 동영상도 다운로드할 수 있습니다.")
        else:
            # 쿠키 없이도 시도할 수 있는 옵션 추가
            ydl_opts.update({
                'no_check_certificate': True,
                'extractor_retries': 3,
                'fragment_retries': 3,
                'retries': 3,
            })

        # YouTube 다운로드 캐시 디렉토리 설정 및 생성
        d_youtube_downloads_cache = D_YOUTUBE_DOWNLOADS_CACHE
        d_youtube_downloads_cache.mkdir(parents=True, exist_ok=True)
        f_pk_youtube_downloads_db = d_youtube_downloads_cache / "youtube_downloads.sqlite"
        logging.debug(f"YouTube 다운로드 DB 경로: {f_pk_youtube_downloads_db}")

        pk_db = PkSqlite3(db_path=f_pk_youtube_downloads_db)  # PkSqlite3 초기화 시 db_path 전달
        pk_db.ensure_table_exists("youtube_urls", {
            "id": "INTEGER PRIMARY KEY",
            "raw_url": "TEXT",
            "normalized_url": "TEXT UNIQUE",
            "download_status": "TEXT",  # PENDING, COMPLETED, FAILED
            "error_message": "TEXT",  # 다운로드 실패 시 오류 메시지
            "created_at": "TEXT",
            "updated_at": "TEXT"
        })
        pk_db.ensure_column_exists("youtube_urls", "error_message", "TEXT")

        # 시작 시 실패한 URL 관리
        _handle_failed_urls_at_startup(pk_db)

        # 다운로드 후 동작 선택
        play_option = ensure_value_completed(key_name="다운로드 후 동영상을 재생할까요", options=[PkTexts.SKIP, PkTexts.play])

        # URL 입력 파일 경로 설정 및 사용자 입력 대기
        f_url_input_txt = Path(F_YOUTUBE_URLS_TO_DOWNLOAD_TXT)
        logging.debug("URL 입력 모드")
        urls_from_txt = _get_urls_from_txt_file(f_url_input_txt)
        _add_urls_to_db(pk_db, urls_from_txt, ydl_opts, d_pnx)

        logging.debug("URL 입력 및 DB 업데이트 완료. 바로 다운로드를 시작합니다.")
        downloaded_files = _handle_db_download_mode(d_pnx, ydl_opts, pk_db, play_option, cookie_exists)  # 바로 다운로드 시작

        if play_option == PkTexts.play and downloaded_files:
            logging.debug(f"다운로드된 {len(downloaded_files)}개의 비디오를 재생합니다.")
            from pk_internal_tools.pk_objects.pk_files import F_LOSSLESSCUT_EXE

            # media_file_controller = PkLosslesscut(files_working=downloaded_files)
            # for _ in range(len(downloaded_files)):
            #     if not media_file_controller.ensure_play_next_video():
            #         logging.error("비디오 재생 중 오류가 발생했습니다.")
            #         break
            #     input("다음 비디오 재생")
        elif play_option == PkTexts.play and not downloaded_files:
            logging.debug("재생할 다운로드된 비디오가 없습니다.")
        else:
            logging.debug("비디오 재생을 건너뜁니다.")

        return True

    except Exception as e:
        ensure_debugged_verbose(traceback, e)
        return False


def _download_single_url_improved(url, d_pnx, ydl_opts, pk_db, play_option, cookie_exists) -> Optional[Path]:
    """
    Improved single-URL downloader: normalization, duplicate check, robust fallback formats,
    post-processing, and status updates. Returns the final downloaded file path when successful.
    """
    # Lazy imports (user preference)
    import logging
    from pk_internal_tools.pk_functions.normalize_youtube_url import normalize_youtube_url
    from pk_internal_tools.pk_functions.is_f_contained_signature import is_f_contained_signature
    from pk_internal_tools.pk_functions.backup_successful_cookies import backup_successful_cookies
    import yt_dlp
    from pk_internal_tools.pk_functions.ensure_values_completed import ensure_values_completed
    downloaded_file_path: Optional[Path] = None
    merge_ext = f".{ydl_opts.get('merge_output_format', 'mp4')}"  # safer default

    try:
        logging.debug(f"_download_single_url_improved called for URL: {url}")

        # 0) URL normalize
        url = normalize_youtube_url(url)

        # n. Extract info (no download)
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e)
            if "Video unavailable" in error_msg:
                logging.warning(f"영상을 찾을 수 없습니다 (삭제 또는 비공개): {url}")
                _update_download_status(pk_db, url, "FAILED", error_message="Video unavailable")
                return None  # Skip to next URL
            else:
                # For other errors during info extraction, log and fail
                logging.error(f"URL 정보 추출 중 예상치 못한 오류 발생: {url}, 오류: {error_msg}")
                _update_download_status(pk_db, url, "FAILED", error_message=error_msg)
                return None  # Skip to next URL

        # If it's a playlist-like object, pick the first entry
        if isinstance(info, dict) and ('entries' in info) and info['entries']:
            # pick the first non-null entry safely
            first = None
            for e in info['entries']:
                if e:
                    first = e
                    break
            if first is not None:
                info = first

        youtube_clip_id = info.get('id')
        clip_title = info.get('title')
        youtube_clip_id_stamp = f"[{youtube_clip_id}]"

        # 2) Already downloaded?
        if youtube_clip_id and is_f_contained_signature(
                signature=youtube_clip_id_stamp,
                d_pnx=d_pnx,
                expected_extension=merge_ext
        ):
            logging.debug(f"{youtube_clip_id_stamp} already exists: {clip_title}")
            _update_download_status(pk_db, url, "COMPLETED")
            downloaded_file_path = _handle_post_download_action(youtube_clip_id, url, d_pnx, pk_db, play_option)
            return downloaded_file_path

        # 3) Download
        logging.info(f"Download start: '{clip_title}' (URL: {url})")
        download_successful = False
        error_msg = ""

        try:
            # Primary attempt with provided options
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            download_successful = True

        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e)
            if "Requested format is not available" in error_msg:
                logging.warning(f"기본 포맷을 사용할 수 없습니다: {url}. 사용 가능한 포맷 목록을 조회하여 수동 선택을 시도합니다...")

                from pk_internal_tools.pk_functions.ensure_values_completed import ensure_values_completed_2025_10_23

                try:
                    # n. Get available formats
                    with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
                        info_full = ydl.extract_info(url, download=False)

                    if not (isinstance(info_full, dict) and 'formats' in info_full):
                        raise ValueError("포맷 정보를 가져올 수 없습니다.")

                    # n. Format them for fzf
                    fzf_options = []
                    header = f"{'ID':<10} | {'EXT':<5} | {'RESOLUTION':<18} | {'BITRATE':<8} | {'ACODEC':<15} | {'VCODEC':<15} | {'SIZE':<10} | {'NOTE'}"

                    format_list = info_full.get('formats', [])
                    # Sort by quality (height, then bitrate)
                    format_list.sort(key=lambda f: (f.get('height', 0), f.get('tbr', 0)), reverse=True)

                    for f in format_list:
                        format_id = f.get('format_id', 'N/A')
                        ext = f.get('ext', 'N/A')

                        if f.get('vcodec') == 'none':
                            resolution = 'audio only'
                        else:
                            resolution = f.get('resolution', 'video only')

                        vcodec = f.get('vcodec', 'none')
                        acodec = f.get('acodec', 'none')
                        tbr = f.get('tbr')
                        filesize = f.get('filesize') or f.get('filesize_approx')

                        filesize_str = "N/A"
                        if filesize:
                            if filesize > 1024 * 1024 * 1024:
                                filesize_str = f"{filesize / (1024 * 1024 * 1024):.1f}GB"
                            elif filesize > 1024 * 1024:
                                filesize_str = f"{filesize / (1024 * 1024):.1f}MB"
                            elif filesize > 1024:
                                filesize_str = f"{filesize / 1024:.0f}KB"
                            else:
                                filesize_str = f"{filesize}B"

                        bitrate_str = f"{tbr:.0f}k" if tbr else ""
                        note = f.get('format_note', '')

                        fzf_options.append(f"{format_id:<10} | {ext:<5} | {resolution:<18} | {bitrate_str:<8} | {acodec:<15} | {vcodec:<15} | {filesize_str:<10} | {note}")

                    # 3. Show fzf and get user selection
                    prompt_header = "다운로드할 포맷을 선택하세요 (Tab으로 영상+음성 조합). ESC로 취소."
                    full_prompt = f"{prompt_header}\n{header}"

                    selected_formats_str = ensure_values_completed(
                        key_name=full_prompt,
                        options=fzf_options,
                        multi_select=True
                    )

                    if not selected_formats_str:
                        logging.warning("사용자가 포맷 선택을 취소했습니다. 다운로드를 중단합니다.")
                        error_msg = "User cancelled format selection."
                    else:
                        # 4. Parse selection and retry
                        selected_ids = [item.split('|')[0].strip() for item in selected_formats_str]
                        user_format_selection = "+".join(selected_ids)
                        logging.info(f"사용자가 선택한 포맷으로 재시도합니다: {user_format_selection}")

                        temp_ydl_opts = dict(ydl_opts)
                        temp_ydl_opts['format'] = user_format_selection

                        try:
                            with yt_dlp.YoutubeDL(temp_ydl_opts) as temp_ydl:
                                temp_ydl.download([url])
                            download_successful = True
                            logging.info(f"사용자 선택 포맷 '{user_format_selection}' 다운로드 성공: {url}")
                        except Exception as fallback_e:
                            logging.error(f"사용자 선택 포맷 '{user_format_selection}' 다운로드 실패: {url}. err={fallback_e}")
                            error_msg = str(fallback_e)

                except Exception as interactive_e:
                    logging.error(f"포맷 선택 과정에서 오류 발생: {interactive_e}")
                    error_msg = str(interactive_e)
            else:
                # Other DownloadError
                error_msg = str(e)

        except Exception as e:
            # Unexpected errors
            error_msg = str(e)

        # 4) Post-checks / bookkeeping
        if not download_successful:
            logging.debug(f"Download error for {url}\n{error_msg}")
            _update_download_status(pk_db, url, "FAILED", error_message=error_msg)
            _handle_download_error_improved(url, error_msg, cookie_exists)
            return downloaded_file_path  # None

        # Verify file existence via signature check
        if youtube_clip_id and is_f_contained_signature(
                signature=youtube_clip_id_stamp,
                d_pnx=d_pnx,
                expected_extension=merge_ext
        ):
            logging.info(f"Download completed: '{clip_title}' (URL: {url})")
            _update_download_status(pk_db, url, "COMPLETED")

            if cookie_exists:
                try:
                    if backup_successful_cookies():
                        logging.debug("Cookies backup succeeded.")
                    else:
                        logging.debug("Cookies backup failed.")
                except ImportError:
                    logging.debug("Cookie backup system not available (ImportError).")

            downloaded_file_path = _handle_post_download_action(
                youtube_clip_id, url, d_pnx, pk_db, play_option
            )
        else:
            # Rare case: success flag true but we cannot locate the merged file
            logging.debug(f"Download marked successful but file verification failed: {clip_title}")
            _update_download_status(pk_db, url, "FAILED", error_message="file verification failed")

    except Exception as e:
        # Top-level guard to ensure no bare try remains and function always returns

        logging.error(f"Unhandled error in _download_single_url_improved: {e}\n{traceback.format_exc()}")
        try:
            _update_download_status(pk_db, url, "FAILED", error_message=str(e))
        except Exception as e:
            # Avoid masking original error with a secondary failure
            pass

    return downloaded_file_path


def _handle_failed_urls_at_startup(pk_db: PkSqlite3) -> bool:
    """
    스크립트 시작 시 이전에 실패한 URL들을 사용자에게 보여주고 관리하도록 합니다.
    """
    import logging

    from pk_internal_tools.pk_functions.ensure_values_completed import ensure_values_completed
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_objects.pk_colors import PkColors

    func_n = get_caller_name()

    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed

    cur = pk_db.pk_db_connection.cursor()
    cur.execute("SELECT normalized_url, error_message FROM youtube_urls WHERE download_status = 'FAILED'")
    failed_items = cur.fetchall()

    if not failed_items:
        return False  # No failed URLs to manage

    from pk_internal_tools.pk_functions.ensure_ansi_codes_stripped import ensure_ansi_codes_stripped

    logging.info("--- 이전에 다운로드 실패한 URL 목록 ---")
    display_options = []
    failed_urls_map = {}
    for url, msg in failed_items:
        # ANSI 코드 제거 및 None 처리
        clean_msg = ensure_ansi_codes_stripped(msg) if msg else "알 수 없는 오류"

        # fzf에 표시될 색상 적용된 문자열
        colored_display_string = f"{PkColors.BRIGHT_RED}{url} (오류: {clean_msg}){PkColors.RESET}"
        display_options.append(colored_display_string)

        # map의 키로 사용될 색상 없는 순수 텍스트
        uncolored_display_string = f"{url} (오류: {clean_msg})"
        failed_urls_map[uncolored_display_string] = url
    logging.info(f"DB에서 {len(failed_items)}개의 실패한 URL을 찾았습니다. fzf로 관리해주세요.")
    selected_display_items = ensure_values_completed(
        key_name="재시도 또는 삭제할 실패 URL을 선택하세요 (Tab으로 다중선택)",
        options=display_options,
        func_n=func_n
    )
    if not selected_display_items:
        logging.info("선택된 실패 URL이 없습니다. 계속 진행합니다.")
        return False

    selected_failed_urls = [failed_urls_map[ensure_ansi_codes_stripped(item)] for item in selected_display_items]

    action = ensure_value_completed(
        key_name=f"{len(selected_failed_urls)}개의 실패 URL에 대해 수행할 작업을 선택하세요",
        options=["재시도", "영구 삭제"]
    )

    if action == "재시도":
        logging.info(f"선택된 {len(selected_failed_urls)}개의 URL을 재시도 목록에 추가합니다.")
        for url in selected_failed_urls:
            _update_download_status(pk_db, url, "PENDING", error_message=None)
        return True  # Indicate that some URLs were retried, so main download loop should run
    elif action == "영구 삭제":
        logging.info(f"선택된 {len(selected_failed_urls)}개의 URL을 영구 삭제합니다.")
        _delete_urls_from_db(pk_db, selected_failed_urls)
        _remove_urls_from_txt_file(selected_failed_urls)
        return False  # No need to run main download loop for these

    return False  # Should not be reached


def _handle_db_download_mode(d_pnx, ydl_opts, pk_db, play_option, cookie_exists) -> List[Path]:
    """DB에서 PENDING 상태의 URL을 fzf로 선택하여 다운로드하거나 삭제하는 모드 처리"""
    import logging

    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_functions.ensure_values_completed import ensure_values_completed

    cur = pk_db.pk_db_connection.cursor()
    cur.execute("SELECT normalized_url FROM youtube_urls WHERE download_status = 'PENDING'")
    pending_urls = [row[0] for row in cur.fetchall()]

    if not pending_urls:
        logging.warning("다운로드할 PENDING 상태의 URL이 DB에 없습니다.")
        return []

    logging.info(f"DB에서 {len(pending_urls)}개의 PENDING URL을 찾았습니다. fzf로 선택해주세요.")

    # fzf로 다중 선택
    selected_urls = ensure_values_completed(
        key_name="다운로드할 URL을 선택하세요 (Tab으로 다중선택)",
        options=pending_urls,
    )

    if not selected_urls:
        logging.info("선택된 URL이 없습니다. 다운로드를 취소합니다.")
        return []

    # 다운로드 또는 삭제 선택
    action = ensure_value_completed(
        key_name=f"{len(selected_urls)}개의 URL에 대해 수행할 작업을 선택하세요",
        options=["다운로드", "목록에서 삭제"]
    )

    if action == "다운로드":
        logging.info(f"선택된 {len(selected_urls)}개의 URL 다운로드를 시작합니다.")
        downloaded_files = _download_multiple_urls_improved(selected_urls, d_pnx, ydl_opts, None, pk_db, play_option, cookie_exists)
        return downloaded_files
    elif action == "목록에서 삭제":
        _delete_urls_from_db(pk_db, selected_urls)
        _remove_urls_from_txt_file(selected_urls)
        return []
    return []


def _handle_download_error_improved(url, error_msg, cookie_exists):
    """개선된 다운로드 오류 처리 - 더 구체적인 해결 방안 제시"""
    import logging

    logging.error(f"다운로드 오류 발생: URL={url}, Error={error_msg}")  # 오류 레벨로 변경
    logging.debug(f"다운로드 오류 분석 중...")

    if "Sign in to confirm your age" in error_msg or "age-restricted" in error_msg:
        logging.warning("연령 제한 동영상입니다.")

        if not cookie_exists:
            logging.debug("해결 방법:")
            logging.debug("  1. Chrome에서 YouTube에 로그인")
            logging.debug("  2. 확장 프로그램 'Get cookies.txt' 설치")
            logging.debug("  3. YouTube 페이지에서 쿠키 내보내기")
            logging.debug("  4. 자동 쿠키 관리 실행:")
            logging.debug("     python -m pk_external_tools.pk_functions.ensure_youtube_cookies_created")
        else:
            logging.debug("쿠키 파일이 있지만 인증에 실패했습니다.")
            logging.debug("  쿠키를 새로 내보내거나 자동 관리 시스템을 사용하세요:")
            logging.debug("  python -m pk_external_tools.pk_functions.ensure_youtube_cookies_created")

    elif "This video is unavailable" in error_msg:
        logging.debug("동영상을 사용할 수 없습니다. (삭제되었거나 비공개)")

    elif "Video unavailable" in error_msg:
        logging.debug("동영상을 사용할 수 없습니다.")

    elif "copyright" in error_msg.lower():
        logging.debug("️ 저작권 문제로 다운로드할 수 없습니다.")

    elif "network" in error_msg.lower() or "connection" in error_msg.lower():
        logging.debug("네트워크 연결 문제입니다.")
        logging.debug("  인터넷 연결을 확인하고 다시 시도해주세요.")

    else:
        logging.debug(f"알 수 없는 오류: {error_msg[:100]}...")

    logging.debug("다운로드를 건너뛰고 다음 URL로 진행합니다.")


def _download_multiple_urls_improved(urls, d_pnx, ydl_opts, f_historical, pk_db, play_option, cookie_exists) -> List[Path]:
    """개선된 여러 URL 배치 다운로드"""
    from pk_internal_tools.pk_functions.is_f_contained_signature import is_f_contained_signature
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    from pk_internal_tools.pk_functions.normalize_youtube_url import normalize_youtube_url
    import logging
    import yt_dlp

    from pathlib import Path
    from typing import List

    from pk_internal_tools.pk_functions.backup_successful_cookies import backup_successful_cookies

    downloaded_files: List[Path] = []

    if is_os_windows():
        # Windows에서는 기존 방식 사용
        for url in urls:
            file_path = _download_single_url_improved(url, d_pnx, ydl_opts, pk_db, play_option, cookie_exists)
            if file_path:
                downloaded_files.append(file_path)
    else:
        # Linux에서는 배치 다운로드
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                for url in urls:
                    url = normalize_youtube_url(url)
                    try:
                        info = ydl.extract_info(url, download=False)
                        youtube_clip_id = info.get('id', None)
                        youtube_clip_id_stamp = f"[{youtube_clip_id}]"
                        clip_title = info.get('title')

                        logging.debug(f"다운로드 시작: {clip_title} ({youtube_clip_id})")

                        # 이미 다운로드된 경우
                        if is_f_contained_signature(signature=youtube_clip_id_stamp, d_pnx=d_pnx, expected_extension=f".{ydl_opts['merge_output_format']}"):
                            logging.debug(f"{youtube_clip_id_stamp} 이미 다운로드됨: {clip_title}")
                            file_path = _handle_post_download_action(youtube_clip_id, url, d_pnx, pk_db, play_option)
                            if file_path:
                                downloaded_files.append(file_path)
                            continue

                        # 다운로드 실행
                        ydl.download([url])

                        # 다운로드 확인
                        if is_f_contained_signature(signature=youtube_clip_id_stamp, d_pnx=d_pnx, expected_extension=f".{ydl_opts['merge_output_format']}"):
                            logging.debug(f"다운로드 완료: {clip_title}")
                            _update_download_status(pk_db, url, "COMPLETED")  # 상태 업데이트

                            # 연령 제한 동영상 다운로드 성공 시 쿠키 백업
                            if cookie_exists:
                                try:

                                    if backup_successful_cookies():
                                        logging.debug("성공한 쿠키를 백업했습니다.")
                                    else:
                                        logging.debug("️ 쿠키 백업에 실패했습니다.")
                                except ImportError:
                                    logging.debug("️ 쿠키 백업 시스템을 사용할 수 없습니다.")

                            file_path = _handle_post_download_action(youtube_clip_id, url, d_pnx, f_historical, pk_db, play_option)
                            if file_path:
                                downloaded_files.append(file_path)
                        else:
                            logging.debug(f"다운로드 실패: {clip_title}")
                            _update_download_status(pk_db, url, "FAILED")  # 상태 업데이트

                    except Exception as e:
                        logging.debug(f"다운로드 오류: {url}\n{str(e)}")
                        _update_download_status(pk_db, url, "FAILED")  # 상태 업데이트
                        _handle_download_error_improved(url, str(e), cookie_exists)

        except Exception as e:
            logging.debug(f"배치 다운로드 오류: {str(e)}")

    return downloaded_files


def _handle_post_download_action(youtube_clip_id, url, d_pnx, pk_db, play_option) -> Optional[Path]:
    """다운로드 후 동작 처리 (재생 또는 스킵) 및 다운로드된 파일 경로 반환"""
    from pk_internal_tools.pk_functions.get_f_contained_signature import get_f_contained_signature
    import logging
    from pathlib import Path

    f_downloaded = get_f_contained_signature(signature=youtube_clip_id, d_pnx=d_pnx)
    if f_downloaded:
        logging.debug(f"다운로드된 파일: {f_downloaded}")
        return Path(f_downloaded)
    return None


def _remove_urls_from_txt_file(urls_to_remove: list[str]):
    """
    주어진 정규화된 URL 목록을 F_YOUTUBE_URLS_TO_DOWNLOAD_TXT 파일에서 완전히 제거합니다.
    """
    from pk_internal_tools.pk_functions.normalize_youtube_url import normalize_youtube_url
    import logging
    from pathlib import Path

    from pk_internal_tools.pk_objects.pk_files import F_YOUTUBE_URLS_TO_DOWNLOAD_TXT

    file_path = Path(F_YOUTUBE_URLS_TO_DOWNLOAD_TXT)
    if not file_path.exists():
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        removed_count = 0
        normalized_urls_to_remove = {normalize_youtube_url(url) for url in urls_to_remove}

        for line in lines:
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith('#'):
                new_lines.append(line)
                continue

            normalized_current_line = normalize_youtube_url(stripped_line)

            if normalized_current_line in normalized_urls_to_remove:
                removed_count += 1
                logging.info(f"TXT 파일에서 제거: {stripped_line}")
            else:
                new_lines.append(line)

        if removed_count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            logging.info(f"{removed_count}개의 URL을 {F_YOUTUBE_URLS_TO_DOWNLOAD_TXT} 파일에서 제거했습니다.")

    except Exception as e:
        logging.error(f"TXT 파일에서 URL 제거 중 오류 발생: {e}")


def _comment_out_url_in_txt_file(normalized_url_to_complete: str):
    """txt 파일에서, 완료된 동영상에 해당하는 모든 URL 라인을 찾아 주석 처리합니다."""
    from pk_internal_tools.pk_functions.normalize_youtube_url import normalize_youtube_url
    import logging
    from pathlib import Path

    from pk_internal_tools.pk_objects.pk_files import F_YOUTUBE_URLS_TO_DOWNLOAD_TXT

    try:
        file_path = Path(F_YOUTUBE_URLS_TO_DOWNLOAD_TXT)
        if not file_path.exists():
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        changed = False
        for line in lines:
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith('#'):
                new_lines.append(line)
                continue

            # 현재 라인을 정규화하여 완료된 URL과 일치하는지 확인
            normalized_current_line = normalize_youtube_url(stripped_line)

            if normalized_current_line == normalized_url_to_complete:
                new_lines.append(f"# {line}")
                changed = True
                logging.info(f"주석 처리: {stripped_line}")
            else:
                new_lines.append(line)

        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

    except Exception as e:
        logging.error(f"URL 주석 처리 중 오류 발생: {e}")


def _get_urls_from_txt_file(file_path: Path) -> list[str]:
    """
    사용자에게 URL을 입력할 .txt 파일 경로를 안내하고, 해당 파일에 URL을 작성하도록 유도합니다.
    파일 내용을 읽어 URL 목록을 반환합니다.
    """
    # lazy import
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext  # Moved here for lazy import
    import logging

    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    logging.debug(f"[_get_urls_from_txt_file] 시작. 파일 경로: {file_path}")  # 로깅 추가

    # 파일 생성 전 상위 디렉토리 존재 확인 및 생성
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if not file_path.exists():
        file_path.touch()
        logging.debug(f"[_get_urls_from_txt_file] URL을 입력할 파일이 생성되었습니다: {file_path}")  # 로깅 추가
        logging.debug("이 파일에 다운로드할 YouTube URL을 한 줄에 하나씩 입력해주세요.")

    # 파일을 자동으로 열어줍니다.
    if QC_MODE:
        ensure_pnx_opened_by_ext(pnx=file_path)  # pk_option
        pass
    else:
        ensure_pnx_opened_by_ext(pnx=file_path)

    while True:
        logging.debug(f"[_get_urls_from_txt_file] URL 입력 파일: {file_path}")  # 로깅 추가
        if QC_MODE:
            # user_choice = PkTexts.YES # pk_option
            user_choice = ensure_value_completed(
                key_name="URL 입력을 완료하셨습니까",
                options=[PkTexts.NO, PkTexts.YES]
            )
        else:
            user_choice = ensure_value_completed(
                key_name="URL 입력을 완료하셨습니까",
                options=[PkTexts.NO, PkTexts.YES]
            )
        logging.debug(f"[_get_urls_from_txt_file] 사용자 선택: {user_choice}")  # 로깅 추가
        if user_choice == PkTexts.YES:
            break
        else:
            logging.debug("URL 입력을 기다리는 중...")

    with open(file_path, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
    logging.debug(f"[_get_urls_from_txt_file] TXT 파일에서 읽어온 최종 URL 목록 ({len(urls)}개): {urls}")  # 로깅 추가
    return urls


def _add_urls_to_db(pk_db: PkSqlite3, urls: list[str], ydl_opts: dict, d_pnx: str):
    """
    .txt 파일에서 읽은 URL 목록을 분석하여 유효한 단일 동영상파일 DB에 추가하고 중복을 처리합니다.
    yt-dlp를 사용하여 각 URL의 유형(단일 동영상, 재생목록 등)을 확인합니다.
    """
    # lazy import
    from datetime import datetime
    import yt_dlp
    from pk_internal_tools.pk_functions.normalize_youtube_url import normalize_youtube_url
    import re  # For playlist handling
    import logging
    import os

    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed

    logging.debug(f"[_add_urls_to_db] 시작. 입력 URL 개수: {len(urls)}")  # 로깅 추가

    # URL 유효성 검사를 위한 최소한의 yt-dlp 옵션
    validation_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': 'in_playlist',  # 재생목록의 경우 동영상 목록을 가져오지 않고 정보만 확인
    }

    cur = pk_db.pk_db_connection.cursor()

    with yt_dlp.YoutubeDL(validation_opts) as ydl:
        for raw_url in urls:
            logging.debug(f"[_add_urls_to_db] 처리 중인 raw_url: {raw_url}")  # 로깅 추가
            info = None  # Initialize info
            try:
                # URL 정보 추출 (다운로드는 안 함)
                info = ydl.extract_info(raw_url, download=False)
                logging.debug(f"[_add_urls_to_db] 정보 추출 성공: {raw_url}")  # 로깅 추가
            except Exception as e:
                logging.warning(f"[_add_urls_to_db] URL 정보 추출 실패 (yt-dlp): {raw_url}. 오류: {e}. 일단 PENDING으로 추가 시도.")
                # 정보 추출에 실패한 경우에도 DB에 PENDING 상태로 추가
                normalized_url = normalize_youtube_url(raw_url)
                cur.execute("SELECT download_status FROM youtube_urls WHERE normalized_url = ?", (normalized_url,))
                result = cur.fetchone()

                if not result:  # DB에 없는 경우에만 새로 추가
                    now = datetime.now().isoformat()
                    sql = "INSERT INTO youtube_urls (raw_url, normalized_url, download_status, created_at, updated_at, error_message) VALUES (?, ?, ?, ?, ?, ?)"
                    params = (raw_url, normalized_url, "PENDING", now, now, str(e))
                    cur.execute(sql, params)
                    pk_db.pk_db_connection.commit()
                    logging.debug(f"[_add_urls_to_db] 정보 추출 실패 URL을 DB에 PENDING으로 추가했습니다: {raw_url}")
                else:  # 이미 DB에 있는 경우, 상태를 PENDING으로 업데이트
                    now = datetime.now().isoformat()
                    sql = "UPDATE youtube_urls SET download_status = ?, error_message = ?, updated_at = ? WHERE normalized_url = ?"
                    params = ("PENDING", str(e), now, normalized_url)
                    cur.execute(sql, params)
                    pk_db.pk_db_connection.commit()
                    logging.debug(f"[_add_urls_to_db] 정보 추출 실패 URL의 상태를 PENDING으로 업데이트했습니다: {raw_url}")
                continue  # 다음 URL로 넘어감

            # 'entries' 키가 있으면 재생목록 또는 채널로 간주하고 사용자에게 질문
            if info and 'entries' in info:  # Check if info is not None before accessing 'entries'
                logging.debug(f"[_add_urls_to_db] 재생목록/채널 감지: {raw_url}")  # 로깅 추가
                playlist_title = info.get('title', raw_url)
                question = f"재생목록(또는 채널) '{playlist_title}'이 발견되었습니다. 모든 동영상을 다운로드할까요"
                user_choice = ensure_value_completed(key_name=question, options=["모두 다운로드", "건너뛰기"])
                logging.debug(f"[_add_urls_to_db] 재생목록 처리 사용자 선택: {user_choice}")  # 로깅 추가

                if user_choice == "건너뛰기":
                    logging.info(f"[_add_urls_to_db] 재생목록 다운로드를 건너뜁니다: {raw_url}")
                    continue
                else:  # "모두 다운로드"
                    logging.info(f"[_add_urls_to_db] 재생목록의 모든 동영상 다운로드를 시작합니다: {raw_url}")

                    playlist_ydl_opts = ydl_opts.copy()
                    playlist_ydl_opts['noplaylist'] = False

                    # Sanitize playlist_title for use as a directory name
                    sanitized_title = re.sub(r'[\\/*?:"<>|]', "", playlist_title)

                    # Update output template to save into a sub-directory named after the playlist
                    playlist_ydl_opts['outtmpl'] = os.path.join(d_pnx, sanitized_title, '%(title)s [%(id)s].%(ext)s')

                    try:
                        with yt_dlp.YoutubeDL(playlist_ydl_opts) as playlist_ydl:
                            playlist_ydl.download([raw_url])
                        logging.info(f"[_add_urls_to_db] 재생목록 다운로드가 완료되었습니다: {playlist_title}")
                    except Exception as pl_e:
                        logging.error(f"[_add_urls_to_db] 재생목록 다운로드 중 오류 발생: {playlist_title}, error: {pl_e}")

                    # After attempting download, skip adding to DB and move to the next URL
                    continue
            # 유효한 단일 동영상 URL의 경우, DB 처리 진행
            normalized_url = normalize_youtube_url(raw_url)
            cur.execute("SELECT download_status FROM youtube_urls WHERE normalized_url = ?", (normalized_url,))
            result = cur.fetchone()

            if result:
                existing_status = result[0]
                if existing_status == "COMPLETED":
                    logging.debug(f"[_add_urls_to_db] 이미 다운로드 완료된 URL입니다. 건너뜁니다: {raw_url}")
                    _comment_out_url_in_txt_file(normalized_url)
                else:
                    now = datetime.now().isoformat()
                    sql = "UPDATE youtube_urls SET download_status = ?, error_message = NULL, updated_at = ? WHERE normalized_url = ?"
                    params = ("PENDING", now, normalized_url)
                    cur.execute(sql, params)
                    pk_db.pk_db_connection.commit()
                    logging.debug(f"[_add_urls_to_db] 기존 URL을 다시 다운로드하도록 PENDING으로 업데이트했습니다: {raw_url}")
            else:
                now = datetime.now().isoformat()
                sql = "INSERT INTO youtube_urls (raw_url, normalized_url, download_status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)"
                params = (raw_url, normalized_url, "PENDING", now, now)
                cur.execute(sql, params)
                logging.debug(f"[_add_urls_to_db] 새로운 URL을 DB에 추가했습니다: {raw_url}")

            pk_db.pk_db_connection.commit()


def _delete_urls_from_db(pk_db: PkSqlite3, urls_to_delete: list[str]):
    """
    주어진 정규화된 URL 목록을 DB에서 삭제합니다.
    """
    import logging

    if not urls_to_delete:
        return

    cur = pk_db.pk_db_connection.cursor()
    try:
        cur.executemany("DELETE FROM youtube_urls WHERE normalized_url = ?", [(url,) for url in urls_to_delete])
        pk_db.pk_db_connection.commit()
        logging.info(f"{len(urls_to_delete)}개의 URL을 DB에서 삭제했습니다.")
    except Exception as e:
        logging.error(f"DB에서 URL 삭제 중 오류 발생: {e}")
        pk_db.pk_db_connection.rollback()


def _update_download_status(pk_db: PkSqlite3, normalized_url: str, status: str, error_message: Optional[str] = None):
    """
    주어진 정규화된 URL의 download_status와 오류 메시지를 업데이트합니다.
    완료 시 .txt 파일의 해당 URL을 주석 처리합니다.
    """
    from datetime import datetime
    import logging

    now = datetime.now().isoformat()
    cur = pk_db.pk_db_connection.cursor()

    if status == "FAILED":
        sql = "UPDATE youtube_urls SET download_status = ?, error_message = ?, updated_at = ? WHERE normalized_url = ?"
        params = (status, error_message, now, normalized_url)
    else:
        # 성공 또는 다른 상태의 경우 오류 메시지를 초기화합니다.
        sql = "UPDATE youtube_urls SET download_status = ?, error_message = NULL, updated_at = ? WHERE normalized_url = ?"
        params = (status, now, normalized_url)

    cur.execute(sql, params)
    pk_db.pk_db_connection.commit()
    logging.debug(f"Normalized URL {normalized_url}의 다운로드 상태를 {status}로 업데이트했습니다.")

    # 다운로드 완료 시 .txt 파일 주석 처리
    if status == "COMPLETED":
        _comment_out_url_in_txt_file(normalized_url)
