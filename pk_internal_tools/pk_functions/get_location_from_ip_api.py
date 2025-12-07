import requests
import logging

def get_location_from_ip_api():
    """
    IP 기반 Geolocation API를 통해 현재 위치 정보를 가져옵니다.
    Returns:
        tuple: (도시, 위도, 경도, 국가 코드) 또는 실패 시 ("", "", "", "").
    """
    logging.debug("get_location_from_ip_api 함수 시작.") # Added debug
    try:
        logging.debug("ip-api.com/json으로 요청 전송.") # Added debug
        response = requests.get("http://ip-api.com/json", timeout=5)
        response.raise_for_status()
        data = response.json()
        logging.debug(f"ip-api.com/json 응답 데이터: {data}") # Added debug

        if data["status"] == "success":
            city = data.get("city", "")
            lat = data.get("lat", "")
            lon = data.get("lon", "")
            logging.info(f"IP API를 통한 위치 정보 크롤링 성공: {city} (Lat: {lat}, Lon: {lon})")
            return city, lat, lon, data.get("countryCode", "")
        else:
            logging.info(f"IP API를 통한 위치 정보 가져오기 실패: {data.get("message", "Unknown error")}")
            return "", "", "", ""
    except Exception as e:
        logging.info(f"IP API를 통한 위치 정보 크롤링 중 오류 발생: {e}")
        return "", "", "", ""