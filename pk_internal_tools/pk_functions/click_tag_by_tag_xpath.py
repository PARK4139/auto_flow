import logging



def click_tag_by_tag_xpath(driver, tag_name, tag_property, tag_property_value):
    from pk_internal_tools.pk_functions.remove_block_hidden import remove_block_hidden
    timeout = 10
    try:
        # Lazy Import (이 시점에 모듈을 불러옵니다)
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import ElementClickInterceptedException

        # 페이지가 로딩될 때까지 대기
        WebDriverWait(driver, timeout).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # 태그가 DOM에 존재하고 표시될 때까지 대기
        tag = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, f"//{tag_name}[{tag_property}()='{tag_property_value}']")))

        # 태그가 클릭 가능할 때까지 대기
        tag = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, f"//{tag_name}[{tag_property}()='{tag_property_value}']")))

        # 클릭을 방해하는 요소가 있을 경우, 배경을 클릭하거나 강제로 클릭을 시도
        try:
            tag.click()  # 클릭 시도
            print(f"태그 '{tag_name}' 속성 '{tag_property}={tag_property_value}' 클릭 완료.")
        except ElementClickInterceptedException:
            # 클릭 방해 요소가 있을 경우, 배경 요소 클릭 또는 배경 숨기기
            logging.debug("클릭 방해 요소 발견, 배경을 클릭하거나 숨기려 시도합니다.")
            remove_block_hidden(driver=driver)
            # driver.execute_script("document.querySelector('.MuiBackdrop-root').style.display = 'none';")  # 배경 숨기기
            tag.click()  # 다시 클릭 시도
            print(f"태그 '{tag_name}' 속성 '{tag_property}={tag_property_value}' 클릭 완료.")

    except Exception as e:
        import traceback
        logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")
        print(f"태그 '{tag_name}' 속성 '{tag_property}={tag_property_value}' 클릭 실패.")
