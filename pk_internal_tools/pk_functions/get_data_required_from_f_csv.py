import win32con
import undetected_chromedriver as uc
import tomllib
import timeit
import sqlite3
import secrets

import pickle
import os

from tkinter import UNDERLINE
from pk_internal_tools.pk_functions.is_window_title_front import is_window_title_front
from pk_internal_tools.pk_objects.pk_texts import PkTexts

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def get_data_required_from_f_csv(line_order):
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    logging.debug(rf'''{func_n}()  ''')
    df = get_df_from_issues_list_csv_deprecated()
    columns_required = df.columns.tolist()  # 전부
    # columns_required=['주행일자','해결 여부', '문제점 상세',  'SW 버전', 'f 위치', '발생시각', '문제모듈', '개입(크루)',  'Crew 요청사항', '피드백 조치','차량', '지역', '코스', '날씨', 'Crew', '위치(UTM_E)', '위치(UTM_N)', '위치(Azimuth)', '위치(Altitude)','시작 Frame', '종료 Frame','개입(점검)', '위험도', 'DB 분석피드백', 'Comment','수정 여부', '수정 내용', '교육자료', '특이 DB', 'f 크기', ] # 중요도 높은것 앞으로 변경된
    # columns_required=['주행일자', '해결 여부', '문제점 상세', 'SW 버전', 'f 위치', '발생시각', '문제모듈', '개입(크루)', 'Crew 요청사항', '피드백 조치']  # 필요한 것만
    # columns_required=["f명", "차량", "지역", "코스", "SW 버전", "운전자", "로그 분석자", "프레임", "문제점 상세", "Crew 요청사항"] ?
    data_required = {}
    nth_row = get_nth_row(df, n=line_order)
    if nth_row is not None:
        logging.debug(rf'''{PK_UNDERLINE}n="{line_order}"  ''')
        for col in columns_required:
            if col in df.columns:  # 열이 존재하는 경우만 출력 # todo : chore : get은 get 기능만 출력은 따로..
                logging.debug(f"{col}: {nth_row[col]}")
                # 필요한 것만 추가
                if col == "f 위치":
                    data_required["f 위치"] = nth_row[col]
                if col == "SW 버전":
                    data_required["SW 버전"] = nth_row[col]
                if col == "차량":
                    data_required["차량"] = nth_row[col]
                if col == "지역":
                    data_required["지역"] = nth_row[col]
                if col == "주행일자":
                    data_required["주행일자"] = nth_row[col]
                if col == "코스":
                    data_required["코스"] = nth_row[col]
            else:
                print(f"{col}: N/A")  # 열이 없는 경우 기본값 출력
                # data_required["차량아이디코드번호"] =
            # print(f"'차량아이디코드번호='{nth_row[col]}'") # 데이터 전처리하여 추출 및 딕셔너리 data_required에 추가
    return data_required
