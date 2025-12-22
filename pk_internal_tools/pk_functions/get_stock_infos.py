import logging
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import List

import yfinance as yf

# Removed: from pk_internal_tools.pk_functions.ensure_special_selector_collected_from_url import ensure_special_selector_collected_from_url
from pk_internal_tools.pk_functions.get_price_from_investing_com import get_price_from_investing_com
from pk_internal_tools.pk_functions.manage_investing_com_mappings import get_investing_com_url
from pk_internal_tools.pk_objects.pk_interesting_info import StockInfoItem
from pk_internal_tools.pk_objects.pk_directories import D_PK_CACHE

STOCK_DB_PATH = Path(D_PK_CACHE) / "stock_data.sqlite"


def _init_stock_db():
    # 기존 _init_stock_db 함수 내용 유지
    pass


def _is_korean_ticker(ticker: str) -> bool:
    return bool(re.fullmatch(r'^\d{6}$', ticker))


def get_stock_infos(tickers: List[str]) -> List[StockInfoItem]:
    stock_items: List[StockInfoItem] = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for ticker in tickers:
        if _is_korean_ticker(ticker):
            try:
                import requests
                from bs4 import BeautifulSoup

                url = f"https://finance.naver.com/item/main.naver?code={ticker}"
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                }
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                name_element = soup.select_one('#middle > div.h_company > div.wrap_company > h2 > a')
                stock_name = name_element.get_text(strip=True) if name_element else ticker

                price_element = soup.select_one('#chart_area .rate_info .today .blind')
                if not price_element:
                    price_element = soup.select_one('p.no_today .blind')

                current_price = price_element.get_text(strip=True) if price_element else 'N/A'

                logging.info(f"네이버 증권에서 {ticker} 정보를 성공적으로 조회했습니다.")
                stock_items.append(StockInfoItem(
                    name=stock_name,
                    code=ticker,
                    price=current_price,
                    source_date=current_time,
                    source=url
                ))

            except Exception as e:
                logging.error(f"네이버 증권을 이용한 주식 정보 조회 중 오류 발생 (티커: {ticker}): {e}")
                stock_items.append(StockInfoItem(
                    name=ticker,
                    code=None,
                    price="N/A",
                    source_date=current_time,
                    source="네이버증권 웹크롤링 기준"
                ))
        else:
            # 해외 주식: yfinance를 기본으로 사용
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                stock_name = info.get('longName') or info.get('shortName') or ticker

                if info and info.get('regularMarketPrice'):
                    current_price = str(info.get('regularMarketPrice'))
                    market_time_unix = info.get('regularMarketTime')
                    market_time_str = datetime.fromtimestamp(market_time_unix).strftime("%Y-%m-%d %H:%M:%S") if market_time_unix else current_time
                    logging.info(f"yfinance에서 {ticker} 정보를 성공적으로 조회했습니다.")
                    stock_items.append(StockInfoItem(
                        name=stock_name, code=ticker, price=current_price,
                        source_date=market_time_str, source="yfinance"
                    ))
                else:
                    logging.warning(f"yfinance에서 {ticker} 정보를 찾을 수 없습니다.")
                    stock_items.append(StockInfoItem(
                        name=stock_name,
                        code=ticker,
                        price="N/A",
                        source_date=current_time,
                        source="yfinance",
                        reason="Not found by yfinance"
                    ))
            except Exception as e:
                logging.error(f"yfinance를 이용한 주식 정보 조회 중 오류 발생 (티커: {ticker}): {e}")
                stock_items.append(StockInfoItem(
                    name=ticker,
                    code=None,
                    price="N/A",
                    source_date=current_time,
                    source="yfinance",
                    reason=f"yfinance error: {e}"
                ))

            # 추가 소스: investing.com 크롤링
            # get_price_from_investing_com 함수 내부에서 선택자 설정 및 자동 감지 로직을 처리합니다.
            # get_investing_com_url을 통해 DB에서 URL 매핑 정보만 가져옵니다.
            mapping_info = get_investing_com_url(ticker)
            
            # investing_com_selector는 이제 get_price_from_investing_com 함수 내부에서 결정됩니다.
            # 여기서는 단지 investing.com URL만 제공합니다.
            investing_com_url = mapping_info['url'] if mapping_info else None
            
            if investing_com_url:
                logging.debug(f"investing.com에서 {ticker} 정보 크롤링 시도: {investing_com_url}")
                
                # get_price_from_investing_com 함수가 이제 선택자 설정 및 자동 감지 로직을 내부적으로 처리합니다.
                price, source_method = get_price_from_investing_com(investing_com_url, ticker=ticker)
                
                if price and price != "N/A":
                    stock_items.append(StockInfoItem(
                        name=stock_name,
                        code=ticker,
                        price=price,
                        source_date=current_time,
                        source=f"{investing_com_url}({source_method})" # 사용된 방법만 명시 (선택자는 내부에서 처리)
                    ))
                else:
                    stock_items.append(StockInfoItem(
                        name=stock_name,
                        code=ticker,
                        price="N/A",
                        source_date=current_time,
                        source="investing.com",
                        reason=f"Price not found on Investing.com ({source_method})"
                    ))
            else:
                logging.warning(f"{ticker}에 대한 investing.com URL 매핑 정보를 찾을 수 없어 크롤링을 건너킵니다.")
                stock_items.append(StockInfoItem(
                    name=stock_name,
                    code=ticker,
                    price="N/A",
                    source_date=current_time,
                    source="investing.com",
                    reason="Investing.com URL not mapped in DB"
                ))
    # --- Phase 3: 신뢰성 통계 계산 및 추가 ---

    # n. 티커별로 가격 정보 그룹화
    grouped_prices = defaultdict(list)
    for item in stock_items:
        if item.price != "N/A":  # 유효한 가격만 통계에 포함
            grouped_prices[item.code].append(item.price)

    # n. 각 티커별로 통계 계산 및 StockInfoItem 추가
    for ticker_code, prices in grouped_prices.items():
        if not prices:
            continue

        unique_prices = list(set(prices))
        comparison_value = "N/A"
        comparison_score = "N/A"

        if len(unique_prices) == 1:
            comparison_value = unique_prices[0]
            comparison_score = "모든 출처 가격 일치 (높은 신뢰도)"
        else:
            comparison_value = f"불일치: {', '.join(unique_prices)}"
            comparison_score = "출처별 가격 불일치 (확인 필요)"

        # 통계 정보를 담을 StockInfoItem 생성
        # 이 StockInfoItem은 특별한 용도이므로 name, source 등을 명확히 합니다.
        # 기존 stock_items 리스트에 추가하여 __str__에서 처리되도록 합니다.
        stock_items.append(StockInfoItem(
            name=f"{ticker_code} 비교 통계",  # 통계임을 명확히
            code=ticker_code,
            price=comparison_value,
            source_date=current_time,
            source="내부 비교 분석",
            comparison_value=comparison_value,
            comparison_score=comparison_score
        ))

    return stock_items