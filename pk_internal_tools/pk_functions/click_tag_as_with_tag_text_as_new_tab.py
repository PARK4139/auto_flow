import mutagen
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


def click_tag_as_with_tag_text_as_new_tab(driver, tag_name, tag_text):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys
    try:
        element = driver.find_element(By.XPATH, rf"//{tag_name}[text()='{tag_text}']")

        # 새 탭에서 열기
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).move_to_element(element).click().key_up(Keys.CONTROL).perform()

        # 새 탭으로 전환
        driver.switch_to.window(driver.window_handles[-1])
        print(f"'{tag_text}'가 포함된 {tag_name} 태그를 새 탭에서 열고 전환했습니다.")
    except Exception as e:
        print(f'''{tag_name} 태그(텍스트: {tag_text})를 새 탭에서 여는 데 실패했습니다: {str(e)}''')
