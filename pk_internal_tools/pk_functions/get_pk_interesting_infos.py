from pk_internal_tools.pk_functions.ensure_random_value_from_options import ensure_random_value_from_options
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.get_wifi_profile_names import get_wifi_profile_names
from pk_internal_tools.pk_objects.pk_interesting_info import PkInterestingInfos, StockInfoItem
from pk_internal_tools.pk_objects.pk_modes import PkModesForGetPkInterestingInfo  # Import PkModesForGetPkInterestingInfo
from typing import Union # Add Union for type hinting
from rich.console import Console
from rich.table import Table

import logging # Re-import logging if not already done by ensure_pk_wrapper_starting_routine_done
import traceback


def get_pk_interesting_infos(
        flags: Union[PkModesForGetPkInterestingInfo, str] = PkModesForGetPkInterestingInfo.ALL
) -> PkInterestingInfos:
    # Convert string flags to Enum if necessary
    if isinstance(flags, str):
        flags = PkModesForGetPkInterestingInfo[flags.upper()]
    """
    현재 날짜, 시간, 요일, 날씨, 주식 등 다양한 정보를 선택적으로 수집하여 데이터 객체로 반환하고,
    주식 정보는 rich 라이브러리를 사용하여 테이블 형태로 콘솔에 출력합니다.

    Args:
        flags (PkModesForGetPkInterestingInfo): 포함할 정보 플래그.

    Returns:
        PkInterestingInfos: 수집된 정보가 담긴 데이터 객체.
    """
    from datetime import datetime

    from pk_internal_tools.pk_functions.ensure_wifi_pw_printed_fixed import get_wifi_password
    from pk_internal_tools.pk_functions.ensure_all_import_script_printed import ensure_all_import_script_printed
    from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose  # Added for new rule
    from pk_internal_tools.pk_functions.get_connected_drives_info import get_connected_drives_info
    from pk_internal_tools.pk_functions.get_current_location_info import get_current_location_info
    from pk_internal_tools.pk_functions.get_current_weather_info import get_current_weather_info
    from pk_internal_tools.pk_functions.get_image_names_from_tasklist import get_image_names_from_tasklist
    from pk_internal_tools.pk_functions.get_os_n import get_os_n
    from pk_internal_tools.pk_functions.get_pk_screen_info import get_pk_screen_info
    from pk_internal_tools.pk_functions.get_process_infos import get_process_infos
    from pk_internal_tools.pk_functions.get_project_info_from_pyproject import get_project_info_from_pyproject
    from pk_internal_tools.pk_functions.get_stock_infos import get_stock_infos
    from pk_internal_tools.pk_functions.get_tasklist_with_pid import get_tasklist_with_pid
    from pk_internal_tools.pk_functions.get_top_processes_info import get_top_processes_info
    from pk_internal_tools.pk_functions.get_weekday import get_weekday
    from pk_internal_tools.pk_functions.get_window_titles import get_window_titles
    from pk_internal_tools.pk_objects.pk_interesting_info import PkInterestingInfos
    from pk_internal_tools.pk_objects.pk_stock_tickers import STOCK_TICKERS_OF_INTERESTING

    try:
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
                    # get_current_weather_info는 이제 날씨 정보 문자열의 '리스트'를 반환합니다.
                    weather_list = get_current_weather_info(city, lat, lon, country_code)
                    data.location = city
                    data.weather_infos = weather_list
                else:
                    logging.warning("위치 정보를 가져올 수 없어 날씨 정보를 건너뜀.")
                    data.location = "알 수 없음"
                    data.weather_infos = []
                logging.debug(f"위치 정보 수집: {data.location}, 날씨 정보 수집: {data.weather_infos}")
            except Exception as e:
                ensure_debugged_verbose(traceback, e)  # Apply new rule
                logging.error(f"위치/날씨 정보 수집 중 오류: {e}", exc_info=True)
                data.location = "오류"
                data.weather_infos = []

        if flags & PkModesForGetPkInterestingInfo.STOCK:
            try:
                data.stock_info = get_stock_infos(STOCK_TICKERS_OF_INTERESTING)
                if data.stock_info:
                    console = Console()
                    table = Table(
                        title="주식 정보",
                        show_header=True,
                        header_style="bold magenta"
                    )
                    table.add_column("이름", style="cyan", no_wrap=True)
                    table.add_column("코드", style="green")
                    table.add_column("가격", style="yellow", justify="right")
                    table.add_column("출처", style="blue")
                    table.add_column("일시", style="white")
                    table.add_column("비고", style="red") # Reason or comparison

                    for item in data.stock_info:
                        if isinstance(item, StockInfoItem):
                            table.add_row(
                                item.name or "N/A",
                                item.code or "N/A",
                                item.price or "N/A",
                                item.source or "N/A",
                                item.source_date or "N/A",
                                item.reason or item.comparison_score or "N/A"
                            )
                        elif isinstance(item, dict): # Fallback for dictionary output
                            table.add_row(
                                item.get('name', 'N/A'),
                                item.get('code', 'N/A'),
                                item.get('price', 'N/A'),
                                item.get('source', 'N/A'),
                                item.get('source_date', 'N/A'),
                                item.get('reason', item.get('comparison_score', 'N/A'))
                            )
                    console.print(table)
                else:
                    logging.info("수집된 주식 정보가 없습니다.")
                logging.debug(f"주식 정보 수집: {data.stock_info}")
            except Exception as e:
                ensure_debugged_verbose(traceback, e)
                logging.error(f"주식 정보 수집 실패: {e}", exc_info=True)
                data.stock_info = []

        if flags & PkModesForGetPkInterestingInfo.CONNECTED_DRIVES:
            try:
                data.connected_drives_info = get_connected_drives_info()
                logging.debug(f"연결된 드라이브 정보 수집: {data.connected_drives_info}")
            except Exception as e:
                ensure_debugged_verbose(traceback, e)
                logging.error(f"연결된 드라이브 정보 수집 실패: {e}", exc_info=True)
                data.connected_drives_info = "수집 실패"

        if flags & PkModesForGetPkInterestingInfo.SCREEN:
            try:
                data.screen_info = get_pk_screen_info()
                logging.debug(f"화면 정보 수집: {data.screen_info}")
            except Exception as e:
                ensure_debugged_verbose(traceback, e)
                logging.error(f"화면 정보 수집 실패: {e}", exc_info=True)
                data.screen_info = "수집 실패"

        if flags & PkModesForGetPkInterestingInfo.PROJECT:
            try:
                data.project_info = get_project_info_from_pyproject()
                logging.debug(f"프로젝트 정보 수집: {data.project_info}")
            except Exception as e:
                ensure_debugged_verbose(traceback, e)
                logging.error(f"프로젝트 정보 수집 실패: {e}", exc_info=True)
                data.project_info = "수집 실패"

        if flags & PkModesForGetPkInterestingInfo.OS:
            try:
                data.os_info = get_os_n()
                logging.debug(f"OS 정보 수집: {data.os_info}")
            except Exception as e:
                ensure_debugged_verbose(traceback, e)
                logging.error(f"OS 정보 수집 실패: {e}", exc_info=True)
                data.os_info = "수집 실패"

        if flags & PkModesForGetPkInterestingInfo.WINDOW_TITLES:
            try:
                data.window_titles = get_window_titles()
                logging.debug(f"창 제목 수집: {data.window_titles}")
            except Exception as e:
                ensure_debugged_verbose(traceback, e)
                logging.error(f"창 제목 수집 실패: {e}", exc_info=True)
                data.window_titles = []

        if flags & PkModesForGetPkInterestingInfo.PROCESSES:
            try:
                data.processes_info = get_process_infos()
                logging.debug(f"프로세스 정보 수집: {data.processes_info}")
            except Exception as e:
                ensure_debugged_verbose(traceback, e)
                logging.error(f"프로세스 정보 수집 실패: {e}", exc_info=True)
                data.processes_info = []

        if flags & PkModesForGetPkInterestingInfo.TASKLIST:
            try:
                data.tasklist_info = get_tasklist_with_pid()
                logging.debug(f"작업 목록 수집: {data.tasklist_info}")
            except Exception as e:
                ensure_debugged_verbose(traceback, e)
                logging.error(f"작업 목록 수집 실패: {e}", exc_info=True)
                data.tasklist_info = []

        if flags & PkModesForGetPkInterestingInfo.IMAGE_NAMES_INFO:
            try:
                data.image_names_info = get_image_names_from_tasklist()
                logging.debug(f"이미지 이름 정보 수집: {data.image_names_info}")
            except Exception as e:
                ensure_debugged_verbose(traceback, e)
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
                data.top_cpu_processes = []
                data.top_memory_processes = []

        if flags & PkModesForGetPkInterestingInfo.TOP_CPU_PROCESSES:
            data.top_cpu_processes = top_processes_result.get('top_cpu', [])

        if flags & PkModesForGetPkInterestingInfo.TOP_MEMORY_PROCESSES:
            data.top_memory_processes = top_processes_result.get('top_memory', [])

        if flags & PkModesForGetPkInterestingInfo.WIFI:
            func_n = get_caller_name()
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
                data.python_imports_info = ensure_all_import_script_printed()
            except Exception as e:
                ensure_debugged_verbose(traceback, e)
                logging.error(f"Python 임포트 정보 수집 실패: {e}", exc_info=True)
                data.python_imports_info = "수집 실패"

        if flags & PkModesForGetPkInterestingInfo.AI_IDE_PROCESSES_INFO:
            try:
                # This requires filtering from the general process list.
                # Placeholder for now.
                data.ai_ide_processes_info = ["AI_IDE_Process_Placeholder"]
            except Exception as e:
                ensure_debugged_verbose(traceback, e)
                logging.error(f"AI IDE 프로세스 정보 수집 실패: {e}", exc_info=True)
                data.ai_ide_processes_info = []

        if flags :
            try:
                from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
                data.lta = QC_MODE
            except Exception as e:
                ensure_debugged_verbose(traceback, e)
                logging.error(f"QC_MODE 정보 수집 실패: {e}", exc_info=True)
                data.lta = None

        return data
    except Exception as e:
        ensure_debugged_verbose(traceback, e)
        logging.error(f"get_pk_interesting_infos 함수 실행 중 최상위 오류 발생: {e}", exc_info=True)
        return PkInterestingInfos() # Return empty data on top-level error