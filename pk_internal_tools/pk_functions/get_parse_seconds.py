from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured

@ensure_seconds_measured
def get_parse_seconds(time_str):
    """
        TODO: Write docstring for get_parse_seconds.
    """
    try:

        import re

        import logging

        """시간 문자열을 파싱하여 초 단위로 변환"""
        try:
            # 정규식으로 숫자와 단위 추출
            pattern = r'^(\d+)\s*(초|분|시간|시)$'
            match = re.match(pattern, time_str.strip())

            if not match:
                return None, None

            value = int(match.group(1))
            unit = match.group(2)

            # 단위별 초 계산
            if unit == "초":
                seconds = value
                unit_display = "초"
            elif unit == "분":
                seconds = value * 60
                unit_display = "분"
            elif unit in ["시간", "시"]:
                seconds = value * 3600
                unit_display = "시간"
            else:
                return None, None

            return seconds, unit_display

        except Exception as e:
            logging.debug(f"시간 파싱 오류: {e}")
            return None, None
    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
    finally:
        pass
