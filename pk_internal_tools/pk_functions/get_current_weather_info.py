import logging
from typing import List

from pk_internal_tools.pk_functions.get_weather_from_naver import get_weather_from_naver
from pk_internal_tools.pk_functions.get_weather_from_openweathermap import get_weather_from_openweathermap
from pk_internal_tools.pk_functions.get_weather_from_kma import get_weather_from_kma
from pk_internal_tools.pk_functions.get_weather_from_nws import get_weather_from_nws
from pk_internal_tools.pk_functions.get_weather_from_open_meteo import get_weather_from_open_meteo

def get_current_weather_info(city: str, lat: float, lon: float, country_code: str) -> List[str]:
    """
    주어진 도시, 위도/경도, 국가 코드에 대한 날씨 정보를 여러 소스에서 가져와 통합합니다.
    Args:
        city: 도시 이름.
        lat: 위도.
        lon: 경도.
        country_code: 국가 코드 (ISO 3166-1 alpha-2).
    Returns:
        str: 통합된 날씨 정보 요약 또는 실패 시 "날씨 정보 없음".
    """
    all_weather_info = []

    # n. 네이버 웹 크롤링 시도 (API 키 불필요)
    naver_weather = get_weather_from_naver(lat, lon) # lat, lon을 넘기도록 수정
    if naver_weather:
        all_weather_info.append(naver_weather)
        logging.info("네이버를 통한 날씨 정보 조회 성공.")
    else:
        logging.info("네이버 날씨 정보 가져오기 실패.")

    # n. Open-Meteo API 시도 (API 키 불필요)
    open_meteo_weather = get_weather_from_open_meteo(lat, lon)
    if open_meteo_weather:
        all_weather_info.append(open_meteo_weather)
        logging.info("Open-Meteo를 통한 날씨 정보 조회 성공.")
    else:
        logging.info("Open-Meteo 날씨 정보 가져오기 실패.")

    # 3. 국가별 공개 API 시도 (API 키 불필요)
    if country_code == 'US':
        nws_weather = get_weather_from_nws(lat, lon)
        if nws_weather:
            all_weather_info.append(nws_weather)
            logging.info("NWS를 통한 날씨 정보 조회 성공.")
        else:
            logging.info("NWS 날씨 정보 가져오기 실패.")

    # 4. 국가별 API 시도 (API 키 필요) - KMA 기능은 추후 구현 예정
    # if country_code == 'KR':
    #     kma_weather = get_weather_from_kma(lat, lon)
    #     if kma_weather:
    #         all_weather_info.append(kma_weather)
    #         logging.info("기상청을 통한 날씨 정보 조회 성공.")
    #     else:
    #         logging.info("기상청 날씨 정보 가져오기 실패.")

    # 5. OpenWeatherMap API 시도 (API 키 필요, 최종 폴백) - 추후 구현 예정
    # openweathermap_weather = get_weather_from_openweathermap(str(lat), str(lon))
    # if openweathermap_weather:
    #     all_weather_info.append(openweathermap_weather)
    #     logging.info("OpenWeatherMap을 통한 날씨 정보 조회 성공.")
    # else:
    #     logging.info("OpenWeatherMap 날씨 정보 가져오기 실패.")

    if all_weather_info:
        return all_weather_info
    else:
        logging.error("모든 날씨 정보 소스에서 날씨 정보를 가져올 수 없습니다.")
        return []