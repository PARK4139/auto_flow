from datetime import datetime
import logging
import traceback

from pk_internal_tools.pk_objects.pk_interesting_info import PkInterestingInfos
from pk_internal_tools.pk_objects.pk_modes import PkModesForGetPkInterestingInfo
from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose


def _collect_pk_interesting_info_field(
    data: PkInterestingInfos,
    flags: PkModesForGetPkInterestingInfo,
    field_flag: PkModesForGetPkInterestingInfo,
    collector_func,
    error_message: str,
    default_value,
    field_name: str
):
    if flags & field_flag:
        try:
            collected_value = collector_func()
            setattr(data, field_name, collected_value)
            logging.debug(f"{field_name} 정보 수집: {getattr(data, field_name)}")
        except Exception as e:
            ensure_debugged_verbose(traceback, e)
            logging.error(f"{error_message}: {e}", exc_info=True)
            setattr(data, field_name, default_value)


def _collect_date_info(data: PkInterestingInfos, flags: PkModesForGetPkInterestingInfo):
    _collect_pk_interesting_info_field(
        data=data,
        flags=flags,
        field_flag=PkModesForGetPkInterestingInfo.DATE,
        collector_func=lambda: datetime.now().strftime("%Y년 %m월 %d일"),
        error_message="날짜 정보 수집 실패",
        default_value="수집 실패",
        field_name="date"
    )

def _collect_time_info(data: PkInterestingInfos, flags: PkModesForGetPkInterestingInfo):
    _collect_pk_interesting_info_field(
        data=data,
        flags=flags,
        field_flag=PkModesForGetPkInterestingInfo.TIME,
        collector_func=lambda: datetime.now().strftime("%H시 %M분"),
        error_message="시간 정보 수집 실패",
        default_value="수집 실패",
        field_name="time"
    )

def _collect_day_of_week_info(data: PkInterestingInfos, flags: PkModesForGetPkInterestingInfo):
    from pk_internal_tools.pk_functions.get_weekday import get_weekday
    _collect_pk_interesting_info_field(
        data=data,
        flags=flags,
        field_flag=PkModesForGetPkInterestingInfo.DAY_OF_WEEK,
        collector_func=get_weekday,
        error_message="요일 정보 수집 실패",
        default_value="수집 실패",
        field_name="day_of_week"
    )

def _collect_location_weather_info(data: PkInterestingInfos, flags: PkModesForGetPkInterestingInfo):
    if flags & PkModesForGetPkInterestingInfo.LOCATION_WEATHER:
        try:
            from pk_internal_tools.pk_functions.get_current_location_info import get_current_location_info
            from pk_internal_tools.pk_functions.get_current_weather_info import get_current_weather_info
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
            ensure_debugged_verbose(traceback, e)
            logging.error(f"위치/날씨 정보 수집 실패: {e}", exc_info=True)
            data.location = "수집 실패"
            data.weather = "수집 실패"

def _collect_stock_info(data: PkInterestingInfos, flags: PkModesForGetPkInterestingInfo):
    if flags & PkModesForGetPkInterestingInfo.STOCK:
        try:
            from pk_internal_tools.pk_functions.get_stock_infos import get_stock_infos
            from pk_internal_tools.pk_objects.pk_stock_tickers import STOCK_TICKERS_OF_INTERESTING
            data.stock_info = get_stock_infos(STOCK_TICKERS_OF_INTERESTING)
            logging.debug(f"주식 정보 수집: {data.stock_info}")
        except Exception as e:
            ensure_debugged_verbose(traceback, e)
            logging.error(f"주식 정보 수집 실패: {e}", exc_info=True)
            data.stock_info = []

def _collect_os_info(data: PkInterestingInfos, flags: PkModesForGetPkInterestingInfo):
    from pk_internal_tools.pk_functions.get_os_n import get_os_n
    _collect_pk_interesting_info_field(
        data=data,
        flags=flags,
        field_flag=PkModesForGetPkInterestingInfo.OS,
        collector_func=get_os_n,
        error_message="OS 정보 수집 실패",
        default_value="수집 실패",
        field_name="os_info"
    )

def _collect_connected_drives_info(data: PkInterestingInfos, flags: PkModesForGetPkInterestingInfo):
    from pk_internal_tools.pk_functions.get_connected_drives_info import get_connected_drives_info
    _collect_pk_interesting_info_field(
        data=data,
        flags=flags,
        field_flag=PkModesForGetPkInterestingInfo.CONNECTED_DRIVES,
        collector_func=get_connected_drives_info,
        error_message="연결된 드라이브 정보 수집 실패",
        default_value="수집 실패",
        field_name="connected_drives_info"
    )

def _collect_screen_info(data: PkInterestingInfos, flags: PkModesForGetPkInterestingInfo):
    from pk_internal_tools.pk_functions.get_pk_screen_info import get_pk_screen_info
    _collect_pk_interesting_info_field(
        data=data,
        flags=flags,
        field_flag=PkModesForGetPkInterestingInfo.SCREEN,
        collector_func=get_pk_screen_info,
        error_message="화면 정보 수집 실패",
        default_value="수집 실패",
        field_name="screen_info"
    )

def _collect_project_info(data: PkInterestingInfos, flags: PkModesForGetPkInterestingInfo):
    from pk_internal_tools.pk_functions.get_project_info_from_pyproject import get_project_info_from_pyproject
    _collect_pk_interesting_info_field(
        data=data,
        flags=flags,
        field_flag=PkModesForGetPkInterestingInfo.PROJECT,
        collector_func=get_project_info_from_pyproject,
        error_message="프로젝트 정보 수집 실패",
        default_value="수집 실패",
        field_name="project_info"
    )

def _collect_window_titles_info(data: PkInterestingInfos, flags: PkModesForGetPkInterestingInfo):
    from pk_internal_tools.pk_functions.get_window_titles import get_window_titles
    _collect_pk_interesting_info_field(
        data=data,
        flags=flags,
        field_flag=PkModesForGetPkInterestingInfo.WINDOW_TITLES,
        collector_func=get_window_titles,
        error_message="창 제목 수집 실패",
        default_value=[],
        field_name="window_titles"
    )

def _collect_tasklist_info(data: PkInterestingInfos, flags: PkModesForGetPkInterestingInfo):
    from pk_internal_tools.pk_functions.get_tasklist_with_pid import get_tasklist_with_pid
    _collect_pk_interesting_info_field(
        data=data,
        flags=flags,
        field_flag=PkModesForGetPkInterestingInfo.TASKLIST,
        collector_func=get_tasklist_with_pid,
        error_message="작업 목록 수집 실패",
        default_value=[],
        field_name="tasklist_info"
    )

def _collect_image_names_info(data: PkInterestingInfos, flags: PkModesForGetPkInterestingInfo):
    from pk_internal_tools.pk_functions.get_image_names_from_tasklist import get_image_names_from_tasklist
    _collect_pk_interesting_info_field(
        data=data,
        flags=flags,
        field_flag=PkModesForGetPkInterestingInfo.IMAGE_NAMES_INFO,
        collector_func=get_image_names_from_tasklist,
        error_message="이미지 이름 정보 수집 실패",
        default_value=[],
        field_name="image_names_info"
    )

def _collect_top_processes_info(data: PkInterestingInfos, flags: PkModesForGetPkInterestingInfo):
    if flags & (PkModesForGetPkInterestingInfo.TOP_CPU_PROCESSES | PkModesForGetPkInterestingInfo.TOP_MEMORY_PROCESSES):
        try:
            from pk_internal_tools.pk_functions.get_top_processes_info import get_top_processes_info
            top_processes_result = get_top_processes_info()
            logging.debug(f"상위 프로세스 정보 수집: {top_processes_result}")
            if flags & PkModesForGetPkInterestingInfo.TOP_CPU_PROCESSES:
                data.top_cpu_processes = top_processes_result.get('top_cpu', [])
            if flags & PkModesForGetPkInterestingInfo.TOP_MEMORY_PROCESSES:
                data.top_memory_processes = top_processes_result.get('top_memory', [])
        except Exception as e:
            ensure_debugged_verbose(traceback, e)
            logging.error(f"상위 프로세스 정보 수집 실패: {e}", exc_info=True)
            data.top_cpu_processes = []
            data.top_memory_processes = []

def _collect_processes_info(data: PkInterestingInfos, flags: PkModesForGetPkInterestingInfo):
    from pk_internal_tools.pk_functions.get_process_infos import get_process_infos
    _collect_pk_interesting_info_field(
        data=data,
        flags=flags,
        field_flag=PkModesForGetPkInterestingInfo.PROCESSES,
        collector_func=get_process_infos,
        error_message="프로세스 정보 수집 실패",
        default_value=[],
        field_name="processes_info"
    )

def _collect_wifi_info(data: PkInterestingInfos, flags: PkModesForGetPkInterestingInfo, func_n):
    if flags & PkModesForGetPkInterestingInfo.WIFI:
        try:
            from pk_internal_tools.pk_functions.get_wifi_profile_names import get_wifi_profile_names
            from pk_internal_tools.pk_functions.ensure_random_value_from_options import ensure_random_value_from_options
            from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
            from pk_internal_tools.pk_functions.ensure_wifi_pw_printed import ensure_wifi_pw_printed_core
            from pk_internal_tools.pk_functions.ensure_wifi_pw_printed_fixed import get_wifi_password

            wifi_profile_names = get_wifi_profile_names()
            wifi_profile_name = ensure_random_value_from_options(options=wifi_profile_names)
            
            # Get wifi_name from ensure_wifi_pw_printed_core (requires admin, but only name is needed here)
            # wifi_name, _ = ensure_wifi_pw_printed_core(skip_admin_check=True) # Skip admin check for name only
            data.wifi_name = wifi_profile_name # Use selected profile name as wifi_name

            # Get wifi_password from environment variable
            wifi_password = ensure_env_var_completed(key_name="WIFI_PW", func_n=func_n, mask_log=True)
            data.wifi_password = wifi_password

            logging.debug(f"WiFi 정보 수집: {data.wifi_name}, {data.wifi_password}")
        except Exception as e:
            ensure_debugged_verbose(traceback, e)
            logging.error(f"WiFi 정보 수집 실패: {e}", exc_info=True)
            data.wifi_name = "수집 실패"
            data.wifi_password = "수집 실패"

def _collect_python_imports_info(data: PkInterestingInfos, flags: PkModesForGetPkInterestingInfo):
    if flags & PkModesForGetPkInterestingInfo.PYTHON_IMPORTS:
        try:
            from pk_internal_tools.pk_functions.ensure_all_import_script_printed import ensure_all_import_script_printed
            data.python_imports_info = ensure_all_import_script_printed()
            logging.debug(f"Python 임포트 정보 수집: {data.python_imports_info}")
        except Exception as e:
            ensure_debugged_verbose(traceback, e)
            logging.error(f"Python 임포트 정보 수집 실패: {e}", exc_info=True)
            data.python_imports_info = "수집 실패"

def _collect_ai_ide_processes_info(data: PkInterestingInfos, flags: PkModesForGetPkInterestingInfo):
    if flags & PkModesForGetPkInterestingInfo.AI_IDE_PROCESSES_INFO:
        try:
            # This requires filtering from the general process list.
            # Placeholder for now.
            data.ai_ide_processes_info = ["AI_IDE_Process_Placeholder"]
            logging.debug(f"AI IDE 프로세스 정보 수집: {data.ai_ide_processes_info}")
        except Exception as e:
            ensure_debugged_verbose(traceback, e)
            logging.error(f"AI IDE 프로세스 정보 수집 실패: {e}", exc_info=True)
            data.ai_ide_processes_info = []