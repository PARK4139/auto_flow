import logging

from pk_internal_tools.pk_functions.ensure_env_var_completed_2025_11_24 import ensure_env_var_completed_2025_11_24
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.ensure_api_key_return import ensure_api_key_return
from pk_internal_tools.pk_functions.to_vilage_grid import to_vilage_grid # Import the split function
from pk_internal_tools.pk_functions.kma_get_ultra_now import kma_get_ultra_now # Import the split function

# Assuming KMA_SERVICE_KEY_ID is a common constant
KMA_SERVICE_KEY_ID = "KMA_SERVICE_KEY"

def get_weather_from_kma(lat: float, lon: float) -> str:
    """
    기상청(KMA) API를 통해 특정 위도/경도의 날씨 정보를 가져옵니다.
    Args:
        lat: 위도.
        lon: 경도.
    Returns:
        str: 날씨 정보 요약 또는 실패 시 빈 문자열.
    """
    func_n = get_caller_name()
    KMA_SERVICE_KEY_ID_ENV = ensure_env_var_completed_2025_11_24(key_name="KMA_SERVICE_KEY_ID",func_n=func_n)
    service_key = ensure_api_key_return(KMA_SERVICE_KEY_ID_ENV)
    if not service_key:
        logging.error(f"{KMA_SERVICE_KEY_ID_ENV} 서비스 키가 설정되지 않았습니다. 기상청 날씨 정보를 가져올 수 없습니다.")
        return ""

    try:
        x, y = to_vilage_grid(lat, lon)
        kma_data = kma_get_ultra_now(x, y, service_key)

        if kma_data and kma_data.get('response', {}).get('header', {}).get('resultCode') == '00':
            items = kma_data['response']['body']['items']['item']
            
            temperature = 'N/A'
            humidity = 'N/A'
            weather_condition = 'N/A'

            for item in items:
                if item['category'] == 'T1H': # 기온
                    temperature = item['obsrValue']
                elif item['category'] == 'REH': # 습도
                    humidity = item['obsrValue']
                elif item['category'] == 'SKY': # 하늘 상태 (1: 맑음, 3: 구름많음, 4: 흐림)
                    sky_code = item['obsrValue']
                    if sky_code == '1': weather_condition = '맑음'
                    elif sky_code == '3': weather_condition = '구름많음'
                    elif sky_code == '4': weather_condition = '흐림'
                elif item['category'] == 'PTY': # 강수 형태 (0: 없음, 1: 비, 2: 비/눈, 3: 눈, 5: 빗방울, 6: 빗방울눈날림, 7: 눈날림)
                    pty_code = item['obsrValue']
                    if pty_code != '0':
                        if pty_code == '1': weather_condition += '(비)'
                        elif pty_code == '2': weather_condition += '(비/눈)'
                        elif pty_code == '3': weather_condition += '(눈)'
                        elif pty_code == '5': weather_condition += '(빗방울)'
                        elif pty_code == '6': weather_condition += '(빗방울눈날림)'
                        elif pty_code == '7': weather_condition += '(눈날림)'

            result = f"날씨: {weather_condition}, 온도: {temperature}°C, 습도: {humidity}% (출처: 기상청)"
            logging.info(f"기상청을 통한 날씨 정보 조회 성공: {result}")
            return result
        else:
            logging.warning(f"기상청 날씨 정보 가져오기 실패: {kma_data.get('response', {}).get('header', {}).get('resultMsg', 'Unknown error')}")
            return ""
    except Exception as e:
        logging.error(f"기상청 날씨 정보 조회 중 오류 발생: {e}")
        return ""