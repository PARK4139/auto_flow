


def click_tag_as_with_tag_text(driver, tag_name, tag_text):
    import logging
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    try:
        h3_element = driver.find_element(By.XPATH, rf"//{tag_name}[text()='{tag_text}']")
        actions = ActionChains(driver)
        actions.move_to_element(h3_element).click().perform()
    except Exception as e:
        logging.debug(f'''click {tag_name} tag with text as {tag_text} fail  ''')
