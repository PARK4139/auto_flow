def get_youtube_clip_id(url: str) -> str | None:
    """
    YouTube URL에서 클립 ID를 추출합니다.
    """
    import re
    import logging

    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    match = re.match(youtube_regex, url)
    if match:
        return match.group(6)
    else:
        logging.debug(f"YouTube 클립 ID를 추출할 수 없습니다: {url}")
        return None
