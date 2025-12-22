import logging
import traceback # Added for traceback
from datetime import datetime

from pk_internal_tools.pk_functions.ensure_random_value_from_options import ensure_random_value_from_options
from pk_internal_tools.pk_functions.ensure_sensitive_info_masked import ensure_sensitive_info_masked
from pk_internal_tools.pk_functions.ensure_wifi_pw_printed_fixed import get_wifi_password
from pk_internal_tools.pk_functions.get_wifi_profile_names import get_wifi_profile_names
from pk_internal_tools.pk_functions.get_weekday import get_weekday  # Added for DAY_OF_WEEK
from pk_internal_tools.pk_objects.pk_interesting_info import PkInterestingInfos
from pk_internal_tools.pk_objects.pk_modes import PkModesForGetPkInterestingInfo


def get_pk_interesting_info(
        flags: PkModesForGetPkInterestingInfo
) -> PkInterestingInfos:
    """
    현재 날짜, 시간 등 특정 정보를 선택적으로 수집하여 데이터 객체로 반환합니다.
    이 함수는 get_pk_interesting_infos (복수형)와는 별개로, 단일 정보 유형에 초점을 맞춥니다.

    Args:
        flags (PkModesForGetPkInterestingInfo): 포함할 정보 플래그.

    Returns:
        PkInterestingInfos: 수집된 정보가 담긴 데이터 객체.
    """
    # lazy import로 순환 import 문제 해결 및 성능 최적화
    try:
        # Corrected imports for LOCATION_WEATHER
        from pk_internal_tools.pk_functions.get_current_location_info import get_current_location_info
        from pk_internal_tools.pk_functions.get_current_weather_info import get_current_weather_info
        from pk_internal_tools.pk_functions.get_stock_infos import get_stock_infos
        from pk_internal_tools.pk_objects.pk_stock_tickers import STOCK_TICKERS_OF_INTERESTING # STOCK_TICKERS_OF_INTERESTING 임포트
        from pk_internal_tools.pk_functions.get_os_n import get_os_n
        from pk_internal_tools.pk_functions.get_connected_drives_info import get_connected_drives_info
        from pk_internal_tools.pk_functions.get_pk_screen_info import get_pk_screen_info
        from pk_internal_tools.pk_functions.get_project_info_from_pyproject import get_project_info_from_pyproject
        from pk_internal_tools.pk_functions.get_window_titles import get_window_titles
        from pk_internal_tools.pk_functions.get_tasklist_with_pid import get_tasklist_with_pid
        from pk_internal_tools.pk_functions.get_image_names_from_tasklist import get_image_names_from_tasklist
        from pk_internal_tools.pk_functions.get_top_processes_info import get_top_processes_info
        from pk_internal_tools.pk_functions.get_process_infos import get_process_infos  # Assuming this returns a list of process names/info
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose # Added for new rule
        from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed # Added for ENV VAR
        from pk_internal_tools.pk_functions.ensure_wifi_pw_printed import ensure_wifi_pw_printed_core # Added for WIFI
        # For WIFI, PYTHON_IMPORTS, AI_IDE_PROCESSES_INFO, placeholders or direct calls are used for now.
        # ensure_wifi_pw_printed_fixed is a printing function, not returning.
    except ImportError as e:
        logging.error(f"Lazy import failed in get_pk_interesting_info: {e}", exc_info=True)
        # Fallback or re-raise if critical
        raise

    data = PkInterestingInfos()

    if flags & PkModesForGetPkInterestingInfo.DATE:
        data.date = datetime.now().strftime("%Y년 %m월 %d일")
        logging.debug(f"날짜 정보 수집: {data.date}")

    if flags & PkModesForGetPkInterestingInfo.TIME:
        data.time = datetime.now().strftime("%H시 %M분")
        logging.debug(f"시간 정보 수집: {data.time}")

    if flags & PkModesForGetPkInterestingInfo.DAY_OF_WEEK:
        data.day_of_week = get_weekday()
        logging.debug(f"요일 정보 수집: {data.day_of_week}")

    if flags & PkModesForGetPkInterestingInfo.LOCATION_WEATHER:
        try:
            city, lat, lon, country_code = get_current_location_info()
            if city and lat and lon:
                weather_info = get_current_weather_info(city, lat, lon, country_code)
                data.location = city
                data.weather = weather_info
            else:
                logging.warning("위치 정보를 가져올 수 없어 날씨 정보를 건너뜀.")
                data.location = "알 수 없음"
                data.weather = "알 수 없음"
            logging.debug(f"위치 정보 수집: {data.location}, 날씨 정보 수집: {data.weather}")
        except Exception as e:
            ensure_debugged_verbose(traceback, e) # Apply new rule
            logging.error(f"위치/날씨 정보 수집 실패: {e}", exc_info=True)
            data.location = "수집 실패"
            data.weather = "수집 실패"

    if flags & PkModesForGetPkInterestingInfo.STOCK:
        try:
            data.stock_info = get_stock_infos(STOCK_TICKERS_OF_INTERESTING)
            logging.debug(f"주식 정보 수집: {data.stock_info}")
        except Exception as e:
            ensure_debugged_verbose(traceback, e) # Apply new rule
            logging.error(f"주식 정보 수집 실패: {e}", exc_info=True)
            data.stock_info = "수집 실패"

    if flags & PkModesForGetPkInterestingInfo.OS:
        try:
            data.os_info = get_os_n()
            logging.debug(f"OS 정보 수집: {data.os_info}")
        except Exception as e:
            ensure_debugged_verbose(traceback, e) # Apply new rule
            logging.error(f"OS 정보 수집 실패: {e}", exc_info=True)
            data.os_info = "수집 실패"

    if flags & PkModesForGetPkInterestingInfo.CONNECTED_DRIVES:
        try:
            data.connected_drives_info = get_connected_drives_info()
            logging.debug(f"연결된 드라이브 정보 수집: {data.connected_drives_info}")
        except Exception as e:
            ensure_debugged_verbose(traceback, e) # Apply new rule
            logging.error(f"연결된 드라이브 정보 수집 실패: {e}", exc_info=True)
            data.connected_drives_info = "수집 실패"

    if flags & PkModesForGetPkInterestingInfo.SCREEN:
        try:
            data.screen_info = get_pk_screen_info()
            logging.debug(f"화면 정보 수집: {data.screen_info}")
        except Exception as e:
            ensure_debugged_verbose(traceback, e) # Apply new rule
            logging.error(f"화면 정보 수집 실패: {e}", exc_info=True)
            data.screen_info = "수집 실패"

    if flags & PkModesForGetPkInterestingInfo.PROJECT:
        try:
            data.project_info = get_project_info_from_pyproject()
            logging.debug(f"프로젝트 정보 수집: {data.project_info}")
        except Exception as e:
            ensure_debugged_verbose(traceback, e) # Apply new rule
            logging.error(f"프로젝트 정보 수집 실패: {e}", exc_info=True)
            data.project_info = "수집 실패"

    if flags & PkModesForGetPkInterestingInfo.WINDOW_TITLES:
        try:
            data.window_titles = get_window_titles()
            logging.debug(f"창 제목 수집: {data.window_titles}")
        except Exception as e:
            ensure_debugged_verbose(traceback, e) # Apply new rule
            logging.error(f"창 제목 수집 실패: {e}", exc_info=True)
            data.window_titles = []

    if flags & PkModesForGetPkInterestingInfo.TASKLIST:
        try:
            data.tasklist_info = get_tasklist_with_pid()
            logging.debug(f"작업 목록 수집: {data.tasklist_info}")
        except Exception as e:
            ensure_debugged_verbose(traceback, e) # Apply new rule
            logging.error(f"작업 목록 수집 실패: {e}", exc_info=True)
            data.tasklist_info = []

    if flags & PkModesForGetPkInterestingInfo.IMAGE_NAMES_INFO:
        try:
            data.image_names_info = get_image_names_from_tasklist()
            logging.debug(f"이미지 이름 정보 수집: {data.image_names_info}")
        except Exception as e:
            ensure_debugged_verbose(traceback, e) # Apply new rule
            logging.error(f"이미지 이름 정보 수집 실패: {e}", exc_info=True)
            data.image_names_info = []

    top_processes_result = {}
    if flags & (PkModesForGetPkInterestingInfo.TOP_CPU_PROCESSES | PkModesForGetPkInterestingInfo.TOP_MEMORY_PROCESSES):
        try:
            top_processes_result = get_top_processes_info()
            logging.debug(f"상위 프로세스 정보 수집: {top_processes_result}")
        except Exception as e:
            ensure_debugged_verbose(traceback, e)
            logging.error(f"상위 프로세스 정보 수집 실패: {e}", exc_info=True)

    if flags & PkModesForGetPkInterestingInfo.TOP_CPU_PROCESSES:
        data.top_cpu_processes = top_processes_result.get('top_cpu', [])

    if flags & PkModesForGetPkInterestingInfo.TOP_MEMORY_PROCESSES:
        data.top_memory_processes = top_processes_result.get('top_memory', [])

    if flags & PkModesForGetPkInterestingInfo.PROCESSES:
        try:
            data.processes_info = get_process_infos()
            logging.debug(f"프로세스 정보 수집: {data.processes_info}")
        except Exception as e:
            ensure_debugged_verbose(traceback, e) # Apply new rule
            logging.error(f"프로세스 정보 수집 실패: {e}", exc_info=True)
            data.processes_info = []

    if flags & PkModesForGetPkInterestingInfo.WIFI:
        try:
            wifi_profile_names = get_wifi_profile_names()
            # wifi_profile_name = ensure_value_completed(key_name="wifi_profile_name", func_n=func_n, options=wifi_profile_names)
            wifi_profile_name = ensure_random_value_from_options(options=wifi_profile_names)
            wifi_password = get_wifi_password(profile_name=wifi_profile_name)
            data.wifi_profile_name = wifi_profile_name
            data.wifi_password = wifi_password
        except Exception as e:
            ensure_debugged_verbose(traceback, e)
            logging.error(f"WiFi 정보 수집 실패: {e}", exc_info=True)
            data.wifi_profile_name = "수집 실패"
            data.wifi_password = "수집 실패"

    if flags & PkModesForGetPkInterestingInfo.PYTHON_IMPORTS:
        try:
            # This requires scanning the project for Python files and parsing imports.
            # This is a complex task for a single function. Placeholder for now.
            data.python_imports_info = "Python_Imports_Placeholder"
            logging.debug(f"Python 임포트 정보 수집: {data.python_imports_info}")
        except Exception as e:
            ensure_debugged_verbose(traceback, e) # Apply new rule
            logging.error(f"Python 임포트 정보 수집 실패: {e}", exc_info=True)
            data.python_imports_info = "수집 실패"

    if flags & PkModesForGetPkInterestingInfo.AI_IDE_PROCESSES_INFO:
        try:
            # This requires filtering from the general process list.
            # Placeholder for now.
            data.ai_ide_processes_info = ["AI_IDE_Process_Placeholder"]
            logging.debug(f"AI IDE 프로세스 정보 수집: {data.ai_ide_processes_info}")
        except Exception as e:
            ensure_debugged_verbose(traceback, e) # Apply new rule
            logging.error(f"AI IDE 프로세스 정보 수집 실패: {e}", exc_info=True)
            data.ai_ide_processes_info = []

    if flags :
        try:
            from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
            data.lta = QC_MODE
            logging.debug(f"QC_MODE 정보 수집: {data.lta}")
        except Exception as e:
            ensure_debugged_verbose(traceback, e) # Apply new rule
            logging.error(f"QC_MODE 정보 수집 실패: {e}", exc_info=True)
            data.lta = None

    return data
