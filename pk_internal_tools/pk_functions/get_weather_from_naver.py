import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime

def get_weather_from_naver(lat: float, lon: float) -> str:
    """
    네이버 날씨 페이지를 크롤링하여 특정 위도/경도의 날씨 정보를 가져옵니다.
    네이버는 위도/경도 직접 조회를 지원하지 않으므로, 현재는 일반적인 날씨 정보를 가져옵니다.
    향후 위도/경도를 기반으로 지역명을 역지오코딩하여 검색하는 기능 추가 필요.
    Args:
        lat: 위도 (현재 사용되지 않음).
        lon: 경도 (현재 사용되지 않음).
    Returns:
        str: 날씨 정보 요약 또는 실패 시 빈 문자열.
    """
    try:
        # 네이버 날씨 검색 페이지 URL (일반적인 현재 날씨)
        url = "https://search.naver.com/search.naver?query=%ED%98%84%EC%9E%AC%EB%82%A0%EC%94%A8"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 날씨 정보 추출
        # 네이버 날씨 페이지 구조는 변경될 수 있으므로, 선택자 변경 필요할 수 있음
        # 예시: 현재 온도, 날씨 상태, 체감 온도, 습도, 바람 등
        current_temp_elem = soup.select_one('#main_pack > div.sc.cs_weather._weather_service.api_cs_weather_area > div.weather_box > div.weather_area._main_info > div.weather_now > div > strong')
        weather_desc_elem = soup.select_one('#main_pack > div.sc.cs_weather._weather_service.api_cs_weather_area > div.weather_box > div.weather_area._main_info > div.weather_now > div > p')
        # wind_speed_elem = soup.select_one('#main_pack > div.sc.cs_weather._weather_service.api_cs_weather_area > div.weather_box > div.weather_area._main_info > div.weather_info > ul > li:nth-child(3) > span')
        # 네이버는 풍속을 직접적으로 보여주지 않거나, 위치에 따라 다를 수 있음. 여기서는 생략하거나 다른 요소 탐색 필요.

        current_temp = current_temp_elem.text.strip() if current_temp_elem else "N/A"
        weather_desc = weather_desc_elem.text.strip() if weather_desc_elem else "N/A"

        # 데이터 시간
        data_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        result = f"날씨: {weather_desc}, 온도: {current_temp} (출처: 네이버, 시간: {data_time})"
        logging.info(f"네이버를 통한 날씨 정보 조회 성공: {result}")
        return result

    except requests.exceptions.RequestException as req_err:
        logging.warning(f"네이버 날씨 정보 요청 중 오류 발생: {req_err}")
        return ""
    except Exception as e:
        logging.error(f"네이버 날씨 정보 크롤링 중 오류 발생: {e}")
        return ""