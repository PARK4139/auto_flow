def kill_tabs_except_current_tab_via_selenium(driver):
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept

    current_window = driver.current_window_handle
    for window in driver.window_handles:
        if window != current_window:
            driver.switch_to.window(window)
            # press("ctrl", "w"5)
            driver.close()  # 탭 닫기
            ensure_slept(seconds=0.1)
        #     ensure_slept(milliseconds=random.randint(a=22, b=2222))
        # ensure_slept(milliseconds=random.randint(a=22, b=2222))

    driver.switch_to.window(current_window)
