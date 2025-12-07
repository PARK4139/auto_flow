
from pk_internal_tools.pk_functions.get_pnx_unix_style import get_pnx_unix_style


def get_channel_n(channel_url, driver=None):
    from selenium.webdriver.common.by import By
    if driver is None:
        driver = get_selenium_driver(browser_debug_mode=True)

    driver.get(channel_url)
    ensure_slept(seconds=2)  # 페이지 로드 대기

    channel_name = driver.find_element(By.CSS_SELECTOR, "meta[itemprop='name']").get_attribute("content")
    channel_name = get_pnx_unix_style(channel_name)
    return channel_name
