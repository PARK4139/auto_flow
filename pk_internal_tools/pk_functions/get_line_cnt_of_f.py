from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def get_line_cnt_of_f(f: str):
    import traceback

    try:
        line_cnt = 0
        # f 변경 감지 이슈: linecache 모듈은 f의 변경을 감지하지 못합니다.
        # f이 변경되었을 때에도 이전에 캐시된 내용을 반환하여 오래된 정보를 사용할 수 있습니다.
        # 실시간으로 f의 변경을 감지해야 하는 경우에는 정확한 결과를 얻기 어려울 수 있습니다.
        # line_cnt=len(linecache.getlines(pnx_todo))
        # logging.debug(f'line_cnt:{line_cnt}')  캐시된 내용을 반환하기 때문에. 실시간 정보가 아니다

        # 이 코드는 실시간으로 f의 변경을 감지 처리 되도록 수정, 단, f이 크면 성능저하 이슈 있을 수 있다.
        with open(file=f, mode='r', encoding="UTF-8") as file:
            # whole_contents=file.readlines()
            # logging.debug(whole_contents)
            # line_cnt=len(whole_contents)
            # line_cnt=list(en umerate(file))[-1][0] + 1
            line_cnt = file.read().count("\n") + 1
        return line_cnt
    except FileNotFoundError:
        logging.debug("f을 찾을 수 없었습니다")
        pass
    except Exception as e:
        logging.debug(f"# traceback.format_exc()\n{traceback.format_exc()}")
