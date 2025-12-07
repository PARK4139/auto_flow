import asyncio
import logging
import traceback
from dataclasses import dataclass
from typing import List, Optional

from bs4 import BeautifulSoup

from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
from pk_internal_tools.pk_objects.pk_gui import PkGui
from pk_internal_tools.pk_functions.get_selenium_driver import get_selenium_driver
# --- 프로젝트 의존성 ---
# 아래 모듈들은 프로젝트 내에 존재한다고 가정합니다.
# Lazy-loading 규칙에 따라 함수 내에서 import 할 수도 있습니다.
from pk_internal_tools.pk_functions.is_internet_connected_2025_10_21 import is_internet_connected_2025_10_21


# --- 데이터 구조 정의 ---
@dataclass
class CrawlResult:
    """크롤링 결과 저장을 위한 기본 데이터 클래스"""
    title: str
    details: str


# --- 개별 크롤링 함수 ---

async def crawl_pm_ranking() -> Optional[CrawlResult]:
    """미세먼지 랭킹 정보를 dustrank.com 에서 크롤링합니다."""
    driver = None
    try:
        driver = get_selenium_driver(browser_debug_mode=False)
        target_url = 'https://www.dustrank.com/air/air_dong_detail.php?addcode=41173103'
        driver.get(target_url)
        soup = BeautifulSoup(driver.page_source, "lxml")

        results_table = soup.find("table", class_="datatable")
        if not results_table:
            logging.warning("미세먼지 랭킹 테이블을 찾을 수 없습니다.")
            return None

        rows = results_table.find_all("tr")
        header = " ".join(rows[1].text.split()) + " " + " ".join(rows[2].text.split())

        body_lines = []
        for row in rows[3:]:
            cols = [col.text.strip() for col in row.find_all('td')]
            if cols:
                body_lines.append(" ".join(cols))

        details = f"{header}\n" + "\n".join(body_lines)
        return CrawlResult(title="미세먼지 랭킹", details=details)
    except Exception:
        logging.error(f"미세먼지 랭킹 크롤링 중 오류 발생: {traceback.format_exc()}")
        return None
    finally:
        if driver:
            driver.quit()


async def crawl_nationwide_ultrafine_dust() -> Optional[CrawlResult]:
    """네이버에서 전국 초미세먼지 정보를 크롤링합니다."""
    driver = None
    try:
        driver = get_selenium_driver(browser_debug_mode=False)
        target_url = 'https://search.naver.com/search.naver?query=전국초미세먼지'
        driver.get(target_url)
        soup = BeautifulSoup(driver.page_source, "lxml")

        detail_box = soup.find("div", class_="detail_box")
        if not detail_box:
            logging.warning("전국 초미세먼지 정보 박스를 찾을 수 없습니다.")
            return None

        lines = detail_box.text.split('\n')
        clean_lines = [" ".join(line.split()) for line in lines if line.strip()]
        details = "\n".join(clean_lines)
        return CrawlResult(title="전국 초미세먼지", details=details)
    except Exception:
        logging.error(f"전국 초미세먼지 크롤링 중 오류 발생: {traceback.format_exc()}")
        return None
    finally:
        if driver:
            driver.quit()


async def crawl_naver_weather() -> Optional[CrawlResult]:
    """네이버에서 지역 날씨 정보를 크롤링합니다."""
    driver = None
    try:
        driver = get_selenium_driver(browser_debug_mode=False)
        target_url = 'https://search.naver.com/search.naver?query=동안구+관양동+날씨'
        driver.get(target_url)
        soup = BeautifulSoup(driver.page_source, "lxml")

        status_wrap = soup.find("div", class_="status_wrap")
        if not status_wrap:
            logging.warning("지역 날씨 정보 박스를 찾을 수 없습니다.")
            return None

        lines = status_wrap.text.split('\n')
        clean_lines = [line.strip() for line in lines if line.strip()]
        details = "\n".join(clean_lines)
        return CrawlResult(title="동안구 관양동 날씨", details=details)
    except Exception:
        logging.error(f"지역 날씨 크롤링 중 오류 발생: {traceback.format_exc()}")
        return None
    finally:
        if driver:
            driver.quit()


async def crawl_geo_info() -> Optional[CrawlResult]:
    """구글에서 현재 위치 정보를 크롤링합니다."""
    driver = None
    try:
        driver = get_selenium_driver(browser_debug_mode=False)
        target_url = 'https://www.google.com/search?q=현재위치'
        driver.get(target_url)
        soup = BeautifulSoup(driver.page_source, "lxml")

        location_span = soup.find("span", class_="BBwThe")
        if not location_span:
            logging.warning("현재 위치 정보를 찾을 수 없습니다.")
            return None

        location = location_span.text
        return CrawlResult(title="현재 위치", details=location)
    except Exception:
        logging.error(f"현재 위치 크롤링 중 오류 발생: {traceback.format_exc()}")
        return None
    finally:
        if driver:
            driver.quit()


def display_results(results: List[Optional[CrawlResult]]):
    """크롤링된 정보를 GUI 다이얼로그에 표시합니다."""
    dialogs = []
    for result in results:
        if result:
            dialog = PkGui.PkQdialog(title=result.title, prompt=result.details)
            dialog.show()
            dialogs.append(dialog)

    # 참고: dialog.show()는 non-blocking 입니다.
    # 스크립트가 바로 종료되면 다이얼로그가 사라질 수 있습니다.
    # 실제 GUI 애플리케이션에서는 이벤트 루프를 다르게 관리해야 합니다.
    if dialogs:
        logging.info(f"{len(dialogs)}개의 정보창을 표시했습니다.")


async def _async_main():
    """모든 크롤링 작업을 비동기적으로 실행하고 결과를 수집합니다."""
    tasks = [
        crawl_pm_ranking(),
        crawl_nationwide_ultrafine_dust(),
        crawl_naver_weather(),
        crawl_geo_info(),
    ]
    results = await asyncio.gather(*tasks)
    return results


def get_comprehensive_weather_information_from_web():
    """
    웹에서 날씨 및 미세먼지 정보를 종합적으로 크롤링하고 처리하여 GUI로 보여주는 메인 함수.
    (가독성, 유지보수성, 정확성을 위해 재구성된 버전)
    """
    try:
        if not is_internet_connected_2025_10_21():
            logging.error("인터넷에 연결되어 있지 않아 웹 정보를 가져올 수 없습니다.")
            raise ConnectionError("Internet is not connected.")

        # 비동기 메인 함수를 실행하여 모든 데이터를 수집
        results = asyncio.run(_async_main())

        # 결과 표시
        display_results(results)

        # 작업 완료 음성 안내
        successful_crawls = sum(1 for r in results if r is not None)
        if successful_crawls > 0:
            ensure_spoken(text=f'{successful_crawls}개의 웹 크롤링 및 데이터 분석에 성공했습니다.')
        else:
            ensure_spoken(text='웹 크롤링에 실패했습니다. 로그를 확인해주세요.')

    except Exception:
        logging.error(f"종합 날씨 정보 수집 중 예기치 않은 오류 발생: {traceback.format_exc()}")
        ensure_spoken(text='작업 중 오류가 발생했습니다.')
