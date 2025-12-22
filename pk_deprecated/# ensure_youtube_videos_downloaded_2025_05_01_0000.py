from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_youtube_videos_downloaded_2025_05_01_0000():
    from pk_internal_tools.pk_objects.pk_files import F_DOWNLOAD_YOUTUBE_VIDEOS_HISTORY
    from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
    from pk_internal_tools.pk_functions.ensure_ubuntu_pkg_enabled import ensure_ubuntu_pkg_enabled
    from pk_internal_tools.pk_functions.get_p import get_p
    from pathlib import Path
    from pk_internal_tools.pk_functions.get_pnx_ubuntu_pkg_enabled import get_pnx_ubuntu_pkg_enabled
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
    import logging
    from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
    from pk_internal_tools.pk_objects.pk_files import F_FFMPEG_EXE
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    from pk_internal_tools.pk_objects.pk_sqlite3 import PkSqlite3
    from pk_internal_tools.pk_functions.ensure_youtube_cookies_created import ensure_youtube_cookies_created
    from pk_internal_tools.pk_objects.pk_files import F_CHORME_YOUTUBE_COOKIE

    import os
    import sys
    try:

        d_pnx = D_PK_WORKING

        # 쿠키 파일 경로 및 확인
        file_cookie = F_CHORME_YOUTUBE_COOKIE
        cookie_exists = file_cookie.exists()

        if not cookie_exists:
            ensure_youtube_cookies_created()

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
            'quiet': False,
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
            ydl_opts['cookiefile'] = str(file_cookie)
            logging.debug("쿠키 파일을 사용하여 연령 제한 동영상도 다운로드할 수 있습니다.")
        else:
            # 쿠키 없이도 시도할 수 있는 옵션 추가
            ydl_opts.update({
                'no_check_certificate': True,
                'extractor_retries': 3,
                'fragment_retries': 3,
                'retries': 3,
            })

        f_historical = F_DOWNLOAD_YOUTUBE_VIDEOS_HISTORY
        ensure_pnx_made(pnx=f_historical, mode='f')

        pk_db = PkSqlite3()

        # 다운로드 모드 선택
        download_mode = pk_db.get_state_value(db_id='download_mode')
        if not download_mode:
            pk_db.reset_values(db_id='download_mode')
            pk_db.save_value_from_options(question="다운로드 모드를 선택하세요", options=["URL 입력 모드", "히스토리 URLs 다운로드 모드"], db_id='download_mode')
            download_mode = pk_db.get_state_value(db_id='download_mode')

        # 다운로드 후 동작 선택
        value = pk_db.get_state_value(db_id='download_option')
        if not value:
            pk_db.reset_values(db_id='download_option')
            pk_db.save_value_from_options(question="다운로드 후 동영상을 재생할까요", options=[PkTexts.SKIP, PkTexts.play], db_id='download_option')
            value = pk_db.get_state_value(db_id='download_option')

        # 히스토리 파일 열기 옵션
        value_historical = pk_db.get_state_value(db_id='open historical f')
        if value_historical == PkTexts.YES:
            ensure_pnx_opened_by_ext(pnx=f_historical)
            pk_db.set_values(db_id="open historical f", values="YES, one time done")  # 프로그램 실행 중 1회만 실행제한

        if download_mode == "URL 입력 모드":
            logging.debug("URL 입력 모드")
            _handle_url_input_mode(f_historical, d_pnx, ydl_opts, pk_db, value, cookie_exists)
        else:
            logging.debug("히스토리 URLs 다운로드 모드")
            _handle_history_download_mode(f_historical, d_pnx, ydl_opts, pk_db, value, cookie_exists)

    except SystemExit as e:
        if e.code == 0:
            logging.debug(f'[{PkTexts.NORMAL_EXIT}: SystemExit(0)]')
            sys.exit(0)
        else:
            raise  # 비정상 종료는 그대로 propagate
    except Exception as e:
        import traceback
        import sys
        traceback.print_exc()


def _handle_url_input_mode(f_historical, d_pnx, ydl_opts, pk_db, play_option, cookie_exists):
    """URL 입력 모드 처리"""
    from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    from pk_internal_tools.pk_functions.get_str_from_clipboard import get_str_from_clipboard
    from pk_internal_tools.pk_functions.is_url import is_url
    from pk_internal_tools.pk_functions.ensure_list_written_to_f import ensure_list_written_to_f
    from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
    from pk_internal_tools.pk_objects.pk_texts import PK_BLANK
    import sys

    # 클립보드에서 URL 가져오기
    youtube_video_url_from_clipboard = get_str_from_clipboard()
    marker_for_clipboard = f'{PK_BLANK}(url from clipboard)'
    youtube_video_url_from_clipboard = rf"{youtube_video_url_from_clipboard}{marker_for_clipboard}"

    # 히스토리에서 URL 목록 가져오기
    historical_lines = get_historical_list(f=f_historical)

    # 옵션 구성 (클립보드 + 히스토리)
    options = []
    if youtube_video_url_from_clipboard and is_url(youtube_video_url_from_clipboard):
        options.append(youtube_video_url_from_clipboard)
    options.extend(historical_lines)

    # URL 입력 받기
    if QC_MODE:
        answer = rf"https://www.youtube.com/watch?v=6jQOQQA7-eA"
    else:
        answer = ensure_value_completed(key_name='YOUTUBE URL TO DOWNLOAD', options=options)
    answer = answer.strip()
    if answer.lower() in ["x", "exit", "q", "quit"]:
        sys.exit(0)

    url = answer
    ensure_list_written_to_f(f=f_historical, working_list=[url] + historical_lines, mode="w")
    url = url.replace(marker_for_clipboard, "")

    # 단일 URL 다운로드
    _download_single_url(url, d_pnx, ydl_opts, f_historical, pk_db, play_option, cookie_exists)


def _handle_history_download_mode(f_historical, d_pnx, ydl_opts, pk_db, play_option, cookie_exists):
    """히스토리 URLs 다운로드 모드 처리"""
    from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
    from pk_internal_tools.pk_functions.get_list_deduplicated import get_list_deduplicated
    from pk_internal_tools.pk_functions.get_list_from_f import get_list_from_f
    from pk_internal_tools.pk_functions.get_list_removed_element_contain_prompt import get_list_removed_element_contain_prompt
    from pk_internal_tools.pk_functions.get_list_striped_element import get_list_striped_element
    import logging
    from pk_internal_tools.pk_functions.get_list_removed_element_empty import get_list_removed_empty

    # 히스토리에서 모든 URL 가져오기
    working_list = get_list_from_f(f=f_historical)
    working_list = get_list_removed_element_contain_prompt(working_list=working_list, prompt="#")
    working_list = get_list_deduplicated(working_list=working_list)
    working_list = get_list_removed_empty(working_list=working_list)
    working_list = get_list_striped_element(working_list=working_list)

    if len(working_list) == 0:
        logging.debug("히스토리에 다운로드할 URL이 없습니다.")
        return

    logging.debug(f"히스토리에서 {len(working_list)}개의 URL을 찾았습니다.")

    # 이미 다운로드된 URL들 처리
    _process_already_downloaded_urls(working_list, d_pnx, f_historical, pk_db, play_option)

    # 남은 URL들 다운로드
    remaining_urls = get_historical_list(f=f_historical)
    if remaining_urls:
        logging.debug(f"다운로드할 URL 개수: {len(remaining_urls)}")
        for i, url in enumerate(remaining_urls, 1):
            logging.debug(f"{i}: {url}")

        # 배치 다운로드
        _download_multiple_urls(remaining_urls, d_pnx, ydl_opts, f_historical, pk_db, play_option, cookie_exists)
    else:
        logging.debug("모든 URL이 이미 다운로드되었습니다.")


def _download_single_url(url, d_pnx, ydl_opts, f_historical, pk_db, play_option, cookie_exists):
    """단일 URL 다운로드"""
    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    from pk_internal_tools.pk_functions.get_youtube_clip_id import get_youtube_clip_id
    from pk_internal_tools.pk_functions.ensure_youtube_videos_downloaded_2025_05_02_0000 import ensure_youtube_videos_downloaded_2025_05_02_0000
    import logging
    from pk_internal_tools.pk_functions.normalize_youtube_url import normalize_youtube_url
    from pk_internal_tools.pk_functions.is_f_contained_signature import is_f_contained_signature
    import yt_dlp

    if is_os_windows():
        try:
            youtube_clip_id = get_youtube_clip_id(url=url)
            ensure_youtube_videos_downloaded_2025_05_02_0000(url_list=[youtube_clip_id], d_pnx=d_pnx, f_func_n_txt=f_historical)

            youtube_clip_id_stamp = f"[{youtube_clip_id}]"
            if is_f_contained_signature(signature=youtube_clip_id_stamp, d_pnx=d_pnx):
                logging.debug(f"{youtube_clip_id_stamp} 다운로드 완료: {url}")
                _handle_post_download_action(youtube_clip_id, url, d_pnx, f_historical, pk_db, play_option)
            else:
                logging.debug(f"{youtube_clip_id_stamp} 다운로드 실패: {url}")
        except Exception as e:
            logging.debug(f"Windows 다운로드 오류: {url}\n{str(e)}")
            _handle_download_error(url, str(e), cookie_exists)
    else:
        url = normalize_youtube_url(url)
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                youtube_clip_id = info.get('id', None)
                youtube_clip_id_stamp = f"[{youtube_clip_id}]"
                clip_title = info.get('title')

                logging.debug(f"다운로드 시작: {clip_title} ({youtube_clip_id})")

                # 이미 다운로드된 경우
                if is_f_contained_signature(signature=youtube_clip_id_stamp, d_pnx=d_pnx):
                    logging.debug(f"{youtube_clip_id_stamp} 이미 다운로드됨: {clip_title}")
                    _handle_post_download_action(youtube_clip_id, url, d_pnx, f_historical, pk_db, play_option)
                    return

                # 다운로드 실행
                ydl.download([url])

                # 다운로드 확인
                if is_f_contained_signature(signature=youtube_clip_id_stamp, d_pnx=d_pnx):
                    logging.debug(f"다운로드 완료: {clip_title}")
                    _handle_post_download_action(youtube_clip_id, url, d_pnx, f_historical, pk_db, play_option)
                else:
                    logging.debug(f"다운로드 실패: {clip_title}")

        except Exception as e:
            logging.debug(f"다운로드 오류: {url}\n{str(e)}")
            _handle_download_error(url, str(e), cookie_exists)


def _download_multiple_urls(urls, d_pnx, ydl_opts, f_historical, pk_db, play_option, cookie_exists):
    """여러 URL 배치 다운로드"""
    from pk_internal_tools.pk_functions.is_f_contained_signature import is_f_contained_signature

    from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
    from pk_internal_tools.pk_functions.normalize_youtube_url import normalize_youtube_url
    import logging
    import yt_dlp

    if is_os_windows():
        # Windows에서는 기존 방식 사용
        for url in urls:
            _download_single_url(url, d_pnx, ydl_opts, f_historical, pk_db, play_option, cookie_exists)
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
                        if is_f_contained_signature(signature=youtube_clip_id_stamp, d_pnx=d_pnx):
                            logging.debug(f"{youtube_clip_id_stamp} 이미 다운로드됨: {clip_title}")
                            _handle_post_download_action(youtube_clip_id, url, d_pnx, f_historical, pk_db, play_option)
                            continue

                        # 다운로드 실행
                        ydl.download([url])

                        # 다운로드 확인
                        if is_f_contained_signature(signature=youtube_clip_id_stamp, d_pnx=d_pnx):
                            logging.debug(f"다운로드 완료: {clip_title}")
                            _handle_post_download_action(youtube_clip_id, url, d_pnx, f_historical, pk_db, play_option)
                        else:
                            logging.debug(f"다운로드 실패: {clip_title}")

                    except Exception as e:
                        logging.debug(f"다운로드 오류: {url}\n{str(e)}")
                        _handle_download_error(url, str(e), cookie_exists)

        except Exception as e:
            logging.debug(f"배치 다운로드 오류: {str(e)}")


def _process_already_downloaded_urls(urls, d_pnx, f_historical, pk_db, play_option):
    """이미 다운로드된 URL들 처리"""
    from pk_internal_tools.pk_functions.is_f_contained_signature import is_f_contained_signature
    from pk_internal_tools.pk_functions.remove_lines_within_keyword_from_f import remove_lines_within_keyword_from_f
    from pk_internal_tools.pk_functions.get_historical_list import get_historical_list

    import logging
    from pk_internal_tools.pk_functions.get_youtube_clip_id import get_youtube_clip_id

    for url in urls:
        url = url.strip()
        if not url:
            continue

        youtube_clip_id = get_youtube_clip_id(url=url)
        youtube_clip_id_stamp = f"[{youtube_clip_id}]"

        if is_f_contained_signature(signature=youtube_clip_id_stamp, d_pnx=d_pnx):
            logging.debug(f"{youtube_clip_id_stamp} 이미 다운로드됨: {url}")
            _handle_post_download_action(youtube_clip_id, url, d_pnx, f_historical, pk_db, play_option)

            # 히스토리에서 제거
            remove_lines_within_keyword_from_f(f=f_historical, keyword=youtube_clip_id)

    # 히스토리 업데이트
    get_historical_list(f=f_historical)


def _handle_post_download_action(youtube_clip_id, url, d_pnx, f_historical, pk_db, play_option):
    """다운로드 후 동작 처리 (재생 또는 스킵)"""

    from pk_internal_tools.pk_functions.get_f_contained_signature import get_f_contained_signature
    from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    import logging

    if play_option == PkTexts.play:
        # 동영상 재생
        f_downloaded = get_f_contained_signature(signature=youtube_clip_id, d_pnx=d_pnx)
        if f_downloaded:
            logging.debug(f"동영상 재생: {f_downloaded}")
            ensure_pnx_opened_by_ext(pnx=f_downloaded)
    elif play_option == PkTexts.SKIP:
        logging.debug("동영상 재생을 건너뜁니다.")


def _handle_download_error(url, error_msg, cookie_exists):
    """다운로드 오류 처리"""
    import logging

    logging.debug(f"다운로드 오류 분석 중...")

    if "Sign in to confirm your age" in error_msg or "age-restricted" in error_msg:
        logging.warning("연령 제한 동영상입니다.")
        if not cookie_exists:
            logging.debug("해결 방법: Chrome에서 YouTube에 로그인 후 쿠키를 내보내주세요.")
            logging.debug("  확장 프로그램 'Get cookies.txt'를 사용하면 쉽게 쿠키를 내보낼 수 있습니다.")
        else:
            logging.debug("쿠키 파일이 있지만 인증에 실패했습니다. 쿠키를 새로 내보내주세요.")

    elif "This video is unavailable" in error_msg:
        logging.debug("동영상을 사용할 수 없습니다. (삭제되었거나 비공개)")

    elif "Video unavailable" in error_msg:
        logging.debug("동영상을 사용할 수 없습니다.")

    elif "copyright" in error_msg.lower():
        logging.debug("️ 저작권 문제로 다운로드할 수 없습니다.")

    else:
        logging.debug(f"알 수 없는 오류: {error_msg[:100]}...")

    logging.debug("다운로드를 건너뛰고 다음 URL로 진행합니다.")
