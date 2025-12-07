def normalize_youtube_url(url_or_id):
    """
    YouTube URL 또는 ID를 표준 형식('https://www.youtube.com/watch?v=VIDEO_ID')으로 변환합니다.
    - 단축 URL (youtu.be/...)
    - 일반 URL의 불필요한 파라미터 (&t=, &ab_channel= 등)
    - 11자리 비디오 ID 문자열
    모두 처리합니다.
    """
    import re
    import logging

    input_str = url_or_id.strip()
    logging.debug(f"Normalizing input: {input_str}")

    # 0. 채널, 재생목록 등 비디오가 아닌 URL은 그대로 반환
    if any(p in input_str for p in ['/c/', '/channel/', '/user/', '/@', 'playlist?list=']):
        logging.debug(f"Non-video URL (channel, playlist, etc.) detected, returning original: {input_str}")
        return input_str

    # n. 11자리 비디오 ID 형식인지 확인
    # YouTube 비디오 ID는 보통 11자리이며, 영문, 숫자, -, _ 문자를 사용합니다.
    if re.fullmatch(r'[a-zA-Z0-9_-]{11}', input_str):
        video_id = input_str
        normalized_url = f"https://www.youtube.com/watch?v={video_id}"
        logging.debug(f"Converted video ID to standard format: {normalized_url}")
        return normalized_url

    # n. youtu.be 형식의 단축 URL 변환
    if "youtu.be/" in input_str:
        video_id_match = re.search(r"youtu\.be/([a-zA-Z0-9_-]+)", input_str)
        if video_id_match:
            video_id = video_id_match.group(1)
            normalized_url = f"https://www.youtube.com/watch?v={video_id}"
            logging.debug(f"Converted youtu.be to standard format: {normalized_url}")
            return normalized_url

    # 3. 표준 watch?v= 형식에서 비디오 ID 추출 및 정규화
    video_id_match = re.search(r"v=([a-zA-Z0-9_-]+)", input_str)
    if video_id_match:
        video_id = video_id_match.group(1)
        normalized_url = f"https://www.youtube.com/watch?v={video_id}"
        logging.debug(f"Normalized URL to core format: {normalized_url}")
        return normalized_url

    # 4. 어떤 패턴에도 해당하지 않는 경우
    logging.warning(f"Could not normalize input, returning original: {input_str}")
    return input_str
