def get_video_title_with_ytdlp(clip_id):
    from pk_internal_tools.pk_functions.normalize_youtube_url import normalize_youtube_url
    import logging
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE

    from yt_dlp import YoutubeDL

    # URL 정리
    url = normalize_youtube_url(f"https://www.youtube.com/watch?v={clip_id}")

    ydl_opts = {
        'quiet': True,
        'skip_download': True,  # 다운로드는 건너뜀
        'force_generic_extractor': False,  # 유튜브 전용 처리
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # YouTube 영상 ID 추출
            clip_id = info.get('id', None)
            title = info.get('title', None)
            if title is None:
                logging.debug(f"Could not retrieve title for {clip_id}. Using default title.")
                if clip_id:
                    logging.debug(f"Could not retrieve clip_id for URL: {url}.")
                    return rf"Unknown_Title({clip_id})"
                return "Unknown_Title(unknown_clip_id)"
            return title

    except:
        DESCRIPTION = f"yt_dlp를 사용하여 제목을 가져오는 데 실패했습니다"  # 제목에 이모지나 특수문자를 포함한 경우 실패할 수 있음
        logging.debug(f"{DESCRIPTION}  ")
        return "Unknown_Title"
