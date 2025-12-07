from tkinter import UNDERLINE


import logging
from pk_internal_tools.pk_objects.pk_texts import PkTexts


def crawl_html_href(url: str):
    import inspect
    import random

    logging.debug(f"{UNDERLINE}{inspect.currentframe().f_code.co_name}")
    # 최하단으로 스크롤 이동 처리를 추가로 해야함. 그렇지 않으면 기대하는 모든 영상을 크롤링 할 수 없음..귀찮..지만 처리했다.

    browser_debug_mode = False

    # url 전처리
    url = url.strip()

    # driver 설정
    logging.debug(f"{PkTexts.SELENIUM_DRIVER_DEBUG_MODE}...")
    driver = get_selenium_driver(browser_debug_mode=browser_debug_mode)

    logging.debug(f"{PkTexts.DRIVER_GET_TARGET_URL}...")
    target_url = url
    driver.get(target_url)

    # 자동제어 브라우저 화면 초기 로딩 random.randint(1,n) 초만큼 명시적 대기
    n = 2
    seconds = random.randint(1, n)
    logging.debug(f"{PkTexts.BROWSER_SCREEN_INITIAL_LOADING}... {seconds} {PkTexts.SECONDS}")
    driver.implicitly_wait(seconds)  # 처음페이지 로딩이 끝날 때까지 약 random.randint(1,n)초 대기

    # 최하단으로 자동 스크롤, 페이지 최하단에서 더이상 로딩될 dom 객체가 없을 때 까지
    logging.debug(f"{PkTexts.SCROLL_TO_BOTTOM}...")
    scroll_cnt = 0
    previous_scroll_h = None
    current_scroll_h = None
    scroll_maxs_monitored = []
    while 1:
        if current_scroll_h is not None and previous_scroll_h is not None:
            if previous_scroll_h == current_scroll_h:
                scroll_maxs_monitored.append(True)
                # break

        # 로딩타이밍 제어가 어려워 추가한 코드. n번 모니터링.
        n = 6  # success
        if len(scroll_maxs_monitored) == n:
            if all(scroll_maxs_monitored) == True:  # [bool] bool list 내 요소가 모두 true 인지 확인
                logging.debug(f"{PkTexts.SCROLL_TO_BOTTOM_COMPLETE}")
                break

        # previous_scroll_h 업데이트
        # previous_scroll_h=driver.execute_script("return document.body.scrollHeight")
        previous_scroll_h = driver.execute_script("return document.documentElement.scrollHeight")

        # 가능한만큼 스크롤 최하단으로 이동
        # driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)  # page_down 을 누르는 방법, success
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")# JavaScript 로 스크롤 최하단으로 이동, 네이버용 코드?
        driver.execute_script(
            "window.scrollTo(0, document.documentElement.scrollHeight);")  # JavaScript 로 스크롤 최하단으로 이동, 유튜브용 코드?
        # sleep(seconds=2)  # 스크롤에 의한 추가적인 dom 객체 로딩 대기, 여러가지 예제를 보니, 일반적으로 2 초 정도 두는 것 같음. 2초 내에 로딩이 되지 않을 때도 있는데.
        ensure_slept(milliseconds=500)  # 스크롤에 의한 추가적인 dom 객체 로딩 대기, success, 지금껏 문제 없었음.

        # previous_scroll_h=driver.execute_script("return document.body.scrollHeight")
        current_scroll_h = driver.execute_script("return document.documentElement.scrollHeight")

        scroll_cnt = scroll_cnt + 1

        logging.debug(f'{scroll_cnt}번 째 스크롤 성공 previous_scroll_h : {previous_scroll_h} current_scroll_h : {current_scroll_h}   previous_scroll_h==current_scroll_h : {previous_scroll_h == current_scroll_h}')

    page_src = driver.page_source
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page_src, "lxml")
    driver.close()

    # 모든 태그 가져오기
    # tags=soup.find_all()
    # for tag in tags:
    #     print(tag)

    # body 리소스 확인 : success
    # bodys=soup.find_all("body")
    # for body in bodys:
    #     print(f"body:{body}")

    # 이미지 태그 크롤링
    # images=soup.find_all("img")
    # for img in images:
    #     img_url=img.get("src")
    #     logging.debug("Image URL:", img_url)
    #
    # 스크립트 태그 크롤링
    # scripts=soup.find_all("script")
    # for script in scripts:
    #     script_url=script.get("src")
    #     logging.debug("Script URL:", script_url)
    #
    # # 스타일시트 크롤링
    # stylesheets=soup.find_all("link", rel="stylesheet")
    # for stylesheet in stylesheets:
    #     stylesheet_url=stylesheet.get("href")
    #     logging.debug("Stylesheet URL:", stylesheet_url)

    # 특정 태그의 class 가 "어쩌구" 인
    # div_tags=soup.find_all("div", class_="어쩌구")

    # a 태그 크롤링
    # a_tags=soup.find_all("a")
    # results=""
    # for a_tag in a_tags:
    #     hrefs=a_tag.get("href")
    #     if hrefs is not None and hrefs != "":
    #         # logging.debug("href", hrefs)
    #         results=f"{results}{hrefs}\n"

    # 변수에 저장 via selector
    # name=soup.select('a#video-title')
    # video_url=soup.select('a#video-title')
    # view=soup.select('a#video-title')

    # name, video_url 에 저장 via tag_name and id
    name = soup.find_all("a", id="video-title")
    video_url = soup.find_all("a", id="video-title")

    # 유튜브 주소 크롤링 및 진행률 표시 via tqdm, 14 초나 걸리는데. 성능이 필요할때는 여러개의 thread 로 처리해보자.
    a_tags = soup.find_all("a")

    # success
    # debug_as_gui(f"{len(a_tags)}")

    # results를 str으로 처리
    # results=""
    # a_tags_cnt =0
    # with tqdm(total=total_percent,ncols=79 , desc= "웹 크롤링 진행률") as process_bar:
    #     for a_tag in a_tags:
    #         hrefs=a_tag.get("href")
    #         if hrefs is not None and hrefs != "" and "/watch?v=" in hrefs :
    #             if hrefs not in results:
    #                 results=f"{results}{hrefs}\n"
    #                 a_tags_cnt=a_tags_cnt + 1
    #         sleep(seconds=0.06)
    #         process_bar.update(total_percent/len(a_tags))

    # fail
    # if process_bar.total == 90:
    #     speak_ments(ment='웹 크롤링이 90퍼센트 진행되었습니다. 잠시만 기다려주세요', sleep_after_play=0.65)

    # results를 list 으로 처리, list 으로만 처리하고 str 으로 변형하는 처리를 추가했는데 3초나 빨라졌다. 항상 list 로 처리를 하자.
    results = []
    a_tags_cnt = 0
    for a_tag in a_tags:
        hrefs = a_tag.get("href")
        if hrefs is not None and hrefs != "" and "/watch?v=" in hrefs:
            if hrefs not in results:
                results.append(hrefs)
                a_tags_cnt = a_tags_cnt + 1
    results = DataStructureUtil.add_prefix_to_string_list(results,
                                                          'https://www.youtube.com')  # string list 의 요소마다 suffix 추가
    results = "\n".join(results)  # list to str

    # fail
    # dialog=PkGui.PkQdialog(title=f"크롤링결과보고", ment=f"{results}", btns=[YES], auto_click_positive_btn_after_seconds="")
    # dialog.exec()

    # fail
    # PkGui.pop_up_as_complete(title="크롤링결과보고", ment=f"{results}")

    # success
    # debug_as_gui(f"{results}") # 테스트용 팝업    PkGui 로 옮기는 게 나을 지 고민 중이다.

    # success
    # 비동기로 진행 가능
    global dialog
    dialog = PkGui.PkQdialog(title=f"크롤링결과보고", prompt=f"({a_tags_cnt}개 추출됨)\n\n{results}")
    dialog.show()
