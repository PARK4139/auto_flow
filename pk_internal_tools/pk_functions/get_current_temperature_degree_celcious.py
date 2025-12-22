from typing import Optional


def get_current_temperature_degree_celcious(max_age_minutes=5) -> Optional[float]:
    import requests
    import logging

    from pk_internal_tools.pk_functions.get_current_location_info import get_current_location_info
    from pk_internal_tools.pk_functions.get_temperature_from_db import get_temperature_from_db
    from pk_internal_tools.pk_functions.save_temperature_to_db import save_temperature_to_db
    """
    현재 위치의 기온을 섭씨(°C)로 가져옵니다.
    
    DB에 최근 5분 이내의 데이터가 있으면 DB에서 조회하고,
    없으면 API를 호출하여 가져온 후 DB에 저장합니다.
    
    Returns:
        Optional[float]: 현재 기온 (섭씨), 실패 시 None.
    """
    # n. DB에서 최근 5분 이내 데이터 조회 시도
    db_result = get_temperature_from_db(max_age_minutes=max_age_minutes)
    if db_result is not None:
        temperature, collected_at = db_result
        logging.debug(f"DB에서 기온 조회 성공: {temperature}°C (수집시간: {collected_at})")
        return temperature

    # n. DB에 최근 데이터가 없으면 API 호출
    logging.debug("DB에 최근 데이터가 없어 API에서 기온을 조회합니다.")
    try:
        # 현재 위치 정보 가져오기
        city, lat, lon, country_code = get_current_location_info()

        if not lat or not lon:
            logging.warning("위치 정보를 가져올 수 없어 온도를 조회할 수 없습니다.")
            return None

        # Open-Meteo API를 통해 온도 정보 가져오기 (API 키 불필요)
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&timezone=auto"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if "current_weather" in data:
            current_weather = data["current_weather"]
            temperature = float(current_weather["temperature"])

            # DB에 저장 (비동기적으로 처리하지 않음 - 간단한 구현)
            save_temperature_to_db(
                temperature=temperature,
                latitude=lat,
                longitude=lon,
                city=city,
                country_code=country_code
            )

            logging.info(f"API에서 기온 조회 및 DB 저장 완료: {temperature}°C (위치: {city if city else f'{lat}, {lon}'})")
            return temperature
        else:
            logging.warning(f"Open-Meteo 온도 정보 파싱 실패: {data.get('reason', 'Unknown error')}")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"온도 정보 조회 중 네트워크 오류 발생: {e}")
        return None
    except (KeyError, ValueError, TypeError) as e:
        logging.error(f"온도 정보 파싱 중 오류 발생: {e}")
        return None
    except Exception as e:
        logging.error(f"온도 정보 조회 중 예상치 못한 오류 발생: {e}")
        return None
