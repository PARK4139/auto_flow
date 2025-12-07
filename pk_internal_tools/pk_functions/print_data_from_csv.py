import logging


def print_data_from_csv(f_csv_path, preview_rows=10):
    import pandas as pd
    import os

    if not os.path.exists(f_csv_path):
        logging.debug(f"파일이 존재하지 않습니다: {f_csv_path}")
        return
    try:
        df = pd.read_csv(f_csv_path)
        logging.debug(f"파일 로드 성공: {f_csv_path}")
        logging.debug(f"총 {len(df)}행 × {len(df.columns)}열")
        logging.debug(df)

    except Exception as e:
        logging.debug(f"️ CSV 파일 읽기 실패: {e}")
