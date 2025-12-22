import requests
import logging

def get_weather_from_open_meteo(lat: float, lon: float) -> str:
    """
    Open-Meteo API를 통해 특정 위도/경도의 날씨 정보를 가져옵니다.
    Args:
        lat: 위도.
        lon: 경도.
    Returns:
        str: 날씨 정보 요약 또는 실패 시 빈 문자열.
    """
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&timezone=auto"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if "current_weather" in data:
            current_weather = data["current_weather"]
            temperature = current_weather["temperature"]
            windspeed = current_weather["windspeed"]
            weathercode = current_weather["weathercode"] # Weather code for description

            # Simple mapping for weathercode (can be expanded)
            weather_description = {
                0: "맑음", 1: "대체로 맑음", 2: "부분적으로 흐림", 3: "흐림",
                45: "안개", 48: "성애 안개",
                51: "이슬비", 53: "보통 이슬비", 55: "강한 이슬비",
                56: "약한 어는 이슬비", 57: "강한 어는 이슬비",
                61: "약한 비", 63: "보통 비", 65: "강한 비",
                66: "약한 어는 비", 67: "강한 어는 비",
                71: "약한 눈", 73: "보통 눈", 75: "강한 눈",
                77: "눈송이",
                80: "약한 소나기", 81: "보통 소나기", 82: "강한 소나기",
                85: "약한 눈 소나기", 86: "강한 눈 소나기",
                95: "뇌우", 96: "우박을 동반한 뇌우", 99: "강한 우박을 동반한 뇌우"
            }.get(weathercode, "알 수 없음")

            time_str = current_weather["time"]
            result = f"날씨: {weather_description}, 온도: {temperature}°C, 풍속: {windspeed}km/h (출처: Open-Meteo, 시간: {time_str})"
            logging.info(f"Open-Meteo를 통한 날씨 정보 조회 성공: {result}")
            return result
        else:
            logging.warning(f"Open-Meteo 날씨 정보 가져오기 실패: {data.get("reason", "Unknown error")}")
            return ""
    except Exception as e:
        logging.error(f"Open-Meteo 날씨 정보 조회 중 오류 발생: {e}")
        return ""