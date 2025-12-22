




def does_normal_tab_exist(selenium_driver, tab_title_negative):
    import random

    for window in selenium_driver.window_handles:  # 모든 탭 이동
        selenium_driver.switch_to.window(window)  # 각 탭으로 전환
        ensure_slept(milliseconds=random.randint(22, 2222))
        if tab_title_negative not in selenium_driver.title:  # 탭 제목 확인
            return 1
    return 0
