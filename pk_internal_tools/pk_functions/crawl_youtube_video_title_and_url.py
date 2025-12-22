


def crawl_youtube_video_title_and_url(url: str):
    import inspect
    import tqdm

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    browser_debug_mode = False

    # url 전처리
    url = url.strip()

    # driver 설정
    total_percent = 100
    driver = get_selenium_driver(browser_debug_mode=browser_debug_mode)
    with tqdm(total=total_percent, ncols=79, desc="driver 설정 진행률") as process_bar:
        global title
        title = 'html  href 크롤링 결과'
        target_url = url
        driver.get(target_url)
        page_src = driver.page_source
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(page_src, "lxml")
        ensure_slept(seconds=0.0001)
        process_bar.update(total_percent)
    driver.close()

    # 변수에 저장 via tag_name and id
    name = soup.find_all("a", id="video-title")
    video_url = soup.find_all("a", id="video-title")

    # list 에 저장
    name_list = []
    url_list = []
    # view_list=[]
    for i in range(len(name)):
        name_list.append(name[i].text.strip())
        # view_list.append(view[i].get('aria-label').split()[-1])
    for i in video_url:
        url_list.append('{}{}'.format('https://www.youtube.com', i.get('href')))

    # dict 에 저장
    # youtubeDic={
    #     '제목': name_list,
    #     '주소': url_list,
    #     # '조회수': view_list
    # }

    # csv 에 저장
    # youtubeDf=pd.DataFrame(youtubeDic)
    # youtubeDf.to_csv(f'{keyword}.csv', encoding='', index=False)

    # str 에 저장
    results_list = []
    for index, url in enumerate(url_list):
        results_list.append(f"{name_list[index]}   {url_list[index]}")
    results_str = "\n".join(results_list)  # list to str

    # fail
    # dialog=PkGui.PkQdialog(title=f"크롤링결과보고", ment=f"{results}", btns=[YES], auto_click_positive_btn_after_milliseconds="")
    # dialog.exec()

    # fail
    # PkGui.pop_up_as_complete(title="크롤링결과보고", ment=f"{results}")

    # success
    # debug_as_gui(f"{results}") # 테스트용 팝업    PkGui 로 옮기는 게 나을 지 고민 중이다.

    # success
    # 비동기로 진행 가능
    global dialog
    dialog = PkGui.PkQdialog(title=f"크롤링결과보고", prompt=f"({len(url_list)}개 url 추출됨)\n\n{results_str}")
    dialog.show()
