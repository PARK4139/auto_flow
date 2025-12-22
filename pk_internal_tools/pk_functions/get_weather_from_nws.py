import requests
import logging

def get_weather_from_nws(lat: float, lon: float) -> str:
    """
    NWS (National Weather Service) API를 통해 미국 특정 위도/경도의 날씨 정보를 가져옵니다.
    Args:
        lat: 위도.
        lon: 경도.
    Returns:
        str: 날씨 정보 요약 또는 실패 시 빈 문자열.
    """
    try:
        # n. Gridpoint 정보 가져오기
        points_url = f"https://api.weather.gov/points/{lat},{lon}"
        headers = {'User-Agent': 'pk_weather_app (pk_system@example.com)'} # NWS requires a User-Agent
        response = requests.get(points_url, headers=headers, timeout=5)
        response.raise_for_status()
        points_data = response.json()

        forecast_url = points_data["properties"]["forecast"]
        
        # n. 예보 정보 가져오기
        forecast_response = requests.get(forecast_url, headers=headers, timeout=5)
        forecast_response.raise_for_status()
        forecast_data = forecast.json()

        if "properties" in forecast_data and "periods" in forecast_data["properties"]:
            # 현재 또는 다음 예보 기간 정보 가져오기
            current_period = forecast_data["properties"]["periods"][0]
            
            name = current_period.get("name", "현재")
            temperature = current_period.get("temperature", "N/A")
            temperature_unit = current_period.get("temperatureUnit", "F")
            short_forecast = current_period.get("shortForecast", "N/A")
            detailed_forecast = current_period.get("detailedForecast", "N/A")

            result = f"날씨: {short_forecast}, 온도: {temperature}°{temperature_unit} ({name}) (출처: NWS)"
            logging.info(f"NWS를 통한 날씨 정보 조회 성공: {result}")
            return result
        else:
            logging.warning(f"NWS 날씨 정보 파싱 실패: {lat}, {lon}")
            return ""
    except Exception as e:
        logging.error(f"NWS 날씨 정보 조회 중 오류 발생: {e}")
        return ""