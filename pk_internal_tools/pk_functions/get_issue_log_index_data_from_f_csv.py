

from tkinter import UNDERLINE

from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def get_issue_log_index_data_from_f_csv(line_order, issues_list_csv):
    df = get_df_from_issues_list_csv(issues_list_csv)
    columns_required = df.columns.tolist()
    data_required = {}
    line_order = int(line_order)
    nth_row = get_nth_row(df, n=line_order)
    if nth_row is not None:
        logging.debug(rf'''{PK_UNDERLINE}n="{line_order}"  ''')
        for col in columns_required:
            if col in df.columns:  # 열이 존재하는 경우만 출력 # todo get은 get 기능만 출력은 따로..
                logging.debug(f"{col}: {nth_row[col]}")
                # 필요한 것만 추가
                if col == "_f_ 위치":
                    data_required["_f_ 위치"] = nth_row[col]
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
