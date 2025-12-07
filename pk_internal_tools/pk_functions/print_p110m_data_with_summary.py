"""
P110M 데이터를 Pretty JSON과 요약 정보로 출력하는 함수들
"""

import sys
from typing import Dict, Any, Optional
from datetime import datetime, date
import json


def json_serializer(obj):
    """JSON 직렬화를 위한 커스텀 함수"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    obj_type = type(obj)
    raise TypeError("Type " + str(obj_type) + " not serializable")


def format_runtime_seconds(seconds: int) -> str:
    """
    초 단위 시간을 읽기 쉬운 형식으로 변환합니다.
    
    Args:
        seconds: 초 단위 시간
        
    Returns:
        포맷된 시간 문자열 (예: "1시간 30분 (90분)" 또는 "30분")
    """
    if seconds is None:
        return "N/A"
    
    runtime_min = seconds // 60
    runtime_hour = runtime_min // 60
    
    if runtime_hour > 0:
        return f"{runtime_hour}시간 {runtime_min % 60}분 ({seconds}초)"
    elif runtime_min > 0:
        return f"{runtime_min}분 ({seconds}초)"
    else:
        return f"{seconds}초"


def print_p110m_energy_data_with_summary(
    energy_dict: Dict[str, Any],
    title: str = "P110M 에너지 데이터",
    output_file=sys.stderr,
    json_output_file=Optional[sys.stdout]
) -> None:
    """
    P110M 에너지 데이터를 Pretty JSON과 요약 정보로 출력합니다.
    
    Args:
        energy_dict: 에너지 데이터 딕셔너리
        title: 출력 제목
        output_file: 출력할 파일 (기본값: sys.stderr)
        json_output_file: JSON 출력할 파일 (None이면 출력 안 함, 기본값: sys.stdout)
    """
    from pk_internal_tools.pk_functions.get_pretty_json_string import get_pretty_json_string
    
    print("", file=output_file)
    print("=" * 60, file=output_file)
    print(title, file=output_file)
    print("=" * 60, file=output_file)
    
    # Pretty JSON 출력
    print(get_pretty_json_string(energy_dict), file=output_file)
    print("", file=output_file)
    
    # 주요 정보 요약
    print("주요 정보:", file=output_file)
    print("-" * 60, file=output_file)
    
    if "current_power" in energy_dict:
        current_power_val = energy_dict.get("current_power")
        print(f"  현재 소비 전력: {current_power_val} W", file=output_file)
    
    if "today_energy" in energy_dict:
        today_energy_val = energy_dict.get("today_energy")
        print(f"  오늘 사용 에너지: {today_energy_val} Wh", file=output_file)
    
    if "today_runtime" in energy_dict:
        today_runtime_val = energy_dict.get("today_runtime")
        runtime_str = format_runtime_seconds(today_runtime_val)
        print(f"  오늘 가동 시간: {runtime_str}", file=output_file)
    
    if "month_energy" in energy_dict:
        month_energy_val = energy_dict.get("month_energy")
        print(f"  이번 달 사용 에너지: {month_energy_val} Wh", file=output_file)
    
    if "month_runtime" in energy_dict:
        month_runtime_val = energy_dict.get("month_runtime")
        runtime_str = format_runtime_seconds(month_runtime_val)
        print(f"  이번 달 가동 시간: {runtime_str}", file=output_file)
    
    if "local_time" in energy_dict:
        local_time_val = energy_dict.get("local_time")
        print(f"  조회 시간: {local_time_val}", file=output_file)
    
    print("-" * 60, file=output_file)
    print("=" * 60, file=output_file)
    
    # DB 저장을 위한 JSON 출력 (선택적)
    if json_output_file is not None:
        try:
            print("", file=json_output_file)
            print("===ENERGY_DATA_JSON_START===", file=json_output_file)
            energy_json_str = json.dumps(energy_dict, ensure_ascii=False, indent=4, default=json_serializer)
            print(energy_json_str, file=json_output_file)
            print("===ENERGY_DATA_JSON_END===", file=json_output_file)
        except Exception as json_err:
            print(f"⚠️ JSON 출력 실패: {json_err}", file=output_file)


def print_p110m_device_info_with_summary(
    device_info_dict: Dict[str, Any],
    title: str = "P110M 전체 정보 (JSON)",
    output_file=sys.stderr
) -> None:
    """
    P110M 장치 정보를 Pretty JSON과 요약 정보로 노란색으로 출력합니다.
    
    Args:
        device_info_dict: 장치 정보 딕셔너리
        title: 출력 제목
        output_file: 출력할 파일 (기본값: sys.stderr)
    """
    from pk_internal_tools.pk_functions.get_pretty_json_string import get_pretty_json_string
    from pk_internal_tools.pk_functions.get_text_yellow import get_text_yellow
    
    print("", file=output_file)
    print(get_text_yellow("=" * 60), file=output_file)
    print(get_text_yellow(title), file=output_file)
    print(get_text_yellow("=" * 60), file=output_file)
    
    # Pretty JSON 출력
    json_str = get_pretty_json_string(device_info_dict)
    print(get_text_yellow(json_str), file=output_file)
    print(get_text_yellow("=" * 60), file=output_file)
    
    # 주요 정보 요약
    print("", file=output_file)
    print(get_text_yellow("주요 정보 요약:"), file=output_file)
    print(get_text_yellow("-" * 60), file=output_file)
    
    if "device_on" in device_info_dict:
        device_on = device_info_dict.get("device_on")
        print(get_text_yellow(f"  전원 상태: {'ON' if device_on else 'OFF'}"), file=output_file)
    
    if "on_time" in device_info_dict:
        on_time = device_info_dict.get("on_time")
        runtime_str = format_runtime_seconds(on_time)
        print(get_text_yellow(f"  켜져 있던 시간: {runtime_str}"), file=output_file)
    
    if "device_id" in device_info_dict:
        device_id = device_info_dict.get("device_id")
        print(get_text_yellow(f"  장치 ID: {device_id}"), file=output_file)
    
    if "fw_ver" in device_info_dict:
        fw_ver = device_info_dict.get("fw_ver")
        print(get_text_yellow(f"  펌웨어 버전: {fw_ver}"), file=output_file)
    
    if "hw_ver" in device_info_dict:
        hw_ver = device_info_dict.get("hw_ver")
        print(get_text_yellow(f"  하드웨어 버전: {hw_ver}"), file=output_file)
    
    if "current_power" in device_info_dict:
        current_power = device_info_dict.get("current_power")
        print(get_text_yellow(f"  현재 소비 전력: {current_power} W"), file=output_file)
    
    if "today_energy" in device_info_dict:
        today_energy = device_info_dict.get("today_energy")
        print(get_text_yellow(f"  오늘 사용 에너지: {today_energy} Wh"), file=output_file)
    
    if "month_energy" in device_info_dict:
        month_energy = device_info_dict.get("month_energy")
        print(get_text_yellow(f"  이번 달 사용 에너지: {month_energy} Wh"), file=output_file)
    
    print(get_text_yellow("-" * 60), file=output_file)
    print(get_text_yellow("=" * 60), file=output_file)

