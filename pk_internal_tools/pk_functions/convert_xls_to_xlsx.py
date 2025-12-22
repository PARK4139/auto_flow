from pk_internal_tools.pk_objects.pk_encodings import PkEncoding

import logging
from pk_internal_tools.pk_objects.pk_texts import PkTexts


def convert_xls_to_xlsx(f_xls):
    """
    2024-02-12 15:45 작성 함수 템플릿 샘플
    """
    import inspect
    import os
    import traceback
    from zipfile import BadZipFile

    import pandas as pd

    from enum import Enum

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    f_new_xlsx = f'{get_pn(f_xls)}.xlsx'

    try:
        if ".xls" == get_x(f_xls):
            if not os.path.exists(f_xls):
                logging.debug(f"{func_n}() {get_x(f_xls)} {PkTexts.UNPROCESSABLE_EXTENSION}.")
                return
    except CustomErrorUtil as e:
        logging.debug(f"{func_n}() {get_x(f_xls)} {PkTexts.UNPROCESSABLE_EXTENSION}.")
        return

    try:
        df = pd.read_excel(f_xls, engine='openpyxl')  # openpyxl 에만 적용이 되는 함수.. 에러 소지 있음.
        # if not os.path.exists(new_file_xlsx):
        df.to_excel(f_new_xlsx, index=False)
    except BadZipFile as e:
        # 유효데이터만 파싱하여 데이터프레임 으로 변환 후 Excel f로 저장
        # read_html() 를 이용하면 손상된 f을 열 수 ...
        print_yellow(f"확장자가 {get_x(f_xls)} 손상된 f 같습니다. 복구를 시도합니다")
        encoding: Enum
        df = pd.read_html(f_xls, encoding=PkEncoding.UTF8.value)
        # print_ment_blue(df)
        # print_ment_blue(df[0]) # 이번 데이터 구조의 특성상, 불필요 데이터
        # print_ment_blue(df[1]) # 이번 데이터 구조의 특성상, 불필요 데이터
        # print_ment_blue(df[2]) # 이번 데이터 구조의 특성상, 유효 데이터 , 데이터프레임 모든컬럼
        # print_ment_blue(df[2].get(0)) # 데이터프레임 첫번쨰컬럼
        # print_ment_blue(df[2].get(1)) # 데이터프레임 두번쨰컬럼
        # print_ment_blue(df[2].get(2)) #
        # print_ment_blue(df[2].get(6)) #
        # 이번 데이터에서 필요한 데이터, # 0 ~ 6 컬럼까지 유효
        df = df[2]  # 이번 데이터 구조의 특성상, 유효 데이터
        # df_selected=df[[0, 1, 2, 3, 4, 5, 6]]
        # df_selected=df[df.columns[0:7]]
        # df_selected=df[df.columns[7:]]
        # df_selected=df[df.columns[:5]]
        # df_selected=df[df.columns[1:5]]
        df = df[df.columns[:]]  # 모든 컬럼
        # print(rf'df : {df}')
        df.to_excel(f_new_xlsx, index=False)

        # # txt 로 변환
        # file_recovery=f"{get_target_as_pn(pnx_todo)}.txt"
        # print(rf'''file_recovery : {file_recovery}''')
        # shutil.copy2(pnx_todo,file_recovery)

        # # html 로 변환하여, HTML 테이블을 데이터프레임으로 저장
        # file_recovery=f"{get_target_as_pn(pnx_todo)}.html"
        # print(rf'''file_recovery : {file_recovery}''')
        # shutil.copy2(pnx_todo,file_recovery)
        # with open(file=file_recovery,mode= 'r', encoding=Encoding.UTF8.value) as file:
        #     html_content=file.read()
        # soup=BeautifulSoup(html_content, "lxml")
        # # results=soup.find_all(href=re.compile("magnet"), id='link1') # <a class="sister" href="http://example.com/magnet" id="link1">Elsie</a>
        # # results=soup.find_all("body")
        # # results=soup.find_all("html")
        # tables=soup.find_all("table")
        # table_selected=tables[2]  # 3번째 테이블 선택
        # df=pd.read_html(str(table_selected))[0]
        # print_ment_blue(df)

    except Exception as e:
        logging.debug(f"{func_n}() \n {traceback.format_exc()}")
    print_success(f"{func_n}(), success")
