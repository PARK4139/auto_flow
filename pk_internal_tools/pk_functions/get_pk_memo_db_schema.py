import sqlite3
import logging
from pathlib import Path

# pk_files에서 F_PK_MEMO_SQLITE 경로를 가져옵니다.
from pk_internal_tools.pk_objects.pk_files import F_PK_MEMO_SQLITE
from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
import traceback


def get_pk_memo_db_schema():
    """
    pk_memo.sqlite 데이터베이스의 스키마를 조회하여 반환합니다.
    """
    db_path = Path(F_PK_MEMO_SQLITE)

    if not db_path.exists():
        logging.warning(f"데이터베이스 파일이 존재하지 않습니다: {db_path}")
        return {}

    schema_info = {}
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 모든 테이블 이름 조회
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table_name_tuple in tables:
            table_name = table_name_tuple[0]
            # 각 테이블의 스키마 조회
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns_info = cursor.fetchall()
            
            # (cid, name, type, notnull, dflt_value, pk)
            column_details = [{
                "cid": col[0],
                "name": col[1],
                "type": col[2],
                "notnull": col[3],
                "dflt_value": col[4],
                "pk": col[5]
            } for col in columns_info]
            schema_info[table_name] = column_details
        
        conn.close()
        logging.info(f"'{db_path}' 스키마 조회 성공.")
        return schema_info

    except sqlite3.Error as e:
        logging.error(f"데이터베이스 오류 발생: {e}")
        return {}
    except Exception:
        ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
        logging.error(f"예상치 못한 오류 발생: {traceback.format_exc()}")
        return {}


if __name__ == '__main__':
    # 이 스크립트를 직접 실행하여 스키마를 확인할 경우
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    schema = get_pk_memo_db_schema()
    if schema:
        logging.info("pk_memo.sqlite 스키마 정보:")
        for table, columns in schema.items():
            logging.info(f"  테이블: {table}")
            for col in columns:
                logging.info(f" - {col['name']} ({col['type']}) {'[PK]' if col['pk'] else ''}")
    else:
        logging.info("pk_memo.sqlite 스키마 정보를 가져올 수 없습니다.")
