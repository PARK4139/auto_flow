def get_videos_urls_from_youtube_channel_main_page(url_youtube_channel_main_page, debug_mode=True):
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    import logging
    from pk_internal_tools.pk_functions.get_selenium_driver import get_selenium_driver
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from selenium.webdriver.common.by import By
    driver = get_selenium_driver(headless_mode=debug_mode)
    driver.get(url_youtube_channel_main_page)

    # 스크롤을 끝까지 내리기
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while 1:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        # sleep(seconds=random.randint(a=2, b=10))
        ensure_slept(seconds=5)  # 스크롤 사이에 대기시간 추가
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # 동영상탭 처리
    video_urls = set()
    videos = driver.find_elements(By.XPATH, '//a[@id="thumbnail"]')
    for video in videos:
        url = video.get_attribute("href")
        if url and "watch" in url:  # 영상 링크인지 확인
            video_urls.add(url)

    # shorts탭 처리
    shorts_elements = driver.find_elements(By.CSS_SELECTOR, "a.shortsLockupViewModelHostEndpoint")
    for element in shorts_elements:
        href = element.get_attribute("href")
        if href and "/shorts/" in href:
            video_urls.add(href)

    driver.quit()

    video_urls_list = None
    video_urls_list = list(video_urls)
    logging.debug(f'''len(video_urls_list)="{len(video_urls_list)}"  ''')
    for idx, url in enumerate(video_urls, start=1):
        logging.debug(f'''f"{idx}: {url}"''')
    return video_urls_list
