import platform
from webdriver_manager.chrome import ChromeDriverManager
from colorama import init as pk_colorama_init
from bs4 import BeautifulSoup
from pk_internal_tools.pk_functions.is_d import is_d


def get_found_pnx_interested_list_from_txt_f(including_texts=[], exclude_texts=[], except_extensions=[],
                                             including_extensions=[]):
    return find_pnx_interested_list_from_txt_f_x(including_texts=including_texts, exclude_texts=exclude_texts,
                                                 except_extensions=except_extensions,
                                                 f_ext_list_including=including_extensions)
