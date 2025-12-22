import requests
import logging

from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.ensure_api_key_return import ensure_api_key_return

# Assuming OPENWEATHER_API_KEY_ID is a common constant
OPENWEATHER_API_KEY_ID = "OPENWEATHER_API"

def get_weather_from_openweathermap(lat: str, lon: str) -> str:
    """
    OpenWeatherMap API를 통해 특정 위도/경도의 날씨 정보를 가져옵니다.
    Args:
        lat: 위도.
        lon: 경도.
    Returns:
        str: 날씨 정보 요약 또는 실패 시 빈 문자열.
    """
    func_n = get_caller_name()
    OPENWEATHER_API_KEY_ID_ENV = ensure_env_var_completed(key_name="OPENWEATHER_API_KEY_ID",func_n=func_n)
    api_key = ensure_api_key_return(OPENWEATHER_API_KEY_ID_ENV)
    if not api_key:
        logging.error(f"{OPENWEATHER_API_KEY_ID_ENV} API 키가 설정되지 않았습니다. OpenWeatherMap 날씨 정보를 가져올 수 없습니다.")
        return ""

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=kr"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("cod") == 200:
            weather_main = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]

            result = f"날씨: {weather_main}, 온도: {temperature}°C (체감: {feels_like}°C), 습도: {humidity}%"
            logging.info(f"OpenWeatherMap을 통한 날씨 정보 조회 성공: {result}")
            return result
        else:
            logging.warning(f"OpenWeatherMap 날씨 정보 가져오기 실패: {data.get("message", "Unknown error")}")
            return ""
    except Exception as e:
        logging.error(f"OpenWeatherMap 날씨 정보 조회 중 오류 발생: {e}")
        return ""