import undetected_chromedriver as uc
import shutil
import pandas as pd
import ipdb
import easyocr
from selenium.common.exceptions import ElementClickInterceptedException

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


def is_containing_jpn(text):
    import re
    # pattern=r"^[\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Han}ー〜・]+$"
    # pattern=r"^\P{Script=Hiragana}\P{Script=Katakana}\P{Script=Han}ー〜・]+$"
    # pattern=r"^[\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Han}ー〜・]+$"
    # pattern=r"^[^\p{Script=Hiragana}^\p{Script=Katakana}^\p{Script=Han}ー〜・]+$"
    # pattern=r"^[^\p{Script=Hiragana}^\p{Script=Katakana}^\p{Script=Han}ー〜・]+$"
    pattern = r"^[^\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFFー〜・]+$"
    if re.search(pattern, text, flags=re.U):
        return 1
    else:
        return 0
