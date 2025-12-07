import logging

def get_pretty_html_string(html_content: str) -> str:
    """
    주어진 HTML/XML 문자열을 가독성 좋게 들여쓰기하여 반환합니다.
    BeautifulSoup 라이브러리가 필요합니다.

    Args:
        html_content: 원본 HTML 또는 XML 문자열.

    Returns:
        가독성 좋게 포맷된 HTML/XML 문자열.
        라이브러리가 없거나 오류 발생 시 원본 문자열을 반환합니다.
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        logging.warning("HTML을 예쁘게 출력하려면 'beautifulsoup4' 라이브러리가 필요합니다. "
                        "pip install beautifulsoup4")
        return html_content

    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.prettify()
    except Exception as e:
        logging.error(f"HTML 파싱 중 오류 발생: {e}")
        return html_content # Fallback to original content
