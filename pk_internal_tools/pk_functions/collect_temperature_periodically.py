"""
주기적으로 기온 정보를 수집하여 DB에 저장하는 함수.
별도 프로세스나 스케줄러에서 실행하도록 설계됨.
"""
import logging
from pathlib import Path
from typing import Optional

from pk_internal_tools.pk_functions.get_current_location_info import get_current_location_info
from pk_internal_tools.pk_functions.save_temperature_to_db import save_temperature_to_db


def collect_temperature_periodically() -> bool:
    """
    현재 위치의 기온을 API에서 가져와 DB에 저장합니다.
    주기적으로 실행되는 별도 프로세스에서 호출하도록 설계됨.
    
    Returns:
        bool: 성공 시 True, 실패 시 False.
    """
    try:
        # 현재 위치 정보 가져오기
        city, lat, lon, country_code = get_current_location_info()
        
        if not lat or not lon:
            logging.warning("위치 정보를 가져올 수 없어 기온을 수집할 수 없습니다.")
            return False
        
        # Open-Meteo API를 통해 온도 정보 가져오기
        import requests
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&timezone=auto"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if "current_weather" in data:
            current_weather = data["current_weather"]
            temperature = float(current_weather["temperature"])
            
            # DB에 저장
            success = save_temperature_to_db(
                temperature=temperature,
                latitude=lat,
                longitude=lon,
                city=city,
                country_code=country_code
            )
            
            if success:
                logging.info(f"기온 수집 및 저장 완료: {temperature}°C (위치: {city if city else f'{lat}, {lon}'})")
                return True
            else:
                logging.warning("기온 수집은 성공했으나 DB 저장에 실패했습니다.")
                return False
        else:
            logging.warning(f"Open-Meteo 온도 정보 파싱 실패: {data.get('reason', 'Unknown error')}")
            return False
            
    except requests.exceptions.RequestException as e:
        logging.error(f"기온 수집 중 네트워크 오류 발생: {e}")
        return False
    except (KeyError, ValueError, TypeError) as e:
        logging.error(f"기온 수집 중 파싱 오류 발생: {e}")
        return False
    except Exception as e:
        logging.error(f"기온 수집 중 예상치 못한 오류 발생: {e}")
        return False


