import logging

from pk_internal_tools.pk_functions.get_location_from_ip_api import get_location_from_ip_api # Import the split function

def get_current_location_info():
    """
    IP 기반 Geolocation API를 통해 현재 위치 정보를 가져옵니다.
    Returns:
        tuple: (도시, 위도, 경도, 국가 코드) 또는 실패 시 ("", "", "", "").
    """
    logging.debug("get_current_location_info 함수 시작.") # Added debug
    city, lat, lon, country_code = get_location_from_ip_api()
    logging.debug(f"get_location_from_ip_api 결과: city={city}, lat={lat}, lon={lon}, country_code={country_code}") # Added debug
    if not city or not lat or not lon:
        logging.debug("위치를 확인할 수 없어 위치 정보를 가져올 수 없습니다.") # Changed to debug
        return "", "", "", ""
    return city, lat, lon, country_code