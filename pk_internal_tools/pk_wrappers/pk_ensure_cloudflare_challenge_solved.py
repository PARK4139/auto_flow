import traceback

from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done

if __name__ == '__main__':
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_functions.get_selenium_driver_initialized_for_cloudflare import get_selenium_driver_initialized_for_cloudflare

    try:
        url = "https://www.scrapingcourse.com/cloudflare-challenge"

        # cloudflare security challange : try : success
        driver = get_selenium_driver_initialized_for_cloudflare()

        # cloudflare security challange : try : success
        # from seleniumbase import Driver
        # driver = Driver(uc=True, headless=True)
        # driver.uc_open_with_reconnect(url, reconnect_time=6)
        # page_src = driver.page_source
        # from bs4 import BeautifulSoup
        # soup = BeautifulSoup(page_src, "html.parser")  # web parser 설정
        # print(soup)

        # cloudflare security challange : try : success
        # from seleniumbase import Driver
        # # driver = Driver(uc=True, headless=False)
        # driver = Driver(uc=True, headless=True)
        # driver.uc_open_with_reconnect(url, reconnect_time=6)
        # page_src = driver.page_source
        # from bs4 import BeautifulSoup
        # soup = BeautifulSoup(page_src, "html.parser")  # web parser 설정
        # print(soup)

        # get magnet link from magnet page : try : fail
        # import cloudscraper
        # scraper = cloudscraper.create_scraper()
        # response = scraper.get(url)
        # if response.status_code == 200:
        #     print("Page content:", response.text)
        # else:
        #     print("Failed to fetch the page.")

        # get magnet link from magnet page : try : fail : urllib3 버전 호환성이 맞지 않아서 같음. 다운그래이드를 해야하는 것 같은
        # # Cloudflare 보호 우회
        # import cfscrape
        # scraper = cfscrape.create_scraper()
        # response = scraper.get(url)
        # if response.status_code == 200:
        #     print(response.text)  # HTML 내용
        # else:
        #     print("Failed to bypass Cloudflare protection.")

        # get magnet link from magnet page : try : fail
        # import requests
        # from bs4 import BeautifulSoup
        # response = requests.get(url)
        # soup = BeautifulSoup(response.text, "html.parser")
        # magnet_link = soup.find("a", href=True, text=lambda text: text and "magnet:?" in text)
        # if magnet_link:
        #     print(f"Extracted Magnet Link: {magnet_link['href']}")
        # else:
        #     print("No magnet link found.")

        # cloudflare security challange : try : fail
        # try_solve_cloudflare_security(driver)

        # cloudflare security challange : try : fail
        # search_url_in_browser(url = url, driver=driver)
        # click tag as with text as '방송 토렌트 - 토렌트큐큐 - TORRENTQQ'
        # ensure_slept(milliseconds=4000)  # 정적웹소스 다운로드 대기
        # click_tag_as_with_tag_text(driver=driver, tag_name='h3', tag_text='방송 토렌트 - 토렌트큐큐 - TORRENTQQ')
        # cloudflare security challange
        # try_solve_cloudflare_security(driver)

        # cloudflare security chanllege : try : fail
        # def get_graphics_card_info():
        #     try:
        #         result = subprocess.run(["wmic", "path", "win32_videocontroller", "get", "caption"],
        #                                 capture_output=True, text=True, shell=True)
        #         output = result.stdout.strip().split("\n")
        #         if len(output) > 1 and output[1].strip():
        #             return output[1].strip()  # 첫 번째 항목은 'Caption', 두 번째는 실제 그래픽 카드 이름
        #         return "Unknown GPU"
        #     except Exception as e:
        #         return "Unknown GPU"
        # graphics_card = get_graphics_card_info()
        # webgl_vendor = None
        # renderer = None
        # if graphics_card == "Unknown GPU":
        #     webgl_vendor = "NVIDIA Corporation",
        #     renderer = "NVIDIA GeForce RTX 3080",
        # else:
        #     webgl_vendor = rf"{graphics_card.split()[0]}",
        #     renderer = rf"{graphics_card}",
        # from selenium_stealth import stealth # pip install selenium-stealth
        # stealth(
        #     driver,
        #     languages=["ko-KR", "ko"],
        #     vendor="Google Korea Inc.",
        #     platform="Win64",
        #     webgl_vendor=webgl_vendor,
        #     renderer=renderer,
        #     fix_hairline=True,
        # )

        # cloudflare security challange : try : fail
        # from selenium import webdriver
        # from selenium_stealth import stealth
        # from time import sleep
        # options = webdriver.ChromeOptions()
        # # options.add_argument("--headless")
        # options.add_argument("--disable-blink-features=AutomationControlled")
        # driver = webdriver.Chrome(options=options)
        # graphics_card = "Unknown GPU"
        # if graphics_card == "Unknown GPU":
        #     webgl_vendor = "NVIDIA Corporation",
        #     renderer = "NVIDIA GeForce RTX 3080",
        # else:
        #     webgl_vendor = rf"{graphics_card.split()[0]}",
        #     renderer = rf"{graphics_card}",
        # stealth(
        #     driver,
        #     languages=["ko-KR", "ko"],
        #     vendor="Google Korea Inc.",
        #     platform="Win64",
        #     webgl_vendor=webgl_vendor,
        #     renderer=renderer,
        #     fix_hairline=True,
        # )
        # driver.get(url)
        # sleep(20)
        # page_src = driver.page_source
        # from bs4 import BeautifulSoup
        # soup = BeautifulSoup(page_src, "html.parser")  # web parser 설정
        # print(soup)
        # driver.quit()

        # cloudflare security challange : try : fail
        # import undetected_chromedriver as uc
        # from time import sleep
        # driver = uc.Chrome(use_subprocess=False, headless=True)
        # driver.get(url)
        # sleep(10)
        # page_src = driver.page_source
        # from bs4 import BeautifulSoup
        # soup = BeautifulSoup(page_src, "html.parser")  # web parser 설정
        # print(soup)
        # driver.quit()

        # cloudflare security challange : try : fail
        # from selenium import webdriver
        # from selenium.webdriver.chrome.options import Options
        # import subprocess
        # from webdriver_manager.chrome import ChromeDriverManager
        # from selenium.webdriver.chrome.service import Service
        # from selenium.webdriver.common.by import By
        # # chrome.exe 경로를 찾아입력
        # subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')
        # option = Options()
        # option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        # # driver.maximize_window()
        # driver.get(url)
        # # content 아이디를 갖는 태그부분 가져와서 출력
        # content = driver.find_element(By.ID, "content")
        # print(content)

        # cloudflare security challange : try : not yet

        # from playwright_stealth import stealth_sync
        #
        # chrome_path = rf"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Windows 예시
        #
        # with sync_playwright() as p:
        #     # Chrome 브라우저 exec 
        #     browser = p.chromium.launch_persistent_context(
        #         user_data_dir="C:\\path\\to\\user_data",
        #         executable_path=chrome_path,
        #         headless=False
        #     )
        #     page = browser.new_page()
        #
        #     # Stealth 모드 활성화
        #     stealth_sync(page)
        #     page.goto(url)
        #
        #     # Cloudflare 확인 페이지 대기
        #     page.wait_for_selector("body", timeout=10000)  # 최대 10초 대기
        #     print(page.title())
        #
        #     # 링크 추출
        #     links = page.query_selector_all("a")
        #     for link in links:
        #         print(link.get_attribute("href"))
        #
        #     print("브라우저가 열려 있습니다. 강제 종료(Ctrl+C)를 사용하세요.")
        #     while 1:
        #         pass  # 무한 대기

        # collect_magnets_from_nyaa_si(via_f_txt=True)
        # collect_magnets_from_torrentqq(via_f_txt=True)
        # download_magnets()

        ensure_spoken("cloudflare challenge solved, successfully")
        # import ipdb
        # ipdb.set_trace()
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
