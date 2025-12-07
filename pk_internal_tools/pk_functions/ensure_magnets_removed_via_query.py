def ensure_magnets_removed_via_query():
    import logging
    import sqlite3
    from pathlib import Path

    from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    from pk_internal_tools.pk_objects.pk_files import F_NYAA_MAGNETS_SQLITE

    db_path = Path(F_NYAA_MAGNETS_SQLITE)
    if not db_path.exists():
        logging.error(f"Magnet database not found at: {db_path}")
        return

    try:
        while True:
            # n. Get search query from the user
            query = ensure_value_completed_2025_10_12_0000(key_name="삭제할 마그넷에 포함된 검색어를 입력하세요", options=["(480p)", "(720p)"])
            if not query.strip():
                logging.info("검색어가 입력되지 않아 작업을 취소합니다.")
                return

            query_like = f"%{query}%"

            # n. Find matching magnets before deleting
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT title, magnet FROM nyaa_magnets WHERE title LIKE ? OR magnet LIKE ?", (query_like, query_like))
            magnets_to_delete = cursor.fetchall()

            if not magnets_to_delete:
                logging.info(f"'{query}' 검색어와 일치하는 마그넷을 찾을 수 없습니다.")
                continue

            # 3. Show findings and ask for confirmation
            logging.info(f"{len(magnets_to_delete)}개의 마그넷이 삭제될 예정입니다.")
            logging.info("--- 삭제될 마그넷 샘플 ---")
            for i, (title, magnet) in enumerate(magnets_to_delete[:5]):  # Show up to 5 samples
                logging.info(f"{i + 1}. {title}")
            logging.info("-------------------------")

            confirmation = ensure_value_completed_2025_10_12_0000(
                key_name=f"정말로 {len(magnets_to_delete)}개의 마그넷을 데이터베이스에서 삭제하시겠습니까?",
                options=[PkTexts.NO, PkTexts.YES]
            )

            # 4. Delete if confirmed
            if confirmation == PkTexts.YES:
                cursor.execute("DELETE FROM nyaa_magnets WHERE title LIKE ? OR magnet LIKE ?", (query_like, query_like))
                conn.commit()
                deleted_count = cursor.rowcount
                logging.info(f"{deleted_count}개의 마그넷을 성공적으로 삭제했습니다.")
            else:
                logging.info("삭제 작업을 취소했습니다.")

            conn.close()
    except sqlite3.Error as e:
        logging.error(f"데이터베이스 작업 중 오류가 발생했습니다: {e}")
    except Exception as e:
        logging.error(f"알 수 없는 오류가 발생했습니다: {e}")
