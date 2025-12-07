import json
import dataclasses
import logging
from datetime import datetime, date

def get_pretty_json_string(data: object) -> str:
    """
    주어진 파이썬 객체(dataclass 포함)를 가독성 좋은 JSON 문자열로 변환합니다.

    - ensure_ascii=False: 한글이 깨지지 않도록 보장합니다.
    - indent=4: 4칸 들여쓰기로 가독성을 높입니다.
    - datetime 객체는 ISO 형식 문자열로 변환합니다.

    Args:
        data: JSON으로 변환할 파이썬 객체.

    Returns:
        가독성 좋게 포맷된 JSON 문자열.
    """
    def json_serializer(obj):
        """JSON 직렬화를 위한 커스텀 함수"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
    
    if dataclasses.is_dataclass(data):
        data_to_dump = dataclasses.asdict(data)
    else:
        data_to_dump = data

    try:
        return json.dumps(data_to_dump, ensure_ascii=False, indent=4, default=json_serializer)
    except TypeError as e:
        # 객체에 직렬화할 수 없는 타입(예: set)이 포함된 경우 처리
        logging.error(f"JSON 직렬화 실패: {e}. 객체 타입: {type(data)}", exc_info=True)
        # Fallback으로 간단한 문자열 표현을 반환하거나, 예외를 다시 발생시킬 수 있습니다.
        return f'{{"error": "JSON serialization failed", "message": "{str(e)}"}}'
