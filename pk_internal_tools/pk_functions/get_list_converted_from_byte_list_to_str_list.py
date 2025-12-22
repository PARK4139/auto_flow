import tqdm
import functools
from selenium.webdriver.chrome.options import Options
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
from pk_internal_tools.pk_objects.pk_directories  import D_PK_ROOT
from pk_internal_tools.pk_objects.pk_state_via_context import SpeedControlContext
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed
from pk_internal_tools.pk_functions.get_pnxs import get_pnxs


def get_list_converted_from_byte_list_to_str_list(item_byte_list, encoding=None):
    """
    기본적으로 utf-8로 디코딩을 시도하되,
    실패할 경우 cp949로 재시도하고,
    둘 다 실패하면 대체문자로 표시합니다.
    이미 문자열인 경우는 그대로 반환합니다.
    """

    encoding = encoding or PkEncoding.UTF8
    result = []
    for item in item_byte_list:
        # 이미 문자열인 경우 그대로 반환
        if isinstance(item, str):
            result.append(item)
            continue
            
        try:
            # n. 우선 utf-8 디코딩
            decoded = item.decode(encoding)
        except UnicodeDecodeError:
            try:
                # 2) 실패하면 cp949로 재시도
                decoded = item.decode('cp949')
            except UnicodeDecodeError:
                # 3) 그래도 안 되면 대체문자 처리
                decoded = item.decode('utf-8', errors='replace')
        result.append(decoded)
    return result
