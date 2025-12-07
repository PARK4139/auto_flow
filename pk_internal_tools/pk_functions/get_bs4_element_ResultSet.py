def get_bs4_element_ResultSet(driver, tag_n, class_n=None):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")  # web parser 설정
    if tag_n and class_n:
        bs4_element_ResultSet = soup.find_all(tag_n, class_=class_n)
        return bs4_element_ResultSet
    if tag_n:
        bs4_element_ResultSet = soup.find_all(name=tag_n)
        return bs4_element_ResultSet
