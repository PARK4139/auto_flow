

def is_url_open_via_selenium(url_to_check):
    """
    Selenium을 사용하여 특정 URL이 열려 있는지 확인하고, 열려 있지 않으면 새로 열기
    """
    from selenium.webdriver.chrome.options import Options

    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # 브라우저 최대화
    chrome_options.add_argument("--disable-infobars")  # 브라우저 정보 표시 비활성화
    chrome_options.add_argument("--disable-extensions")  # 확장 프로그램 비활성화
    chrome_options.add_experimental_option("detach", True)  # 브라우저 종료 방지

    # ChromeDriver exec
    driver = get_selenium_driver(browser_debug_mode=True)

    # 열려 있는 모든 탭 가져오기
    handles = driver.window_handles
    url_found = False

    for handle in handles:
        driver.switch_to.window(handle)
        if url_to_check in driver.current_url:
            print(f"이미 열려 있는 URL: {driver.current_url}")
            url_found = True
            break

    # URL이 열려 있지 않으면 새로 열기
    if not url_found:
        print(f"URL 열려 있지 않음. 새 탭으로 열기: {url_to_check}")
        driver.execute_script(f"window.open('{url_to_check}', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])  # 새로 연 탭으로 전환

    # 드라이버 유지 (필요 시)
    return driver
