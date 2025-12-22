import shlex
import requests
import re
from pk_internal_tools.pk_functions.get_historical_list import get_historical_list
from moviepy import VideoFileClip
from datetime import timedelta
from bs4 import BeautifulSoup
from pk_internal_tools.pk_objects.pk_directories import D_PK_EXTERNAL_TOOLS


def get_kor_from_eng(english_word: str):
    translating_dictionary = {
        "id": "아이디",
        "pw": "패스워드",
        "e mail": "이메일",
    }
    result = ""
    try:
        result = translating_dictionary[english_word]
    except Exception as e:
        result = english_word
    return result
