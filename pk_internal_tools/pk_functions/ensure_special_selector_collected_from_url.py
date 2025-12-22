import logging
import webbrowser
from typing import Optional

from pk_internal_tools.pk_functions.ensure_env_var_completed import ensure_env_var_completed
from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
from pk_internal_tools.pk_functions.manage_investing_com_mappings import get_investing_com_url, set_investing_com_url
from pk_internal_tools.pk_functions.input_with_timeout import input_with_timeout
from pk_internal_tools.pk_functions.ensure_value_completed import ensure_value_completed

# 미리 추론된 investing.com URL 매핑
_INFERRED_INVESTING_COM_URLS = {
    "AAPL": "https://www.investing.com/equities/apple-computer-inc",
    "NVDA": "https://www.investing.com/equities/nvidia-corp",
    "SPY": "https://www.investing.com/etfs/spdr-s-p-500",
    "TQQQ": "https://www.investing.com/etfs/proshares-ultrpro-q-q-q",
    "QQQ": "https://www.investing.com/etfs/powershares-qqqq", # QQQ는 이미 DEFAULT_INVESTING_COM_MAPPINGS에 있지만, 여기에도 추가하여 일관성 유지
}

def _infer_investing_com_url(ticker: str) -> Optional[str]:
    """
    티커를 기반으로 investing.com URL을 추론합니다.
    """
    return _INFERRED_INVESTING_COM_URLS.get(ticker.upper())

def ensure_special_selector_collected_from_url(ticker: str):
    """
    사용자가 investing.com의 특정 티커에 대한 CSS 선택자를 설정하도록 돕는 함수입니다.
    해당 티커의 investing.com 페이지를 브라우저로 열고, 사용자에게 선택자 입력을 요청합니다.
    """
    func_n = get_caller_name()
    logging.info(f"{ticker}에 대한 investing.com 선택자 설정 시작 ---")
    
    # n. DB에서 URL 정보 조회
    mapping_info = get_investing_com_url(ticker)
    
    url = None
    current_selector = None

    if mapping_info:
        url = mapping_info['url']
        current_selector = mapping_info.get('selector')
    
    # URL이 없으면 사용자에게 입력 요청
    if not url:
        inferred_url = _infer_investing_com_url(ticker)
        
        guide_text_suffix = f" (추론값: {inferred_url})" if inferred_url else ""
        options_for_url_input = [inferred_url] if inferred_url else []

        logging.warning(f"DB에 {ticker}에 대한 investing.com URL 정보가 없습니다. URL을 입력해주세요.")
        input_url_raw = ensure_value_completed(
            key_name=f"{ticker}_investing_com_url",
            func_n="ensure_special_selector_collected_from_url",
            guide_text=f"'{ticker}'의 investing.com URL을 입력해주세요 (현재: {url if url else '없음'}){guide_text_suffix}",
            options=options_for_url_input
        )
        input_url = input_url_raw.strip() if input_url_raw else ""
        if input_url:
            set_investing_com_url(ticker, input_url) # URL만 먼저 저장
            url = input_url
            logging.info(f"'{ticker}'에 대한 URL '{url}'이 DB에 저장되었습니다.")
        else:
            logging.error("URL 입력이 취소되었거나 비어있습니다. 선택자 설정을 진행할 수 없습니다.")
            logging.info(f"{ticker}에 대한 investing.com 선택자 설정 실패 ---")
            return
    
    logging.info(f"티커: {ticker}")
    logging.info(f"현재 URL: {url}")
    logging.info(f"현재 저장된 선택자: {current_selector if current_selector else '없음'}")

    # n. 브라우저로 URL 열기
    logging.info(f"브라우저로 {url} 페이지를 엽니다. 가격 선택자를 찾아주세요.")
    webbrowser.open(url)

    # 3. 사용자에게 선택자 입력 요청
    url_normalized =  url
    url_normalized = url_normalized.replace("/","_")
    url_normalized = url_normalized.replace(".","_")
    new_selector_raw = ensure_value_completed(
        key_name=f"{ticker}_investing_com_selector",
        func_n="ensure_special_selector_collected_from_url",
        guide_text=f"'{ticker}'의 가격 선택자(CSS Selector)를 입력해주세요 (현재: {current_selector if current_selector else '없음'})",
        options=[] # No predefined options for selector
    )
    new_selector = new_selector_raw.strip() if new_selector_raw else ""
    if new_selector:
        # 4. DB에 선택자 저장
        set_investing_com_url(ticker, url, new_selector)
        logging.info(f"'{ticker}'에 대한 새로운 선택자 '{new_selector}'가 DB에 성공적으로 저장되었습니다.")
    else:
        logging.warning("선택자 입력이 취소되었거나 비어있습니다. 기존 선택자가 유지됩니다.")
    
    logging.info(f"{ticker}에 대한 investing.com 선택자 설정 완료 ---")
