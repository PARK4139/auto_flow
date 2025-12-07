import logging

from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
from pk_internal_tools.pk_functions.get_nx import get_nx
from pk_internal_tools.pk_functions.get_pnxs_from_d_working import get_pnxs_from_d_working
from pk_internal_tools.pk_functions.is_f import is_f
from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_objects.pk_directories import d_pk_root

if __name__ == "__main__":
    try:
        import traceback

        # from pk_internal_tools.pk_objects.500_live_logic import copy, QC_MODE, get_pnxs_from_d_working, is_f, get_nx, pk_ensure_pnx_removed
        # , '{PkTexts.TRY_GUIDE}', d_pk_system, '[ UNIT TEST EXCEPTION DISCOVERED ]'
        #

        d_working = fr"C:\Users\WIN10PROPC3\Downloads\working directory for pk_external_tools pnx restoration via recuva"
        for pnx in get_pnxs_from_d_working(d_working, with_walking=False):
            if is_f(pnx):
                try:
                    with open(pnx, "rb") as f:
                        byte_data = f.read()

                    # 디코딩 시도 + 깨진 바이트 추적
                    decoded = []
                    errors = []
                    i = 0
                    while i < len(byte_data):
                        for j in range(1, 5):
                            try:
                                char = byte_data[i:i + j].decode("utf-8")
                                decoded.append(char)
                                i += j
                                break
                            except UnicodeDecodeError:
                                if j == 4:
                                    errors.append(byte_data[i])
                                    decoded.append(f"[\\x{byte_data[i]:02x}]")
                                    i += 1

                    content = "".join(decoded)

                except Exception as e:
                    print(f"❌ 파일 열기 실패: {e}")
                    exit(1)

                logging.debug(f'''_________________________________________________ ''')
                logging.debug(f'''restored ({get_nx(pnx)}) ''')
                # print(content)
                # signature = 'pk_'
                # if signature in content:
                for line in content.splitlines():
                    # if any(line.strip().startswith(k) for k in ("def ", "class ", "import", "from", "if __name__")):
                    #     print(line.strip())
                    print(line)
                user_input = input("o/x  pass/del : ")
                if user_input == 'o':
                    pass
                if user_input == 'x':
                    pk_ensure_pnx_removed(pnx)

    except:
        traceback_format_exc_list = traceback.format_exc().split("\n")
        logging.debug(f'{PK_UNDERLINE}')
        for traceback_format_exc_str in traceback_format_exc_list:
            logging.debug(f'{'[ UNIT TEST EXCEPTION DISCOVERED ]'} {traceback_format_exc_str}')
        logging.debug(f'{PK_UNDERLINE}')

    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
