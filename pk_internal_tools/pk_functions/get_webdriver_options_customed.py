import logging


def get_webdriver_options_customed(browser_debug_mode=True, proxy=None):
    from selenium.webdriver.chrome.options import Options
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    # options=webdriver.ChromeOptions()
    options = Options()

    if proxy is not None:
        options.add_argument(f'--proxy-server={proxy}')

    # 브라우저 최대화
    # options.add_argument("--start-maximized")

    # 셀레니움 브라우저 show 설정
    if browser_debug_mode == True:
        # options.add_argument('--headless')
        pass
    elif browser_debug_mode == False:
        options.add_argument('--headless')
    # options.add_argument('--window-size=3440x1440')
    # options.add_argument('--window-size=1920x1080')
    # options.add_argument("window-size=1200x600")
    # options.add_argument("window-size=1210x630")
    # options.add_argument('--window-size=800x800')
    # size 하드코딩 되어 있는 부분을 pyautogui 에서 size() 로 대체하는 것이 좋겠다.

    # 셀레니움 브라우저 언어
    options.add_argument("lang=ko_KR")

    # init my_chrome_version
    # https://www.whatismybrowser.com/detect/what-is-my-user-agent/ # IP 차단됨
    # https://detectmybrowser.com/ # 대안
    my_chrome_version = "131"

    # init UserAgent
    user_agent = rf"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{my_chrome_version}.0.0.0 Safari/537.36"

    # init UserAgent , as random
    # 쓸려면 구체적으로 설정
    # ua = UserAgent()
    # user_agent = ua.chrome.replace("en-US", "ko-KR")  # 랜덤 최신 크롬 User-Agent, 생성된 User-Agent에서 언어를 한국어로 변경
    options.add_argument(f"user-agent={user_agent}")
    logging.debug(f'''user_agent={user_agent}''')

    # 자동화 감지 비활성화
    options.add_argument("--disable-blink-features=AutomationControlled")

    # 자동화 스위치 비활성화
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # 자동화 확장 비활성화
    options.add_experimental_option("useAutomationExtension", False)

    # Chrome 기본 프로필
    # profile_path=rf'{USERPROFILE}\AppData\Local\Google\Chrome\User Data'
    # options.add_argument(f"user-data-dir={profile_path}")
    # options.add_argument("profile-directory=Default")

    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    options.set_capability("acceptInsecureCerts", True)
    options.set_capability("browserName", "chrome")

    # proxy
    # options.add_argument(f"--proxy-server={proxy}")

    return options
