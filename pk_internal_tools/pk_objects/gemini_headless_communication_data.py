# -*- coding: utf-8 -*-
import json
import logging
from typing import Any, Dict, Optional

# pk_system 프로젝트의 로깅 규칙을 준수합니다.
# ensure_pk_system_log_initialized()는 래퍼 스크립트에서 호출되므로, 함수 내에서는 basicConfig를 호출하지 않습니다.
# pk_functions 디렉토리에 있으면 호출하지 않습니다.
# from pk_internal_tools.pk_functions.ensure_pk_system_log_initialized import ensure_pk_system_log_initialized
# ensure_pk_system_log_initialized(__file__)


class GeminiHeadlessCommunicationData:
    """
    gemini CLI의 headless 모드(-p) 호출 결과를 저장하고 관리하는 데이터 클래스.
    """

    def __init__(self, json_data: Dict[str, Any]):
        """
        JSON 데이터를 기반으로 객체를 초기화합니다.

        Args:
            json_data (Dict[str, Any]): gemini CLI가 반환한 JSON 응답을 파싱한 딕셔너리.
        """
        logging.debug(f"GeminiHeadlessCommunicationData 초기화 시작, 원시 데이터: {json_data}")

        self.raw_data: Dict[str, Any] = json_data
        self.response: Optional[str] = self.raw_data.get("response")
        self.error: Optional[str] = self.raw_data.get("error")
        self.is_result_usable: bool = self._check_if_usable()

        logging.debug(f"초기화된 response: {self.response}")
        logging.debug(f"초기화된 error: {self.error}")
        logging.debug(f"결과 사용 가능 여부 (is_result_usable): {self.is_result_usable}")
        logging.debug("GeminiHeadlessCommunicationData 초기화 완료")

    def _check_if_usable(self) -> bool:
        """
        결과 데이터가 사용 가능한지 확인합니다.
        'response' 키가 존재하고, 그 값이 비어있지 않으며, 'error' 키가 없는 경우에만 사용 가능한 것으로 간주합니다.

        Returns:
            bool: 데이터 사용 가능 여부.
        """
        is_usable = "response" in self.raw_data and bool(self.response) and "error" not in self.raw_data
        logging.debug(f"_check_if_usable: response 존재 여부: {'response' in self.raw_data}, "
                      f"response 내용 유무: {bool(self.response)}, "
                      f"error 존재 여부: {'error' in self.raw_data}")
        return is_usable

    def to_json(self, indent: int = 4) -> str:
        """
        객체 데이터를 JSON 문자열로 변환합니다.

        Args:
            indent (int): JSON 출력 시 사용할 들여쓰기 크기.

        Returns:
            str: 객체 데이터를 나타내는 JSON 형식의 문자열.
        """
        logging.debug("to_json 호출됨")
        return json.dumps(self.raw_data, ensure_ascii=False, indent=indent)

    def __repr__(self) -> str:
        return f"GeminiHeadlessCommunicationData(is_usable={self.is_result_usable}, response='{self.response[:50]}...')"

