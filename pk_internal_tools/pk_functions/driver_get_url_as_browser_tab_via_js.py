def driver_get_url_as_browser_tab_via_js(driver, url):
    from pk_internal_tools.pk_functions.kill_tabs_except_current_tab_via_selenium import kill_tabs_except_current_tab_via_selenium
    driver.execute_script(rf"window.open('{url}', '_blank');")
    # new_window = [window for window in driver.window_handles if window != original_window][0]
    # driver.switch_to.window(new_window)  # move to magnets btn page
    kill_tabs_except_current_tab_via_selenium(driver)  # 나머지 탭 닫기
