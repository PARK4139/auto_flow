import logging
import json
import re
import hashlib
from typing import Optional, Tuple, Dict
from bs4 import BeautifulSoup
from pk_internal_tools.pk_functions.get_pretty_html_string import get_pretty_html_string
from pk_internal_tools.pk_functions.manage_investing_com_mappings import get_investing_com_url, set_investing_com_url
from pk_internal_tools.pk_functions.ensure_special_selector_collected_from_url import ensure_special_selector_collected_from_url # Assuming this is the old, user-prompting function

# Regex patterns for common price formats
PRICE_PATTERNS = [
    re.compile(r'\d{1,3}(?:,\d{3})*(?:\.\d+)?'),  # e.g., 1,234.56 or 123.45
    re.compile(r'\d+(?:\.\d{2})'),  # e.g., 123.45 (strict two decimals)
    re.compile(r'^\$\s*\d{1,3}(?:,\d{3})*(?:\.\d+)?'),  # e.g., $ 1,234.56
    re.compile(r'^\d{1,3}(?:,\d{3})*(?:\.\d+)?\s*원'),  # e.g., 1,234.56 원
]

# Common attributes/classes indicating price
PRICE_KEYWORDS = ['price', 'value', 'last', 'current', 'quote', 'bid', 'ask', 'rate']


# _generate_structure_hash 헬퍼 함수
def _generate_structure_hash(html_content: str, soup: BeautifulSoup) -> str:
    """
    HTML 콘텐츠에서 가격 관련 구조의 해시를 생성합니다.
    JSON-LD가 있으면 JSON-LD의 해시를, 없으면 주요 가격 태그의 해시를 사용합니다.
    """
    # JSON-LD 해시 시도
    try:
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_ld_scripts:
            if script.string:
                # JSON-LD 내용을 정규화하여 해시 생성 (순서, 공백 무시)
                normalized_json = json.dumps(json.loads(script.string), sort_keys=True, separators=(',', ':'))
                return hashlib.md5(normalized_json.encode('utf-8')).hexdigest()
    except Exception:
        pass # JSON-LD 파싱 실패 시 다음 단계로

    # JSON-LD가 없거나 실패하면 주요 가격 태그의 해시 시도
    try:
        # data-test="instrument-price-last" 태그의 HTML 구조 해시
        price_element = soup.select_one('[data-test="instrument-price-last"]')
        if price_element:
            return hashlib.md5(str(price_element).encode('utf-8')).hexdigest()
    except Exception:
        pass

    # 최종적으로 아무것도 찾지 못하면 전체 HTML의 일부 해시 (덜 정확)
    return hashlib.md5(html_content[:1000].encode('utf-8')).hexdigest() # 처음 1000자만 해시


def get_css_selector_for_element(element) -> Optional[str]:
    """
    BeautifulSoup element로부터 CSS 선택자를 생성합니다.
    가장 고유하고 짧은 선택자를 생성하려고 시도합니다.
    """
    # 이 함수는 아직 구현되지 않았으므로 임시 구현
    # 실제 구현에서는 element의 id, class, nth-of-type 등을 조합하여 선택자를 만듭니다.
    # 여기서는 간단하게 id 또는 클래스 중 하나를 반환합니다.
    if element.get('id'):
        return f'#{element["id"]}'
    if element.get('class'):
        return f'.{".".join(element["class"])}'
    
    # 상위 요소로 올라가면서 경로 생성 (간단화)
    path = []
    for el in element.parents:
        if el.name == 'body':
            break
        if el.get('id'):
            path.insert(0, f'#{el["id"]}')
            break
        path.insert(0, el.name)
    
    if path:
        return ' > '.join(path)
    return element.name # 최후의 수단


def _find_and_store_auto_selector(soup: BeautifulSoup, url: str, ticker: str) -> Optional[str]:
    """
    페이지에서 가격처럼 보이는 요소를 자동으로 찾아 CSS 선택자를 생성하고 DB에 저장합니다.
    """
    logging.info(f"가격 자동 선택자 탐색 시작 (URL: {url}, 티커: {ticker})")
    
    potential_elements_with_price = []

    # 1. PRICE_KEYWORDS를 포함하는 id/class를 가진 요소 탐색
    for tag in ['span', 'div', 'b', 'strong', 'td']:
        for keyword in PRICE_KEYWORDS:
            # ID 기준
            elements_by_id = soup.select(f'{tag}[id*="{keyword}"]')
            for el in elements_by_id:
                text = el.get_text(strip=True)
                if any(pattern.search(text) for pattern in PRICE_PATTERNS):
                    potential_elements_with_price.append((el, text))
            
            # Class 기준
            elements_by_class = soup.select(f'{tag}[class*="{keyword}"]')
            for el in elements_by_class:
                text = el.get_text(strip=True)
                if any(pattern.search(text) for pattern in PRICE_PATTERNS):
                    potential_elements_with_price.append((el, text))
    
    # 2. 모든 텍스트 기반 탐색 (조금 더 일반적)
    if not potential_elements_with_price: # 위에서 찾지 못했을 경우만
        for tag in ['span', 'div', 'b', 'strong', 'td']:
            for el in soup.find_all(tag):
                text = el.get_text(strip=True)
                if any(pattern.search(text) for pattern in PRICE_PATTERNS):
                    potential_elements_with_price.append((el, text))

    # 가장 적합한 선택자 선택 (여기서는 첫 번째 찾은 것을 사용)
    if potential_elements_with_price:
        best_element, price_text = potential_elements_with_price[0]
        best_selector = get_css_selector_for_element(best_element)
        
        if best_selector:
            logging.info(f"자동으로 찾은 가격 선택자: '{best_selector}', 가격 텍스트: '{price_text}'")
            # DB에 저장
            set_investing_com_url(ticker, url, best_selector, _generate_structure_hash(soup.prettify(), soup))
            return best_selector
    
    logging.warning("페이지에서 유효한 가격 선택자를 자동으로 찾지 못했습니다.")
    return None


def get_price_from_investing_com(url: str, user_selector: Optional[str] = None, ticker: Optional[str] = None) -> Tuple[str, str]:
    """
    investing.com URL에서 구조화 데이터(JSON-LD), 사용자 정의 선택자,
    자동 감지된 선택자 또는 HTML 태그를 파싱하여 가격을 추출합니다.
    """
    try:
        import cloudscraper
        # ensure_special_selector_collected_from_url removed from here as per plan
        
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url)
        response.raise_for_status()
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # --- 구조 변경 탐지 ---
        current_structure_hash = _generate_structure_hash(html_content, soup)
        mapping_info = get_investing_com_url(ticker) # 티커로 매핑 정보 가져오기
        stored_structure_hash = mapping_info.get('structure_hash') if mapping_info else None

        # Try to use an existing user_selector if available from mapping_info
        if not user_selector and mapping_info and mapping_info.get('selector'):
            user_selector = mapping_info.get('selector')

        # If page structure changed or no selector stored, try to auto-find
        if (stored_structure_hash and stored_structure_hash != current_structure_hash) or not user_selector:
            logging.info("페이지 구조 변경 감지 또는 선택자 없음. 자동 선택자 탐색 시작.")
            auto_found_selector = _find_and_store_auto_selector(soup, url, ticker)
            if auto_found_selector:
                user_selector = auto_found_selector # Update user_selector with auto-found one
                # Update hash in DB if auto-found
                set_investing_com_url(ticker, url, user_selector, current_structure_hash)
            else:
                logging.warning(f"자동 선택자 탐색 실패. 수동 설정이 필요할 수 있습니다.")
                # Fallback to user input if auto detection fails
                ensure_special_selector_collected_from_url(ticker) # Still need to ask user if all else fails
                mapping_info = get_investing_com_url(ticker)
                user_selector = mapping_info.get('selector') if mapping_info else None
                if mapping_info:
                    set_investing_com_url(ticker, url, user_selector, current_structure_hash)
        
        # After all attempts to get/auto-find a selector, if still no selector, it means user interaction (if any) also failed
        if not user_selector:
            logging.error(f"{ticker}에 대한 유효한 선택자를 찾거나 설정할 수 없습니다. 크롤링을 진행할 수 없습니다.")
            return "N/A", "선택자 설정 실패"

        price_from_json_ld = "N/A"
        price_from_user_auto_selector = "N/A"
        price_from_data_test = "N/A"
        final_price = "N/A"
        source_method = "N/A"

        # --- 레벨 2: JSON-LD 구조화 데이터 파싱 시도 ---
        try:
            json_ld_scripts = soup.find_all('script', type='application/ld+json')
            for script in json_ld_scripts:
                if not script.string: continue
                data = json.loads(script.string)
                if data.get('@type') in ['Product', 'FinancialProduct', 'Etf', 'Stock'] and 'offers' in data:
                    offers = data['offers']
                    offer = offers[0] if isinstance(offers, list) and offers else offers
                    if offer.get('@type') == 'Offer' and 'price' in offer:
                        price_from_json_ld = str(offer['price'])
                        logging.info(f"JSON-LD에서 가격을 찾았습니다: {price_from_json_ld}")
                        break
        except Exception as e:
            logging.debug(f"JSON-LD 파싱 중 오류 발생 (무시하고 다음 단계 진행): {e}")

        # --- 레벨 3 (사용자/자동 선택자): 저장된 선택자 파싱 시도 ---
        if user_selector: # user_selector는 수동 설정되거나 자동으로 탐지된 선택자
            try:
                user_element = soup.select_one(user_selector)
                if user_element and user_element.text.strip():
                    price_from_user_auto_selector = user_element.text.strip()
                    logging.info(f"사용자/자동 선택자 '{user_selector}'로 가격을 찾았습니다: {price_from_user_auto_selector}")
            except Exception as e:
                logging.debug(f"사용자/자동 선택자 '{user_selector}' 파싱 중 오류 발생 (무시): {e}")

        # --- 레벨 3 (data-test): data-test HTML 태그 파싱 시도 ---
        try:
            data_test_element = soup.select_one('[data-test="instrument-price-last"]')
            if data_test_element and data_test_element.text.strip():
                price_from_data_test = data_test_element.text.strip()
                logging.info(f"HTML data-test 태그에서 가격을 찾았습니다: {price_from_data_test}")
        except Exception as e:
            logging.debug(f"HTML data-test 태그 파싱 중 오류 발생 (무시): {e}")

        # --- 결과 로깅 및 최종 값 결정 ---
        logging.info(f"스크레이핑 결과 비교: [JSON-LD: {price_from_json_ld}] vs [선택자: {price_from_user_auto_selector}] vs [data-test: {price_from_data_test}]")

        # 최종 반환 값 결정 (우선순위: JSON-LD > 사용자/자동 선택자 > data-test)
        if price_from_json_ld != "N/A":
            final_price = price_from_json_ld
            source_method = "LV2 LD 구조 기반 크롤링 결과"
        elif price_from_user_auto_selector != "N/A":
            final_price = price_from_user_auto_selector
            source_method = "LV3 사용자/자동 선택자 기반 크롤링 결과"
        elif price_from_data_test != "N/A":
            final_price = price_from_data_test
            source_method = "LV3 data-test 속성 기반 크롤링 결과"
        else:
            logging.warning(f"investing.com의 모든 방법으로 가격 정보를 찾는 데 실패했습니다: {url}")
            final_price = "N/A"
            source_method = "모든 크롤링 방법 실패"
        
        # 최종 가격과 사용된 방법을 튜플로 반환
        return final_price, source_method

    except ImportError:
        logging.error("'cloudscraper' 또는 'beautifulsoup4' 라이브러리가 필요합니다.")
        return "N/A", "크롤러 라이브러리 오류"
    except Exception as e:
        logging.error(f"investing.com({url}) 크롤링 중 오류 발생: {e}")
        return "N/A", f"크롤링 오류: {e}"