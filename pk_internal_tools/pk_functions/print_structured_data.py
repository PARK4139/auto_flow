"""
구조화된 데이터 출력 모듈
JSON, 딕셔너리, 리스트 등의 구조화된 데이터를 일관된 스타일로 출력합니다.
"""

import sys
import json
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, date


def json_serializer(obj):
    """JSON 직렬화를 위한 커스텀 함수"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    obj_type = type(obj)
    raise TypeError("Type " + str(obj_type) + " not serializable")


def format_runtime_seconds(seconds: Optional[int]) -> str:
    """
    초 단위 시간을 읽기 쉬운 형식으로 변환합니다.
    
    Args:
        seconds: 초 단위 시간
        
    Returns:
        포맷된 시간 문자열 (예: "1시간 30분 (90초)" 또는 "30분 (1800초)")
    """
    if seconds is None or seconds == 0:
        return "0초"
    
    runtime_min = seconds // 60
    runtime_hour = runtime_min // 60
    
    if runtime_hour > 0:
        return f"{runtime_hour}시간 {runtime_min % 60}분 ({seconds}초)"
    elif runtime_min > 0:
        return f"{runtime_min}분 ({seconds}초)"
    else:
        return f"{seconds}초"


def print_section_header(title: str, width: int = 60, output_file=sys.stderr) -> None:
    """
    섹션 헤더를 출력합니다.
    
    Args:
        title: 섹션 제목
        width: 구분선 너비
        output_file: 출력할 파일
    """
    print("", file=output_file)
    print("=" * width, file=output_file)
    print(title, file=output_file)
    print("=" * width, file=output_file)


def print_section_footer(width: int = 60, output_file=sys.stderr) -> None:
    """
    섹션 푸터를 출력합니다.
    
    Args:
        width: 구분선 너비
        output_file: 출력할 파일
    """
    print("=" * width, file=output_file)


def print_subsection_header(title: str, width: int = 60, output_file=sys.stderr) -> None:
    """
    서브섹션 헤더를 출력합니다.
    
    Args:
        title: 서브섹션 제목
        width: 구분선 너비
        output_file: 출력할 파일
    """
    print("", file=output_file)
    print(title, file=output_file)
    print("-" * width, file=output_file)


def print_subsection_footer(width: int = 60, output_file=sys.stderr) -> None:
    """
    서브섹션 푸터를 출력합니다.
    
    Args:
        width: 구분선 너비
        output_file: 출력할 파일
    """
    print("-" * width, file=output_file)


def print_key_value(key: str, value: Any, indent: int = 2, output_file=sys.stderr) -> None:
    """
    키-값 쌍을 구조화된 형식으로 출력합니다.
    
    Args:
        key: 키 이름
        value: 값
        indent: 들여쓰기 칸 수
        output_file: 출력할 파일
    """
    indent_str = " " * indent
    print(f"{indent_str}{key}: {value}", file=output_file)


def print_json_data(
    data: Union[Dict[str, Any], List[Any]],
    title: str = "JSON 데이터",
    output_file=sys.stderr,
    indent: int = 2
) -> None:
    """
    JSON 데이터를 구조화된 형식으로 출력합니다.
    
    Args:
        data: 출력할 데이터 (딕셔너리 또는 리스트)
        title: 섹션 제목
        output_file: 출력할 파일
        indent: JSON 들여쓰기 칸 수
    """
    from pk_internal_tools.pk_functions.get_pretty_json_string import get_pretty_json_string
    
    print_section_header(title, output_file=output_file)
    print(get_pretty_json_string(data), file=output_file)
    print_section_footer(output_file=output_file)


def print_summary_info(
    data: Dict[str, Any],
    title: str = "주요 정보 요약",
    output_file=sys.stderr,
    field_formatters: Optional[Dict[str, callable]] = None
) -> None:
    """
    주요 정보를 구조화된 형식으로 요약 출력합니다.
    
    Args:
        data: 출력할 데이터 딕셔너리
        title: 섹션 제목
        output_file: 출력할 파일
        field_formatters: 필드별 포맷터 함수 딕셔너리 (예: {"on_time": format_runtime_seconds})
    """
    print_subsection_header(title, output_file=output_file)
    
    # 기본 포맷터
    default_formatters = {
        "on_time": format_runtime_seconds,
        "today_runtime": format_runtime_seconds,
        "month_runtime": format_runtime_seconds,
        "device_on": lambda x: "ON" if x else "OFF",
    }
    
    # 사용자 제공 포맷터와 병합
    if field_formatters:
        default_formatters.update(field_formatters)
    
    formatters = default_formatters
    
    # 필드별 출력
    field_labels = {
        "device_on": "전원 상태",
        "on_time": "켜져 있던 시간",
        "current_power": "현재 소비 전력",
        "today_energy": "오늘 사용 에너지",
        "month_energy": "이번 달 사용 에너지",
        "today_runtime": "오늘 가동 시간",
        "month_runtime": "이번 달 가동 시간",
        "local_time": "조회 시간",
        "device_id": "장치 ID",
        "device_name": "장치 이름",
        "device_model": "장치 모델",
        "model": "장치 모델",
        "fw_ver": "펌웨어 버전",
        "hw_ver": "하드웨어 버전",
        "ip": "IP 주소",
        "mac": "MAC 주소",
        "rssi": "신호 강도",
        "signal_level": "신호 레벨",
    }
    
    # 출력할 필드 순서 정의
    priority_fields = [
        "device_on", "on_time", "current_power", "today_energy", "month_energy",
        "today_runtime", "month_runtime", "local_time", "device_id", "device_name",
        "device_model", "model", "fw_ver", "hw_ver", "ip", "mac", "rssi", "signal_level"
    ]
    
    # 우선순위 필드 먼저 출력
    for field in priority_fields:
        if field in data:
            value = data[field]
            label = field_labels.get(field, field)
            
            # 포맷터 적용
            if field in formatters:
                try:
                    formatted_value = formatters[field](value)
                    print_key_value(label, formatted_value, output_file=output_file)
                except Exception:
                    # 포맷터 실패 시 원본 값 출력
                    print_key_value(label, value, output_file=output_file)
            else:
                # 단위 추가
                if field == "current_power":
                    print_key_value(label, f"{value} W", output_file=output_file)
                elif field in ["today_energy", "month_energy"]:
                    print_key_value(label, f"{value} Wh", output_file=output_file)
                else:
                    print_key_value(label, value, output_file=output_file)
    
    # 나머지 필드 출력
    for key, value in data.items():
        if key not in priority_fields:
            label = field_labels.get(key, key)
            if key in formatters:
                try:
                    formatted_value = formatters[key](value)
                    print_key_value(label, formatted_value, output_file=output_file)
                except Exception:
                    print_key_value(label, value, output_file=output_file)
            else:
                print_key_value(label, value, output_file=output_file)
    
    print_subsection_footer(output_file=output_file)


def print_structured_data(
    data: Union[Dict[str, Any], List[Any]],
    title: str = "데이터",
    summary_title: str = "주요 정보 요약",
    output_file=sys.stderr,
    show_json: bool = True,
    show_summary: bool = True,
    field_formatters: Optional[Dict[str, callable]] = None
) -> None:
    """
    구조화된 데이터를 JSON과 요약 정보로 출력합니다.
    
    Args:
        data: 출력할 데이터
        title: JSON 섹션 제목
        summary_title: 요약 섹션 제목
        output_file: 출력할 파일
        show_json: JSON 출력 여부
        show_summary: 요약 정보 출력 여부
        field_formatters: 필드별 포맷터 함수 딕셔너리
    """
    if isinstance(data, dict):
        if show_json:
            print_json_data(data, title=title, output_file=output_file)
        
        if show_summary:
            print_summary_info(data, title=summary_title, output_file=output_file, field_formatters=field_formatters)
    elif isinstance(data, list):
        if show_json:
            print_json_data(data, title=title, output_file=output_file)
        # 리스트는 요약 정보 출력 안 함
    else:
        # 기타 타입은 JSON으로 변환 시도
        try:
            data_dict = dict(data) if hasattr(data, '__dict__') else {"value": data}
            if show_json:
                print_json_data(data_dict, title=title, output_file=output_file)
            if show_summary and isinstance(data_dict, dict):
                print_summary_info(data_dict, title=summary_title, output_file=output_file, field_formatters=field_formatters)
        except Exception:
            print(f"⚠️ 데이터 출력 실패: {type(data)}", file=output_file)


def print_json_for_db(
    data: Dict[str, Any],
    start_marker: str = "===ENERGY_DATA_JSON_START===",
    end_marker: str = "===ENERGY_DATA_JSON_END===",
    output_file=sys.stdout
) -> None:
    """
    DB 저장을 위한 JSON을 마커와 함께 출력합니다.
    
    Args:
        data: 출력할 데이터
        start_marker: 시작 마커
        end_marker: 종료 마커
        output_file: 출력할 파일 (기본값: sys.stdout)
    """
    try:
        print("", file=output_file)
        print(start_marker, file=output_file)
        json_str = json.dumps(data, ensure_ascii=False, indent=2, default=json_serializer)
        print(json_str, file=output_file)
        print(end_marker, file=output_file)
    except Exception as json_err:
        print(f"⚠️ JSON 출력 실패: {json_err}", file=sys.stderr)

