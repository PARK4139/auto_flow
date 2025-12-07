def ensure_youtube_videos_downloaded_v_2025_10_08_1256(video_urls=None):
    try:
        import logging
        import traceback
        from urllib.parse import quote

        from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
        from pk_internal_tools.pk_functions.ensure_command_executed import ensure_command_executed
        from pk_internal_tools.pk_functions.ensure_iterable_log_as_vertical import ensure_iterable_log_as_vertical
        from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
        from pk_internal_tools.pk_functions.get_list_from_f import get_list_from_f
        from pk_internal_tools.pk_functions.get_list_removed_by_removing_runtine import get_list_removed_by_removing_runtine
        from pk_internal_tools.pk_functions.get_list_removed_element_contain_prompt import get_list_removed_element_contain_prompt
        from pk_internal_tools.pk_functions.get_list_via_user_input import get_list_via_user_input
        from pk_internal_tools.pk_functions.is_window_opened import is_window_opened
        from pk_internal_tools.pk_objects.pk_files import F_DOWNLOAD_YOUTUBE_VIDEOS_HISTORY

        func_n = get_caller_name()
        f_video_to_download = F_DOWNLOAD_YOUTUBE_VIDEOS_HISTORY
        via_f_txt = F_DOWNLOAD_YOUTUBE_VIDEOS_HISTORY
        ensure_pnx_made(pnx=f_video_to_download, mode="f")

        if not is_window_opened(window_title_seg=func_n):
            ensure_command_executed(cmd=rf"explorer {f_video_to_download}")

        if via_f_txt is None and video_urls is None:
            logging.debug(rf"{func_n}() 동작 조건 불충족")
            return

        if via_f_txt is True and video_urls is None:
            video_urls = get_list_from_f(f=f_video_to_download)
            video_urls = get_list_removed_element_contain_prompt(working_list=video_urls, prompt="#")

        elif via_f_txt is None and video_urls is None:
            video_urls = get_list_via_user_input(ment=rf"다운로드할 유튜브 리스트를 \n 단위로 입력하세요", func_n=func_n)

        elif video_urls is not None:
            video_urls = video_urls
        else:
            logging.debug(f''' ''')
            return

        video_urls = get_list_removed_by_removing_runtine(working_list=video_urls)
        ensure_iterable_log_as_vertical(item_iterable=video_urls, item_iterable_n="urls")
        logging.debug(rf'''len(urls)="{len(video_urls)}"''')
        if len(video_urls) == 0:
            return
        playlist_url_parameter = 'list='
        for url in video_urls:
            if playlist_url_parameter in url:
                encoded_url = quote(url, safe=':/?&=')
                from pytube import Playlist
                playlist = Playlist(encoded_url)
                logging.debug(rf'''playlist="{playlist}"  ''')
                logging.debug(rf'''playlist.title="{playlist.title}"  ''')
                logging.debug(rf'''len(playlist.video_urls)="{len(playlist.video_urls)}"  ''')
                for index, video in enumerate(playlist.videos, start=1):
                    logging.debug(rf'''video.watch_url="{video.watch_url}"  ''')
                    _ensure_youtube_videos_downloaded_core(urls=[video.watch_url])
            else:
                _ensure_youtube_videos_downloaded_core(urls=[url])
    except:
        ensure_debug_loged_verbose(traceback=traceback)


def _ensure_youtube_videos_downloaded_core(urls, output_dir=None, max_workers=3):
    from pk_internal_tools.pk_functions.download_single_youtube_video import download_single_youtube_video

    from asyncio import as_completed
    from concurrent.futures import ThreadPoolExecutor
    from pathlib import Path
    import logging
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    from pk_internal_tools.pk_functions.ensure_youtube_cookies_created import ensure_youtube_cookies_created
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    try:
        # YouTube 쿠키 설정
        try:
            ensure_youtube_cookies_created()
        except Exception as e:
            logging.debug(f"[{PkTexts.YOUTUBE_COOKIES_SETUP_FAILED_CONTINUE}] {e}")

        # PotPlayer 시작 (함수가 정의되지 않았으므로 주석 처리)
        # try:
        #     ensure_pot_player_enabled()
        # except Exception as e:
        #     logging.debug(f"[{PkTexts.POTPLAYER_START_FAILED_CONTINUE}] {e}")

        # URL 처리
        if isinstance(urls, str):
            urls = [urls]

        if not urls:
            logging.debug("URL 목록이 비어있습니다.")
            return []

        # 출력 디렉토리 설정
        if output_dir is None:
            from pk_internal_tools.pk_objects.pk_directories import D_PK_WORKING
            output_dir = D_PK_WORKING / f"downloaded_via_{func_n}"

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 병렬 다운로드 실행
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for url in urls:
                if url.strip() and not url.strip().startswith('#'):
                    future = executor.submit(download_single_youtube_video, url.strip(), output_dir)
                    futures.append(future)

            # 결과 수집
            results = []
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logging.debug(f"[{PkTexts.EXCEPTION_OCCURRED}] {e}")
                    results.append(None)

        return results

    except Exception as e:
        logging.debug(f"[{PkTexts.EXCEPTION_OCCURRED}] {e}")
        return []
