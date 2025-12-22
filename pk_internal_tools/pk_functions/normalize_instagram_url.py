import re
import logging

def normalize_instagram_url(url_or_id):
    """
    Instagram URL 또는 shortcode를 표준 형식('https://www.instagram.com/p/SHORTCODE')으로 변환합니다.
    - /p/ URL
    - /reels/ URL
    - shortcode 자체
    모두 처리합니다.
    """
    input_str = url_or_id.strip().split('?')[0]  # 쿼리 파라미터 제거
    logging.debug(f"Normalizing Instagram input: {input_str}")

    # /p/ 또는 /reels/ 에서 shortcode 추출
    match = re.search(r"/(p|reels)/([a-zA-Z0-9_-]+)", input_str)
    if match:
        shortcode = match.group(2)
        normalized_url = f"https://www.instagram.com/p/{shortcode}"
        logging.debug(f"Normalized Instagram URL to: {normalized_url}")
        return normalized_url

    # 입력값 자체가 shortcode인 경우 (슬래시가 없는 경우)
    if "/" not in input_str:
        shortcode = input_str
        normalized_url = f"https://www.instagram.com/p/{shortcode}"
        logging.debug(f"Converted Instagram shortcode to URL: {normalized_url}")
        return normalized_url

    logging.warning(f"Could not normalize Instagram input, returning original: {url_or_id}")
    return url_or_id
